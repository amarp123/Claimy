# backend/routes/report_routes.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from fastapi.responses import StreamingResponse, JSONResponse
from backend.utils.crypto_utils import (
    generate_file_key,
    encrypt_bytes_with_aes,
    encrypt_key_with_fernet,
    decrypt_key_with_fernet,
    decrypt_bytes_with_aes
)
from backend.utils.ipfs_utils import upload_to_ipfs, download_from_ipfs
from backend.web3_client import add_report_on_chain, get_reports_from_chain

import io
import mimetypes

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/upload_report")
async def upload_report(
    patient_id: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        file_bytes = await file.read()
        aes_key = generate_file_key()
        encrypted_file = encrypt_bytes_with_aes(file_bytes, aes_key)
        encrypted_key = encrypt_key_with_fernet(aes_key)
        cid = upload_to_ipfs(encrypted_file)
        if not cid:
            raise HTTPException(status_code=500, detail="Failed to upload to IPFS")

        tx_hash = add_report_on_chain(patient_id=patient_id, ipfs_cid=cid, encrypted_key=encrypted_key)

        return {
            "status": "success",
            "patient_id": patient_id,
            "ipfs_cid": cid,
            "encrypted_file_key": encrypted_key,
            "tx_hash": tx_hash,
            "message": "Report encrypted, uploaded to IPFS, and stored on blockchain."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list_reports")
def list_reports(patient_id: str = Query(..., description="Patient ID e.g. P-123456")):
    """
    Returns list of reports stored on-chain for given patient_id.
    """
    try:
        reports = get_reports_from_chain(patient_id)
        return JSONResponse(content={"status": "success", "reports": reports})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/download_report")
def download_report(patient_id: str = Form(...), index: int = Form(..., description="0-based index into reports list")):
    """
    Downloads the encrypted file from IPFS, decrypts with AES key (decrypted via Fernet),
    and returns the original file bytes as an attachment.

    Provide patient_id and the index (0 based) of the report in list_reports output.
    """
    try:
        reports = get_reports_from_chain(patient_id)
        if not reports or index < 0 or index >= len(reports):
            raise HTTPException(status_code=404, detail="Report not found")

        rep = reports[index]
        cid = rep["ipfs_cid"]
        enc_key_token = rep["encrypted_key"]

        # 1) fetch encrypted file bytes from IPFS
        encrypted_file_bytes = download_from_ipfs(cid)

        # 2) decrypt AES key
        aes_key = decrypt_key_with_fernet(enc_key_token)  # bytes

        # 3) decrypt file
        original_bytes = decrypt_bytes_with_aes(encrypted_file_bytes, aes_key)

        # 4) detect content type (basic)
        content_type = "application/octet-stream"
        filename = f"{patient_id}_{index}.bin"

        # crude PDF detection
        if original_bytes[:4] == b"%PDF":
            content_type = "application/pdf"
            filename = f"{patient_id}_{index}.pdf"
        else:
            # try to guess from magic/mime
            guess = mimetypes.guess_type(filename)[0]
            if guess:
                content_type = guess

        # create streaming response
        return StreamingResponse(io.BytesIO(original_bytes), media_type=content_type,
                                 headers={"Content-Disposition": f'attachment; filename="{filename}"'})

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

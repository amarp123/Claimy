from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.utils.ipfs_utils import upload_to_ipfs
from backend.database import SessionLocal
from backend.models_insurance import InsuranceClaim
import json, random, string
import requests

router = APIRouter(prefix="/insurance", tags=["Insurance"])

AI_AGENTS_URL = "https://unrehabilitated-mafalda-civilized.ngrok-free.dev/extract"


def generate_claim_id():
    return "C-" + ''.join(random.choices(string.digits, k=6))


@router.post("/apply_claim")
async def apply_claim(
    patient_id: str = Form(...),
    file: UploadFile = File(...)
):
    db = SessionLocal()

    # 1️⃣ Read uploaded file
    file_bytes = await file.read()

    # 2️⃣ Upload file to IPFS
    cid = upload_to_ipfs(file_bytes)
    if not cid:
        raise HTTPException(status_code=500, detail="Failed to upload file to IPFS")

    # 3️⃣ Call AI Agents pipeline (Agent-1 → Agent-2 → Agent-3)
    files = {
        "files": (file.filename, file_bytes, file.content_type)
    }

    try:
        ai_res = requests.post(AI_AGENTS_URL, files=files)
        ai_output = ai_res.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI pipeline failed: {str(e)}")

    # 4️⃣ Extract meaningful fields
    extracted = ai_output.get("extracted_json", {})
    agent3 = ai_output.get("agent_2_output", {}).get("agent_3_result", {})
    final_decision = agent3.get("final_decision", {})

    fraud = final_decision.get("fraud", {})
    approved_amount = final_decision.get("approved_amount", 0)

    is_fraud = fraud.get("is_fraud", False)
    fraud_score = fraud.get("score", 0)

    status = "rejected" if is_fraud else "approved"

    # 5️⃣ Generate claim ID
    claim_id = generate_claim_id()

    # 6️⃣ Save record in PostgreSQL
    claim = InsuranceClaim(
        claim_id=claim_id,
        patient_id=patient_id,
        documents_cid=cid,
        extracted_data=json.dumps(extracted),
        status=status,
        fraud_score=str(fraud_score),
        patient_name=extracted.get("patient_name", ""),
        diagnosis=",".join(extracted.get("diagnosis", [])),
        total_bill=str(extracted.get("total_amount", "")),
    )

    db.add(claim)
    db.commit()
    db.refresh(claim)

    # 7️⃣ Return response
    return {
    "status": "success",
    "claim_id": claim_id,
    "cid": cid,
    "decision": status,
    "approved_amount": approved_amount,
    "fraud_score": fraud_score,

    # EASY DIRECT ACCESS FIELDS
    "patient_name": extracted.get("patient_name"),
    "hospital_name": extracted.get("hospital_name"),
    "diagnosis": extracted.get("diagnosis", []),
    "total_amount": extracted.get("total_amount"),

    # Full AI pipeline
    "ai_pipeline_output": ai_output
}



@router.get("/get_claim_status")
def get_claim_status(claim_id: str):
    db = SessionLocal()
    claim = db.query(InsuranceClaim).filter(InsuranceClaim.claim_id == claim_id).first()

    if not claim:
        raise HTTPException(status_code=404, detail="Claim ID not found")

    return {
        "claim_id": claim.claim_id,
        "patient_id": claim.patient_id,
        "status": claim.status,
        "documents_cid": claim.documents_cid,
        "ai_extracted_data": json.loads(claim.extracted_data),
        "patient_name": claim.patient_name,
        "diagnosis": claim.diagnosis,
        "total_bill": claim.total_bill,
        "fraud_score": claim.fraud_score,
    }

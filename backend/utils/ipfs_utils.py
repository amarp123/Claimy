import requests
import base64
# import os # Removed as environment variables are no longer used

# --- HARDCODED PINATA KEYS ---
# WARNING: Storing keys directly in code is not secure for production environments.
PINATA_API = "4c6bf28e4b245666805e"
PINATA_SECRET = "22bdc43e418e1d7419a9c558ddd76fa61c44e9f476cb612c23cb94e38cf5c2e3"
# -----------------------------

def upload_to_ipfs(file_bytes: bytes):
    """Uploads file bytes to Pinata IPFS service using hardcoded keys."""
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    # Prepare file payload for multipart request
    files = {
        'file': ('encrypted.bin', file_bytes)
    }

    # Use the hardcoded keys in the request headers
    headers = {
        "pinata_api_key": PINATA_API,
        "pinata_secret_api_key": PINATA_SECRET
    }

    try:
        # Make the API call to Pinata
        response = requests.post(url, files=files, headers=headers)
        response.raise_for_status() # Raises an HTTPError if the status is 4xx or 5xx
        
        # Return the IPFS Hash (CID)
        return response.json()["IpfsHash"]
    except requests.exceptions.RequestException as e:
        # Catch requests errors (connection, timeout, etc.)
        print(f"IPFS Upload Error (Request Failed): {e}")
        return None
    except KeyError:
        # Handle case where Pinata returns a valid response but no 'IpfsHash' field
        print("IPFS Upload Error: Response JSON did not contain 'IpfsHash'.")
        # Added a check to print the full response text for debugging
        print("Response:", response.text) 
        return None
    

def download_from_ipfs(cid: str) -> bytes:
    """
    Downloads raw bytes from a public IPFS gateway.
    Returns the raw bytes or raises an Exception on failure.
    """
    # using Pinata public gateway — change if you prefer another
    url = f"https://gateway.pinata.cloud/ipfs/{cid}"

    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.content
    except Exception as e:
        print("IPFS download error:", e)
        raise
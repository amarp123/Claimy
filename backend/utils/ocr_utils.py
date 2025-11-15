import easyocr
import numpy as np
from PIL import Image
from io import BytesIO

reader = easyocr.Reader(['en'], gpu=False)

def extract_text(file_bytes: bytes) -> str:
    image = Image.open(BytesIO(file_bytes)).convert("RGB")
    result = reader.readtext(np.array(image), detail=0)
    return " ".join(result)

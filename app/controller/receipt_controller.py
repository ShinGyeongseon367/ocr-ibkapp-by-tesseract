from typing import List

from fastapi import UploadFile, File, APIRouter

import app.service.image_pretreatment as image_pretreatment


router = APIRouter()


@router.get("/receipt")
async def get_receipt(reporter: str, month: int, image: List[UploadFile] = File(...)):
    image_pretreatment.main_service(input_month=month, repoter_name=reporter, image_bytes= image)
    return None
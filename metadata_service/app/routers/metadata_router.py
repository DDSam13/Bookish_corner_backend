from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.metadata import MetadataRequest, MetadataResponse
from ..services.metadata_service import MetadataService

router = APIRouter(
    prefix="/metadata",
    tags=["Metadata"],
)


@router.post("/enrich", response_model=MetadataResponse)
async def enrich_book(
    data: MetadataRequest,
    db: Session = Depends(get_db),
):
    return await MetadataService(db).enrich_book(data)
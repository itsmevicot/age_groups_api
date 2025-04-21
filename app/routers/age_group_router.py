from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.age_group_schema import AgeGroupCreate, AgeGroupRead
from app.dependencies import get_age_group_service

router = APIRouter(prefix="/age-groups", tags=["age-groups"])


@router.post(
    "/",
    response_model=AgeGroupRead,
    status_code=status.HTTP_201_CREATED,
)
def create_age_group(
    payload: AgeGroupCreate,
    service=Depends(get_age_group_service),
) -> AgeGroupRead:
    try:
        return service.create(payload)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[AgeGroupRead])
def list_age_groups(
    service=Depends(get_age_group_service),
) -> List[AgeGroupRead]:
    return service.list()


@router.get("/{id}", response_model=AgeGroupRead)
def get_age_group(
    id: str,
    service=Depends(get_age_group_service),
) -> AgeGroupRead:
    result = service.get(id)
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Not found")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_age_group(
    id: str,
    service=Depends(get_age_group_service),
) -> None:
    if not service.delete(id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Not found")

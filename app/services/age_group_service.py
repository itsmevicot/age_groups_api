from typing import List, Optional

from app.repositories.age_group_repo import AgeGroupRepository
from app.schemas.age_group_schema import AgeGroupCreate, AgeGroupRead


class AgeGroupService:
    def __init__(self, repo: AgeGroupRepository):
        self.repo = repo

    def list(self) -> List[AgeGroupRead]:
        return self.repo.list()

    def get(self, id: str) -> Optional[AgeGroupRead]:
        return self.repo.get(id)

    def create(self, payload: AgeGroupCreate) -> AgeGroupRead:
        if payload.min_age >= payload.max_age:
            raise ValueError("min_age must be less than max_age")

        for group in self.repo.list():
            if not (payload.max_age < group.min_age or payload.min_age > group.max_age):
                raise ValueError(
                    f"Age range {payload.min_age}-{payload.max_age} overlaps "
                    f"with existing range {group.min_age}-{group.max_age}"
                )

        return self.repo.create(payload)

    def delete(self, id: str) -> bool:
        return self.repo.delete(id)


from typing import List, Optional
from bson import ObjectId
from app.schemas.age_group_schema import AgeGroupRead, AgeGroupCreate


class AgeGroupRepository:
    def __init__(self, db):
        self.collection = db["age_groups"]

    def create(self, payload: AgeGroupCreate) -> AgeGroupRead:
        data = payload.model_dump()
        result = self.collection.insert_one(data)
        return AgeGroupRead(id=str(result.inserted_id), **data)

    def list(self) -> List[AgeGroupRead]:
        out: List[AgeGroupRead] = []
        for doc in self.collection.find():
            out.append(
                AgeGroupRead(
                    id=str(doc["_id"]),
                    name=doc["name"],
                    min_age=doc["min_age"],
                    max_age=doc["max_age"],
                )
            )
        return out

    def get(self, id: str) -> Optional[AgeGroupRead]:
        doc = self.collection.find_one({"_id": ObjectId(id)})
        if not doc:
            return None

        return AgeGroupRead(
            id=str(doc["_id"]),
            name=doc["name"],
            min_age=doc["min_age"],
            max_age=doc["max_age"],
        )

    def delete(self, id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0

from fastapi import Depends
from pymongo.database import Database

from app.config.settings import get_settings
from app.database.provider import DatabaseProvider
from app.repositories.age_group_repo import AgeGroupRepository
from app.services.age_group_service import AgeGroupService

_settings = get_settings()


def get_db() -> Database:
    """
    Return either a real Mongo Database or a mongomock database
    depending on settings.environment.
    """
    return DatabaseProvider.get_db()


def get_age_group_repo(db: Database = Depends(get_db)) -> AgeGroupRepository:
    """
    Inject a DB into your repository.
    """
    return AgeGroupRepository(db)


def get_age_group_service(
    repo: AgeGroupRepository = Depends(get_age_group_repo),
) -> AgeGroupService:
    """
    Inject the repo into your service.
    """
    return AgeGroupService(repo)

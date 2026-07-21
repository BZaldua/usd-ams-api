from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from .config.database import get_db
from .infrastructure.repositories import (
    AssetRepository,
    PublishRepository,
    TaskRepository,
)
from .services import AssetService, PublishService, TaskService


class AppProvider(Provider):

    get_db_session = provide(get_db, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    def get_asset_repository(self, db_session: AsyncSession) -> AssetRepository:
        return AssetRepository(db_session)

    @provide(scope=Scope.REQUEST)
    def get_task_repository(self, db_session: AsyncSession) -> TaskRepository:
        return TaskRepository(db_session)

    @provide(scope=Scope.REQUEST)
    def get_publish_repository(self, db_session: AsyncSession) -> PublishRepository:
        return PublishRepository(db_session)

    @provide(scope=Scope.REQUEST)
    def get_asset_service(self, repository: AssetRepository) -> AssetService:
        return AssetService(repository)

    @provide(scope=Scope.REQUEST)
    def get_task_service(self, repository: TaskRepository) -> TaskService:
        return TaskService(repository)

    @provide(scope=Scope.REQUEST)
    def get_publish_service(
        self,
        repository: PublishRepository,
        asset_service: AssetService,
        task_service: TaskService,
    ) -> PublishService:
        return PublishService(repository, asset_service, task_service)

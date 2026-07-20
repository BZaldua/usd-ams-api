from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from .config.database import get_db
from .infrastructure.repositories import AssetRepository, TaskRepository
from .services import AssetService, TaskService


class AppProvider(Provider):

    get_db_session = provide(get_db, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    def get_asset_service(self, repository: AssetRepository) -> AssetService:
        return AssetService(repository)

    @provide(scope=Scope.REQUEST)
    def get_asset_repository(self, db_session: AsyncSession) -> AssetRepository:
        return AssetRepository(db_session)

    @provide(scope=Scope.REQUEST)
    def get_task_service(self, repository: TaskRepository) -> TaskService:
        return TaskService(repository)

    @provide(scope=Scope.REQUEST)
    def get_task_repository(self, db_session: AsyncSession) -> TaskRepository:
        return TaskRepository(db_session)

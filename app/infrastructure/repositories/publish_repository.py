from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.infrastructure.database import PublishModel
from app.infrastructure.repositories.base import BaseRepository


class PublishRepository(BaseRepository[PublishModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, PublishModel)

    async def get_latest_version(self, asset_id: int, task_id: int) -> int:
        query = (
            select(PublishModel.version)
            .where(PublishModel.asset_id == asset_id, PublishModel.task_id == task_id)
            .order_by(PublishModel.version.desc())
            .limit(1)
        )
        result = await self.db.execute(query)
        latest = result.scalars().first()
        return latest if latest is not None else 0

    async def get_filtered(
        self,
        task_id: int | None = None,
        asset_id: int | None = None,
        version: int | None = None,
    ) -> list[PublishModel]:
        query = select(PublishModel)

        if asset_id:
            query = query.where(PublishModel.asset_id == asset_id)
        if task_id:
            query = query.where(PublishModel.task_id == task_id)
        if version:
            query = query.where(PublishModel.version == version)

        query = query.order_by(PublishModel.version.desc())
        result = await self.db.execute(query)
        publish_models: list[PublishModel] = list(result.scalars().all())
        return publish_models

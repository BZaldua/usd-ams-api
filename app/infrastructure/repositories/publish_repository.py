from sqlalchemy.future import select

from app.infrastructure.database import PublishModel
from app.infrastructure.repositories.base import BaseRepository


class PublishRepository(BaseRepository[PublishModel]):
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

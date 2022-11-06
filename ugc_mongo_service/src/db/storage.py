from abc import ABC, abstractmethod
from typing import Dict

from db.mongo import get_mongo


class Storage(ABC):
    def __call__(self):
        return self

    @abstractmethod
    async def create(self, document: Dict[str, str]):
        pass

    @abstractmethod
    async def search(self, filters: Dict[str, str], offset: int, limit: int):
        """The filter argument is a prototype document that all results must match."""
        pass

    @abstractmethod
    async def get(self, spec: Dict[str, str]):
        """Get a single document from the database."""
        pass

    @abstractmethod
    async def update(self, spec: Dict[str, str], document: Dict[str, str], ):
        pass

    @abstractmethod
    async def delete(self, spec: Dict[str, str]):
        pass


class AsyncMongoStorage(Storage):
    async def create_mongo(self, db: str, collection: str):
        super().__init__()
        self.mongo = await get_mongo()
        self.db = db
        self.collection = collection
        return self

    async def create(self, document: Dict[str, str]) -> Dict[str, str]:
        return await self.mongo[self.db][self.collection].insert_one(document)

    async def get(self, spec: Dict[str, str]) -> Dict[str, str]:
        return await self.mongo[self.db][self.collection].find_one(spec)

    async def search(self, filters: Dict[str, str], offset: int = 0, limit: int = 100):
        cursor = self.mongo[self.db][self.collection].find(filters)
        return await cursor.to_list(length=limit)

    async def update(self, spec: Dict[str, str], document: Dict[str, str]):
        updated = await self.mongo[self.db][self.collection].update_one(spec, document)
        return updated.matched_count > 0

    async def delete(self, spec: Dict[str, str]):
        return await self.mongo[self.db][self.collection].delete_one(spec)


async def get_mongo_storage(**kwargs) -> Storage:
    return await AsyncMongoStorage.create_mongo(**kwargs)

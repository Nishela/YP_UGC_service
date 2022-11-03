from abc import ABC, abstractmethod

from db.mongo import get_mongo

mongo_client = await get_mongo()


class Storage(ABC):
    def __call__(self):
        return self

    @abstractmethod
    async def create(self, document: dict):
        pass

    @abstractmethod
    async def search(self, filters: dict, offset: int, limit: int):
        """The filter argument is a prototype document that all results must match."""
        pass

    @abstractmethod
    async def get(self, spec: dict):
        """Get a single document from the database."""
        pass

    @abstractmethod
    async def update(self, spec: dict, document: dict,):
        pass

    @abstractmethod
    async def delete(self, spec: dict):
        pass


class AsyncMongoStorage(Storage):
    def __init__(self, db: str, collection: str):
        super().__init__()
        self.mongo = mongo_client
        self.db = db
        self.collection = collection

    async def create(self, document: dict) -> dict:
        return await self.mongo[self.db][self.collection].insert_one(document)

    async def get(self, spec: dict) -> dict:
        return await self.mongo[self.db][self.collection].find_one(spec)

    async def search(self, filters: dict, offset: int = 0, limit: int = 100):
        cursor = self.mongo[self.db][self.collection].find(filters)
        return await cursor.to_list(length=limit)

    async def update(self, spec: dict, document: dict):
        updated = await self.mongo[self.db][self.collection].update_one(spec, document)
        return updated.matched_count > 0

    async def delete(self, spec: dict):
        return await self.mongo[self.db][self.collection].delete_one(spec)


def get_mongo_storage(**kwargs) -> Storage:
    return AsyncMongoStorage(**kwargs)

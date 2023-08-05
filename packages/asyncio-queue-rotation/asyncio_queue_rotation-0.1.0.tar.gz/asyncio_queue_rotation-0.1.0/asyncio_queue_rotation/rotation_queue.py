import asyncio
from typing import TypeVar, Generic

T = TypeVar('T')


class RotationQueue(asyncio.Queue, Generic[T]):
    """
    RotationQueue
    """

    def __init__(self, maxsize=1, *, loop=None):
        if maxsize < 1:
            maxsize = 1
        super().__init__(maxsize, loop=loop)

    async def get(self) -> T:
        return await super(RotationQueue, self).get()

    async def put(self, item: T) -> None:
        if self.full():
            super(RotationQueue, self)._get()
        await super(RotationQueue, self).put(item)

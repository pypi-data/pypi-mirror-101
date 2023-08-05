# asyncio rotation queue

based on [asyncio.Queue](https://docs.python.org/3/library/asyncio-queue.html)

On put( element )
if qsize() >= maxsize  
first element popped out and put elements added to back of queue

```python
from asyncio_queue_rotation import RotationQueue

rotation_queue = RotationQueue(10)
await rotation_queue.put(1)

```

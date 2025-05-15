#!/usr/local/bin/python

import asyncio
import math
import random

from mimesis import Generic

from app.database import session_manager

random_seed = math.floor(random.random() * 100000)
mimesis = Generic(seed=random_seed)

print("\n\n")


async def main():
    async with session_manager.session() as db_session:
        await db_session.commit()


asyncio.run(main())

import json
import os
import re
import asyncio
import aiofiles


async def test():
    async with aiofiles.open("/Users/johnlennon/RusttmGDrive/Python/MoiSklad_v2/MoiSkladPackage/data/temporary_file.json", 'r') as json_file:
        json_data = await json_file.read()
    data = json.loads(json_data)
    return data
print(asyncio.run(test()))
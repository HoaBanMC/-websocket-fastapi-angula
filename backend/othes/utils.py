import asyncio

async def haevy_data_precessing(data: dict):
    await asyncio.sleep(1)
    message_proccessed = data.get("message", "").upper()
    return message_proccessed
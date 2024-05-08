import aiohttp


async def tasks_api_request():
    url = "http://65.109.135.126/api/v1/task/task-list/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def check_student_api_request(telegram_id):
    url = f"http://65.109.135.126/api/v1/student/check/{telegram_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def create_student_api_request(telegram_id, first_name, last_name, group_number):
    url = "http://65.109.135.126/api/v1/student/create/"
    data = {
        "telegram_id": telegram_id,
        "first_name": first_name,
        "last_name": last_name,
        "group_number": group_number
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.json()


async def get_task_by_slug_api_request(telegram_id, slug):
    url = f"http://65.109.135.126/api/v1/task/start-task?telegram_id={telegram_id}&task_slug={slug}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def stop_task_api_request(telegram_id, slug):
    url = f"http://65.109.135.126/api/v1/task/delete-task?telegram_id={telegram_id}&task_slug={slug}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

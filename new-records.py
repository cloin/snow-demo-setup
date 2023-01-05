import asyncio
import aiohttp
import json
import os
import time

# Poll ServiceNow API for new records and print out the record number, sys_id and short description as a JSON object.
# Uses asyncio and aiohttp, and authenticates using aiohttp.BasicAuth with the login credentials and instance URL provided as environment variables.
# Only prints out records created after the script began executing, and only prints out each record once.
# Table to watch for records configured as environment variable `SN_TABLE`

#  ➜ python3.9 new records.py
#  {"number": "INC0012170", "sys_id": "b7206ff71b88e950b76a0d0fdc4bcb7b", "short_description": "test incident 1", "incident_state": "1"}
#  {"number": "INC0012171", "sys_id": "4630eb7b1b88e950b76a0d0fdc4bcb4e", "short_description": "test incident 2", "incident_state": "1"}

async def check_records(start_time, printed_records):
    username = os.environ['SN_USERNAME']
    password = os.environ['SN_PASSWORD']
    instance = os.environ['SN_HOST']
    table = os.environ['SN_TABLE']
    interval = 1 # Poll every 1 seconds

    async with aiohttp.ClientSession() as session:
        auth = aiohttp.BasicAuth(login=username, password=password)
        while True:
            async with session.get(f'{instance}/api/now/table/{table}?sysparm_query=sys_created_onONToday@javascript:gs.beginningOfToday()@javascript:gs.endOfToday()', auth=auth) as resp:
                if resp.status == 200:

                    records = await resp.json()
                    for record in records['result']:

                        if record['sys_updated_on'] > start_time and record['sys_id'] not in printed_records:
                            printed_records.add(record['sys_id'])
                            print(json.dumps({
                                'number': record['number'],
                                'sys_id': record['sys_id'],
                                'short_description': record['short_description'],
                            }))
                else:
                    print(f'Error {resp.status}')
            await asyncio.sleep(interval)  # Poll every interval seconds

async def main():
    start_time = time.time()
    start_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(start_time))
    printed_records = set()
    await check_records(start_time_str, printed_records)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())

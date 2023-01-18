import asyncio
import time
from typing import Any, Dict
import aiohttp

# event-driven-ansible source plugin example
# Poll ServiceNow API for new records in a table and print out the record
# Only prints out records created after the script began executing
# and only prints out each record once.

# - name: Watch for new records
#   hosts: localhost
#   sources:
#     - cloin.servicenow.records:
#         instance: "{{ SN_HOST }}"
#         username: "{{ SN_USERNAME }}"
#         password: "{{ SN_PASSWORD }}"
#         table: "{{ SN_TABLE }}"
#         interval: 5
#   rules:
#     - name: New record created
#       condition: event.sys_id is defined
#       action:
#         debug:

async def main(queue: asyncio.Queue, args: Dict[str, Any]):

    instance = args.get("instance")
    username = args.get("username")
    password = args.get("password")
    table = args.get("table")
    # query = args.get("query")
    interval = int(args.get("interval", 5))

    start_time = time.time()
    start_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(start_time))
    printed_records = set()
    async with aiohttp.ClientSession() as session:
        auth = aiohttp.BasicAuth(login=username, password=password)
        while True:
            async with session.get(f'{instance}/api/now/table/{table}?sysparm_query=sys_created_onONToday@javascript:gs.beginningOfToday()@javascript:gs.endOfToday()', auth=auth) as resp:
                if resp.status == 200:

                    records = await resp.json()
                    for record in records['result']:

                        if record['sys_updated_on'] > start_time_str and record['sys_id'] not in printed_records:
                            printed_records.add(record['sys_id'])
                            print(record)
                else:
                    print(f'Error {resp.status}')
            await asyncio.sleep(interval)

import asyncio
import aiohttp
import json
import os
import time

# Poll ServiceNow API for new incidents and print out the incident number, sys_id, incident_status and short description as a JSON object.
# Uses asyncio and aiohttp, and authenticates using aiohttp.BasicAuth with the login credentials and instance URL provided as environment variables.
# Only prints out incidents created after the script began executing, and only prints out each incident once.

#  ➜ python3.9 new-incidents.py
#  {"number": "INC0012170", "sys_id": "b7206ff71b88e950b76a0d0fdc4bcb7b", "short_description": "test incident 1", "incident_state": "1"}
#  {"number": "INC0012171", "sys_id": "4630eb7b1b88e950b76a0d0fdc4bcb4e", "short_description": "test incident 2", "incident_state": "1"}

async def check_incidents(start_time, interval, printed_incidents):
    username = os.environ['SN_USERNAME']
    password = os.environ['SN_PASSWORD']
    instance = os.environ['SN_HOST']

    async with aiohttp.ClientSession() as session:
        auth = aiohttp.BasicAuth(login=username, password=password)
        while True:
            async with session.get(f'{instance}/api/now/table/incident?sysparm_query=sys_created_onONToday@javascript:gs.beginningOfToday()@javascript:gs.endOfToday()', auth=auth) as resp:
                if resp.status == 200:
                    incidents = await resp.json()
                    for incident in incidents['result']:
                        if incident['sys_updated_on'] > start_time and incident['sys_id'] not in printed_incidents:
                            printed_incidents.add(incident['sys_id'])
                            print(json.dumps({
                                'number': incident['number'],
                                'sys_id': incident['sys_id'],
                                'short_description': incident['short_description'],
                                'incident_state': incident['incident_state'],
                            }))
                else:
                    print(f'Error {resp.status}')
            await asyncio.sleep(interval)  # Poll every interval seconds

async def main():
    start_time = time.time()
    start_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(start_time))
    interval = 1 # Poll every 1 seconds
    printed_incidents = set()
    await check_incidents(start_time_str, interval, printed_incidents)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

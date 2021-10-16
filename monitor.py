import time
import logging
import os
from importlib import util
import asyncio
# pip3 install matrix-nio
from nio import AsyncClient, MatrixRoom, RoomMessageText
import os
from temp import get_temp
import socket
import sys, getopt

# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(module)s:%(name)s:%(funcName)s: %(message)s', datefmt='%Y:%m:%d::%H:%M:%S')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# getting credentials
ELEM_ROOM = os.environ.get("ELEM_ROOM")
ELEM_USR = os.environ.get("ELEM_USR")
ELEM_PSW = os.environ.get("ELEM_PSW")

# poll period seconds
CADENCE = 600 # 10min
# probationary temp limit for warning
LIMIT = 80

# argument parsing
try:
    opts, args = getopt.getopt(sys.argv[1:], "hl:", ["limit="])
except getopt.GetoptError:
    logger.info('Usage: monitor.py -l <limit> [--limit=<limit>]')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        logger.info('Usage: monitor.py -l <limit> [--limit=<limit>]')
        sys.exit()
    elif opt in ("-l", "--limit"):
        try:
            LIMIT = int(arg)
        except:
            logger.info('Usage: monitor.py -l <limit> [--limit=<limit>]')
            sys.exit(2)

async def message_callback(
    room: MatrixRoom, event: RoomMessageText) -> None:
    print(f"{room.user_name(event.sender)} | {event.body}")

async def main() -> None:
    client = AsyncClient("https://matrix.org", ELEM_USR)
    client.add_event_callback(message_callback, RoomMessageText)

    print(await client.login(ELEM_PSW))

    await client.join(ELEM_ROOM)

    logger.info(f'limit for warnings is set at {LIMIT} \xb0C.')
    while(True):
        temp = get_temp()
        logger.info(f'{socket.gethostname()} temp is {temp:.2f} \xb0C.')
        if temp > LIMIT:
            await client.room_send(
                room_id=ELEM_ROOM,
                message_type="m.room.message",
                content = {
                    "msgtype": "m.text",
                    "body": f"WARNING: {socket.gethostname()} temp is {get_temp():.2f} \xb0C."
                }
            )
            time.sleep(3600) # if message is sent, wait an hour
        time.sleep(CADENCE) # check temp every 10min

    await client.sync_forever(timeout=3.6e+6) # milliseconds (1hr)

asyncio.get_event_loop().run_until_complete(main())

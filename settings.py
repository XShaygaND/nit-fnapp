from pytz import timezone
import dotenv
import os

dotenv.load_dotenv()

## GENERAL ##

BREAKFAST_LIMIT = {'hour': 8, 'min': 0}
LUNCH_LIMIT = {'hour': 13, 'min': 30}
DINNER_LIMIT = {'hour': 18, 'min':45}

BLOCKED_MESSAGE = 'You have been blocked, for removal contact @Shaygan_2_2'


## USER ##

MAX_WARNS = 3


## SERVER ##

TIMEZONE = timezone('Asia/Tehran')
DATABASE = os.getenv('DATABASE')
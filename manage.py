import sys
import os
import dotenv
from time import sleep

dotenv.load_dotenv()

dev_token = dotenv.get_key('.env', 'DEV_BOT_TOKEN')
test_token = dotenv.get_key('.env', 'TEST_BOT_TOKEN')

def runbot():
    from bot import bot

    try:
        bot.polling()

    except Exception as err:
        print(err)


def set_test_db():
    dotenv.set_key('.env', 'DATABASE', 'testdb.json')
    dotenv.set_key('.env', 'CURRENT_BOT_TOKEN', test_token)
    

def truncate_db():
    from storage import db

    db.drop_tables()


arg_funcs = {
    'run':  runbot,
    'trunc': truncate_db,
    'testdb': set_test_db,
}

args = sys.argv

for arg in args[1:]:
    if arg in arg_funcs:
         arg_funcs[arg]()

    else:
        print('invalid argument: ' + arg)

dotenv.set_key('.env', 'DATABASE', 'db.json')
dotenv.set_key('.env', 'CURRENT_BOT_TOKEN', dev_token)

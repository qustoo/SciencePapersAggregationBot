import os

from dotenv import load_dotenv

PARENT_PATH = os.path.abspath(os.path.join(os.getcwd(), os.pardir, '.env'))
load_dotenv(PARENT_PATH)

BOT_TOKEN = os.getenv('BOT_TOKEN')
FILENAME_DATABASE = os.getenv('FILENAME_DATABASE')

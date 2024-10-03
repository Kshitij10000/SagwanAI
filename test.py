import os
import django
from time import sleep
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hello.settings')
django.setup()

from Home.tasks import fetch_stock_data

def main():
    logging.info("Dispatching the Celery task...")
    result = fetch_stock_data.delay()
    
    while not result.ready():
        logging.info("Task not ready, sleeping for 1 second...")
        sleep(1)
    
    logging.info("Task completed, fetching result...")
    print("Task result:", result.result)

if __name__ == "__main__":
    main()

__author__ = 'andrew.sielen'

# External
import os
import time

# System
import system as syt
if __name__ == "__main__": syt.setup_logger()

# Validation
from database import database as db
from database import health

# Menu

from navigation.M0_main_menu import main_menu

def validate_database():
    if os.path.isfile(db):
        syt.log_info("Connected to database: {}".format(db))
    else:
        syt.log_warning("No Database Found. Please locate it or create one")
    health.validate_all()
    health.get_basic_database_info()



if __name__ == "__main__":
    validate_database()
    time.sleep(1)
    main_menu()

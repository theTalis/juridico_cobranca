import re
from datetime import datetime

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
 
def is_valid_email(email):
    if(re.fullmatch(regex, email)):
        return True
    return False
 
def is_valid_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d").date()
        return True
    except ValueError:
        print('error')
        return False
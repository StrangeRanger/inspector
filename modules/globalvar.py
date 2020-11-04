import collections
from datetime import datetime, timedelta
from sys import exit
from os import geteuid

# Number of days that will be checked that came before today: N = 1 means that today's
#   and yesterday's logs will be checked
N = 8
today = datetime.now().date()
start_date = today - timedelta(days=N)
this_year = datetime.now().year
last_year = this_year - 1
# A.1. A defaultdict that maps objects (dates and users) to a counter
days = collections.defaultdict(collections.Counter)
# B.1. Two nested defaultdicts that map objects (dates, users, and victims) to a counter
daysv2 = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))

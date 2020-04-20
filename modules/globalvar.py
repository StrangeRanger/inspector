import collections
from datetime import datetime, timedelta
from sys import exit

N = 8 # number of days that will be checked that came before today: N = 1 means that today's and yesterday's logs will be checked
today = datetime.now().date()
start_date = today - timedelta(days=N)
this_year = datetime.now().year
last_year = this_year - 1
days = collections.defaultdict(collections.Counter) # A.1. a defaultdict that maps objects (dates and users) to a counter
daysv2 = collections.defaultdict(lambda: collections.defaultdict(collections.Counter)) # B.1. two nested defaultdicts that map objects (dates, users, and victims) to a counter

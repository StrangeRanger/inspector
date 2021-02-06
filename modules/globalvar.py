import collections
from datetime import datetime, timedelta


RED = "\033[1;31m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
DEFCLR = "\033[0m"
# Number of days that will be checked that came before today: N = 1 means that today's
# and yesterday's logs will be checked
N = 8
today = datetime.now().date()
start_date = today - timedelta(days=N)
this_year = datetime.now().year
last_year = this_year - 1
# A.1. A defaultdict that maps objects (dates and users) to a counter
days = collections.defaultdict(collections.Counter)
# B.1. Two nested defaultdicts that map objects (dates, users, and victims) to a counter
daysv2 = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))

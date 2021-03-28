"""
Contains variables used by both 'distro_specific.py' and 'inspector.py.
"""
####[ Imports ]#########################################################################


import collections
from datetime import datetime, timedelta


####[ Variables ]#######################################################################


RED = "\033[1;31m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
DEFCLR = "\033[0m"
N = 8
"""Number of days prior to today, that'll be checked.

If N = 1, logs that were created today and yesterday will be checked.
"""
today = datetime.now().date()
"""Today's date"""
start_date = today - timedelta(days=N)
"""The date to begin inspecting from"""
this_year = datetime.now().year
"""Current year"""
last_year = this_year - 1
"""Last year"""
days = collections.defaultdict(collections.Counter)  # A.1.
"""Map objects (dates and users) to a counter."""
daysv2 = collections.defaultdict(
    lambda: collections.defaultdict(collections.Counter)
)  # B.1.
"""Two nested defaultdicts that map objects (dates, users, and victims) to a counter."""

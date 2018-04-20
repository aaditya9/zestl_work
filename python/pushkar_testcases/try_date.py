import time

import datetime
#
aa = '2008-09-17 14:02:00'

utc_datetime = datetime.datetime.utcnow()
date = utc_datetime.strftime(aa)
print date
# def local_to_utc(t):
#     secs = time.mktime(t)
#     return time.gmtime(secs)
# time = local_to_utc(aa)
# print time


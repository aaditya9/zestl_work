# from datetime import datetime
# import  time
#
# start_date='20180518013000'
# date=time.strftime("%Y-%m-%d %H:%M:%S",
#                   time.gmtime(time.mktime(time.strptime(start_date,
#                                                         "%Y%m%d%H%M%S"))))
# print(date)










import pytz

import datetime
tz = pytz.timezone('Asia/Calcutta')
ct = datetime.datetime.now(tz=tz)

print(ct)


import os
import datetime

os.environ['PANDA_URL'] = 'http://ai-idds-01.cern.ch:25080/server/panda'
os.environ['PANDA_URL_SSL'] = 'https://ai-idds-01.cern.ch:25443/server/panda'

from pandatools import Client  # noqa E402

"""
jediTaskID = 998
ret = Client.getPandaIDsWithTaskID(jediTaskID, verbose=False)
# print(ret)
jobids = ret[1]
# print(jobids)

ret = Client.getJobStatus(ids=jobids, verbose=False)
print(ret)

ret = Client.getFullJobStatus(ids=jobids, verbose=False)
# print(ret)

ret = Client.getJediTaskDetails({'jediTaskID': jediTaskID}, True, True, verbose=False)
print(ret)
"""

"""
jobids = []
Client.getJobStatus(ids=jobids, verbose=False)

Client.getJediTaskDetails(taskDict,fullFlag,withTaskInfo,verbose=False)

Client.getFullJobStatus(ids, verbose=False)
"""

# getJobIDsJediTasksInTimeRange(timeRange, dn=None, minTaskID=None, verbose=False, task_type='user')
# /DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=atlpilo1/CN=614260/CN=Robot: ATLAS Pilot1

start_time = datetime.datetime.utcnow() - datetime.timedelta(hours=5)
start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
# ret = Client.getJobIDsJediTasksInTimeRange(start_time, verbose=False)
# print(ret)

# ret = Client.getJobIDsJediTasksInTimeRange(start_time, task_type='test', verbose=False)
# print(ret)
# ret = Client.getJobIDsJediTasksInTimeRange(start_time, dn='/DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=atlpilo1/CN=614260/CN=Robot: ATLAS Pilot1', task_type='test', verbose=False)
# print(ret)
# ret = Client.getJobIDsJediTasksInTimeRange(start_time, dn='atlpilo1', task_type='test', verbose=False)
# print(ret)


taskID = 1365
newOpts = {}
# warning for PQ
# site = newOpts.get('site', None)
# excludedSite = newOpts.get('excludedSite', None)
# for JEDI
status, out = Client.retryTask(taskID, verbose=True, properErrorCode=True, newParams=newOpts)
print(status)
print(out)

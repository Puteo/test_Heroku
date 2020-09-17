import hashlib
import pandas as pd
import json

from app.models.log import Logs, Log

def GetHashValue(str):
   return hashlib.sha256(str.encode()).hexdigest()

def timetostr(t):
   return t.strftime('%Y/%m/%d %H:%M:%S')

def GetLogsJsonformat():
   logs = Logs()
   logs.set_all_logs()
   if logs.logs is None:
      return None
   l_logs = []
   for log in logs.logs:
      l_logs.append(log.value)
   df_log = pd.DataFrame(l_logs)
   df_log['str_time'] = df_log['time'].map(timetostr)
   df_log = df_log.drop('time', axis=1)
   dict_log = df_log.to_dict()
   dict_log['status'] = 'Success'
   return json.dumps(dict_log)
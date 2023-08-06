from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests, os, json as json_lib


retry_strategy = Retry(
    total=5,
    backoff_factor=15,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS", "POST"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)


def get_data_catalog_service_auth(username, password):
  return { "auth": HTTPBasicAuth(username, password) }
  
  
def request_post_if_has_value(url, json=None, extra={}):
  result = []
  if json:
    for each_row in json:
      print(f"json payload {json_lib.dumps(each_row, sort_keys=True, indent=4)}")
      response = http.post(url, json=each_row, **extra)
      if response.status_code == 200:
        result.append(True)
        #response.json() 
      else: 
        result.append(False)
    
  return result
        
        



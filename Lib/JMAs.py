import requests
import datetime

# JMA Inherit Param
area = "240000" # 地域コード（三重県）
area_detail = "240010" # 予報区（三重県北中部地方）
stnid1 = "53091" # 観測所番号（三重県亀山市）
stnid2 = "53133" # 観測所番号（三重県津市）

# JMA URLs
url_forecast = "https://www.jma.go.jp/bosai/forecast/data/forecast/"+area+".json"
url_amedas = "https://www.jma.go.jp/bosai/amedas/data/latest_time.txt"

url_obs = "https://www.jma.go.jp/bosai/forecast/data/observation/"+area_detail+".json"
url_overview_weekly = "https://www.jma.go.jp/bosai/forecast/data/overview_week/"+area+".json"

# JMA JSON/TXT Acquision
def acquire_JMA_forecast(url) -> str:   # 3日間天気予報
  req = requests.get(url)
  if 'json' in req.headers.get('content-type'):
    data_forecast = req.json()
  else:
    data_forecast = 'Back Text b/c No JSON Format: acquire_JMA_forcast()'
  return data_forecast

def acquire_amedas_data(url,stnid) -> str:   # アメダス（測候所データ）
  # 更新時刻確認
  req = requests.get(url)
  if 'text/plain' in req.headers.get('content-type'):
    data_present = datetime.datetime.strptime(req.text, "%Y-%m-%dT%H:%M:%S%z")
  else:
    data_present = 'Back Text b/c No text/plain Format: acquire_amedas_data() - 1st process'
    return data_present

  yyyymmdd = data_present.strftime('%Y%m%d')
  h3 = ("0" + str((data_present.hour//3)*3))[-2:]
  urls = "https://www.jma.go.jp/bosai/amedas/data/point/"+stnid+"/"+yyyymmdd+"_"+h3+".json"

  # アメダスデータ
  req = requests.get(urls)
  if 'json' in req.headers.get('content-type'):
    data_amedas = req.json()
  else:
    data_amedas = 'Request Error or Not JSON Format: acquire_amedas_data() - 2nd process'
  return data_amedas

#def acquire_JMA_forecast_observation() -> str:   # 天気概況
#  req_obs = requests.get(url_JMA_obs)
#  data_obs = req_obs.json()
#  txt_obs = "\n".join(data_obs["text"].split())
#  return txt_obs

#def acquire_overview_weekly() -> str:   # 週間天気概況
#  req_ov = requests.get(url_overview_weekly)
#  data_ov = req_ov.json()
#  return data_ov

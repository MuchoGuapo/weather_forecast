# Libraries
import sys
from datetime import datetime, timedelta

from Lib.LCDs import *
from Lib.JMAs import *
from Lib.deg16dir import *

import smbus

# I2C open
bus = smbus.SMBus(1)

# Definition - YMDs
dt_today = datetime.date.today()
dt_tomorrow = dt_today + timedelta(1)
dt_dayaftertomorrow = dt_today + timedelta(2)

# Function
def get_keydata(data:list) -> str:
  if data[1] == 0:
    return str(data[0])
  else:
    return "Check Data"

def find_index(data:list, code:str) -> int:
  index = [num for num, i in enumerate(data) if i["area"]["code"] == code][0]
  return index

# main
def main():
  lcd_init()

  while True:
    argv = sys.argv
    argc = len(argv)

    # 1.Data Acquision
    data_forecast = acquire_JMA_forecast(url_forecast)
    data_forecast = data_forecast[0]["timeSeries"][0]["areas"]

    data_amedas = acquire_amedas_data(url_amedas, stnid1)
    data_amedas2 = acquire_amedas_data(url_amedas, stnid2)

    # 2.Processing
    ## 2a.forecast
    index_forecast = find_index(data_forecast, area_detail)

    weathers = data_forecast[index_forecast]["weathers"]
    wt_today = " ".join(weathers[0].split())
    wt_tomorrow = " ".join(weathers[1].split())
    wt_dayaftertomorrow = " ".join(weathers[2].split())

    weatherCodes = data_forecast[index_forecast]["weatherCodes"]
    wcode_today = " ".join(weatherCodes[0].split())
    wcode_tomorrow = " ".join(weatherCodes[1].split())
    wcode_dayaftertomorrow = " ".join(weatherCodes[2].split())

    ## 2b.amedas
    key_max = max(data_amedas)
    key_max2 = max(data_amedas2)

    temp = get_keydata(data_amedas[key_max]["temp"])
    humi = get_keydata(data_amedas[key_max]["humidity"])

    wind = get_keydata(data_amedas[key_max]["wind"])
    windir = get_keydata(data_amedas[key_max]["windDirection"])
    windir = get_Dir(int(windir), "en")

    sun1h = get_keydata(data_amedas[key_max]["sun1h"])
    prcp1h = get_keydata(data_amedas[key_max]["precipitation1h"])

    temp2 = get_keydata(data_amedas2[key_max2]["temp"])
    humi2 = get_keydata(data_amedas2[key_max2]["humidity"])
    pres2 = get_keydata(data_amedas2[key_max2]["pressure"])

    wind2 = get_keydata(data_amedas2[key_max2]["wind"])
    windir2 = get_keydata(data_amedas2[key_max2]["windDirection"])
    windir2 = get_Dir(int(windir2), "en")

    # 3.Debug
    ## Debug - forcast
    print(f"天気予報 : 三重県北中部地方({area}/{area_detail})")
    print(f"")
    print(dt_today.strftime('%Y年%m月%d日'))
    print(f"今日の天気 : {wt_today}")
    print(f"今日{wcode_today} - 明日{wcode_tomorrow} - 明後日{wcode_dayaftertomorrow}")

    ## Debug - amedas
    print(f"    {temp}Cdeg / {humi}% / {windir}の風 {wind}mps")
    print(f"    1時間日射量 : {sun1h} / 前1時間降水量 : {prcp1h} mm")
    print(f"")
    print(f"    {temp2}Cdeg / {humi2}% / {pres2}hPa / {windir2}の風 {wind2}mps")
    print(f"")

    print(dt_tomorrow.strftime('%Y年%m月%d日'))
    print(f"明日の天気 : {wt_tomorrow}")
    print(f"")

    print(dt_dayaftertomorrow.strftime('%Y年%m月%d日'))
    print(f"明後日の天気 : {wt_dayaftertomorrow}")
    print(f"")

    # 4. LCD Display
    if (argc == 2):
      lcd_string(katakana(argv[1].decode('utf-8')),LCD_LINE_1)
    elif (argc == 3):
      lcd_string(katakana(argv[1].decode('utf-8')),LCD_LINE_1)
      lcd_string(katakana(argv[2].decode('utf-8')),LCD_LINE_2)
    else:
      lcd_clear()
      lcd_string_kana(u"アメダス　/　カメヤマ", LCD_LINE_1)
      lcd_string_kana(u"オンド　"+temp+u"Cdeg", LCD_LINE_2)
      time.sleep(5)

      lcd_clear()
      lcd_string_kana(u"シツド　"+humi+u"%RH", LCD_LINE_1)
      lcd_string_kana(u"フウソク　"+wind+u"m/s　"+windir, LCD_LINE_2)
      time.sleep(5)

      lcd_clear()
      lcd_string_kana(u"ニッシャリョウ　"+sun1h, LCD_LINE_1)
      lcd_string_kana(u"コウスイリョウ　"+prcp1h+"  mm", LCD_LINE_2)
      time.sleep(5)

      lcd_clear()
      lcd_string_kana(u"テンキヨホウ1　/　カメヤマ", LCD_LINE_1)
      lcd_string_kana("キョウ" + wcode_today + "　アス" + wcode_tomorrow, LCD_LINE_2)
      time.sleep(5)

      lcd_clear()
      lcd_string_kana(u"テンキヨホウ2　/　カメヤマ", LCD_LINE_1)
      lcd_string_kana("アス" + wcode_tomorrow + "　アサッテ" + wcode_dayaftertomorrow, LCD_LINE_2)
      time.sleep(5)

      lcd_clear()
      lcd_string_kana(u"アメダス　/　ツ", LCD_LINE_1)
      lcd_string_kana(u"オンド　"+temp2+"Cdeg", LCD_LINE_2)
      time.sleep(5)

      lcd_clear()
      lcd_string_kana(u"シツド　"+humi2+"%RH", LCD_LINE_1)
      lcd_string_kana(u"フウソク　"+wind2+u"m/s　"+windir2, LCD_LINE_2)
      time.sleep(5)

      lcd_clear()
      lcd_string_kana(u"キアツ　"+pres2+"hPa", LCD_LINE_1)
      time.sleep(5)

      lcd_clear()
      lcd_string_kana(u"キショウチョウカンソクデータ", LCD_LINE_1)
      lcd_string("Python/Raspberry", LCD_LINE_2)
      time.sleep(3)
      lcd_string("ython/RaspberryP", LCD_LINE_2)
      time.sleep(3)
      lcd_string("thon/RaspberryPi", LCD_LINE_2)
      time.sleep(4)

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)

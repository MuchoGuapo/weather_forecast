import time
import smbus

# LCD Inheret Param
I2C_ADDR  = 0x27
LCD_WIDTH = 16

# LCD Constants
LCD_CHR = 1
LCD_CMD = 0

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
#LCD_LINE_3 = 0x94
#LCD_LINE_4 = 0xD4

LCD_BACKLIGHT = 0x08
#LCD_BACKLIGHT = 0x00

ENABLE = 0b00000100

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# I2C
bus = smbus.SMBus(1)

# LCD Display Functions
# Refer: http://osoyoo.com/driver/i2clcda.py
def lcd_init():
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  message = message.ljust(LCD_WIDTH," ")
  lcd_byte(line, LCD_CMD)
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def lcd_clear():
  lcd_string("                ", LCD_LINE_1)
  lcd_string("                ", LCD_LINE_2)

# LCD1602 KATAKANA(カタカナ) Display Function
# Refer: https://ppdr.softether.net/osoyoo-i2c1602lcd
def lcd_string_kana(message,line):
  codes = u'線線線線線線線線線線線線線線線線　　　　　　　　　　　　　　　　!"#$%&`()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}→←　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　。「」、・ヲァィゥェォャュョッーアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワン゛゜αäβεμσρq√陰ι×￠￡nöpqθ∞ΩüΣπxν千万円÷　塗'
  dic ={u'ガ':u'カ゛',u'ギ':u'キ゛',u'グ':u'ク゛',u'ゲ':u'ケ゛',u'ゴ':u'コ゛',u'ザ':u'サ゛',u'ジ':u'シ゛',u'ズ':u'ス゛',u'ゼ':u'セ゛',u'ゾ':u'ソ゛',u'ダ':u'タ゛',u'ヂ':u'チ゛',u'ヅ':u'ツ゛',u'デ':u'テ゛',u'ド':u'ト゛',u'バ':u'ハ゛',u'ビ':u'ヒ゛',u'ブ':u'フ゛',u'ベ':u'ヘ゛',u'ボ':u'ホ゛',u'パ':u'ハ゜',u'ピ':u'ヒ゜',u'プ':u'フ゜',u'ペ':u'ヘ゜',u'ポ':u'ホ゜',u'℃':u'゜C'}

  message = message.ljust(LCD_WIDTH," ")
  lcd_byte(line, LCD_CMD)

  message2 = ""
  for i in range(LCD_WIDTH):
    if ( message[i] in dic.keys() ):
      message2 += dic[message[i]]
    else:
      message2 += message[i]

  for i in range(LCD_WIDTH):
    if (codes.find(message2[i]) >= 0):
      lcd_byte(codes.find(message2[i])+1,LCD_CHR)
    elif (message2[i] != u' '):
      print("No such character!    :" + message2[i])

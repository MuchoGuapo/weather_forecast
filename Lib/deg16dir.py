# transferring Degree to 16-Direction 
# Refer: https://qiita.com/Yoshiki443/items/6a4682bebdf87bd82cff

# definition of 16 Direction(風向)
dir_jp = {16:"北", 1:"北北東", 2:"北東", 3:"東北東", 4:"東", 5:"東南東", 6:"南東", 7:"南南東", 8:"南", 9:"南南西", 10:"南西", 11:"西南西", 12:"西", 13:"西北西", 14:"北西", 15:"北北西", 0:"不定"}
dir_en = {16:"North", 1:"NNE", 2:"NE", 3:"NEE", 4:"East", 5:"SEE", 6:"SE", 7:"SSE", 8:"South", 9:"SSW", 10:"SW", 11:"SWW", 12:"West", 13:"NWW", 14:"NW", 15:"NNW", 0:"VRB"}

# func of transfering WindDirection(Jp, En)
def get_Dir(windir, lang) -> str:
  if ((lang == "jp") or (lang == "ja")):
    mtx_dir = dir_jp
  else:
    mtx_dir = dir_en

  if windir in mtx_dir:
    direction = mtx_dir[windir]
  else:
    print("Error in direction")
    direction = ""
  return direction

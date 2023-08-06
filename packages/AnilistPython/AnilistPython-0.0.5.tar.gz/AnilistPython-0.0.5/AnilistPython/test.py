from __init__ import Anilist
driverObj = Anilist()

info = driverObj.getCharacterInfo("mia luna")
print(info)
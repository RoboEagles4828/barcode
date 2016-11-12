import barcodebrain

ROSTER = "roster.csv"

fileName = barcodebrain.getid()
barcodebrain.idconvert(ROSTER, fileName)
barcodebrain.findtimediffs(fileName)

import barcodebrain

ROSTER = "roster.csv"

fileName = barcodebrain.getid(ROSTER)
barcodebrain.findtimediffs(fileName)

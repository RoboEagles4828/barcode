import barcodebrain
import os

if not os.path.exists("attendance"):
        os.makedirs("attendance")

ROSTER = "roster.csv"

fileName = barcodebrain.getid(ROSTER)
barcodebrain.findtimediffs(fileName)

# imports
import tkinter
import random
import sys
from tkinter import messagebox

# Variables
gameName = "Save earth from global mining! 2"
size = 32
numberOfMines = int(round(size**2 * 0.1))
flagsLeft = 0
tiles = []
flagging = False
width = int(size*24)
height = int(size*26)
windowGeometry = str(width) + "x" + str( height)

# tkinter init
window = tkinter.Tk()
window.title(gameName)
window.resizable(width=False, height=False)
window.geometry(windowGeometry)

window2 = tkinter.Tk()
window2.title(gameName)
window2.resizable(width=False, height=False)
window2.geometry("240x80")


# Get the coordinates of adjecent tiles
def getAdjacentCoordinateList(x,y):
	indexes = [	{"x":x+1,"y":y  },#
				{"x":x-1,"y":y  },
				{"x":x  ,"y":y+1},#
				{"x":x  ,"y":y-1},
				{"x":x+1,"y":y+1},#
				{"x":x-1,"y":y-1},
				{"x":x-1,"y":y+1},
				{"x":x+1,"y":y-1}
				]
	temp = []

	for	index in indexes:
		if (index["x"] <= size-1) and (index["x"] >= 0) and (index["y"] <= size-1) and(index["y"] >= 0):
			temp.append(index)

	return temp
# Gets index of tile from list with matching coordinates
def findTileIndexWithCoordinates(tileList, x, y):
	for i in range(len(tileList)):
		if tileList[i]["x"] == x and tileList[i]["y"] == y:
			return i
	return None
# Gets tile from list with matching coordinates
def findTileWithCoordinates(tileList, x, y):
	for i in range(len(tileList)):
		if tileList[i]["x"] == x and tileList[i]["y"] == y:
			return tileList[i]
	return None
# Callback from button click
def CheckTile(index):
	global flagsLeft
	if flagging == True:
		if tiles[index]["flagged"]:
			flagsLeft += 1
		else:
			flagsLeft -= 1
		flagLabel["text"] = str(flagsLeft) + " flags left"
		tiles[index]["flagged"] = not tiles[index]["flagged"]
	elif tiles[index]["flagged"] == False:
		tiles[index]["checked"] = True
		if tiles[index]["isBomb"] == True:
			LostGame()
		elif tiles[index]["ab"] == 0:
			tempa = getAdjacentCoordinateList(tiles[index]["x"], tiles[index]["y"])
			for x in range(len(tempa)):
				if findTileWithCoordinates(tiles, tempa[x]["x"], tempa[x]["y"])["checked"] != True:
					CheckTile(findTileIndexWithCoordinates(tiles, tempa[x]["x"], tempa[x]["y"]))
	updateTile(tiles[index])	
# 
def changeFlaggedState():
	global flagging 
	flagging = not flagging
	if flagging == True:
		flaggingButton["bg"] = "red"
	else:
		flaggingButton["bg"] = "#F0F0F0"
# Update tile appearance
def updateTile(tile):
	if tile["checked"] == False:
		tile["button"]["bg"] = "#84C343"
		if tile["flagged"] == True:
			tile["button"]["fg"] = "black"
			tile["button"]["bg"] = "red" 
			tile["button"]["text"] = u"\u2691"
		else:
			tile["button"]["text"] = ""
			tile["button"]["fg"] = "black"
	else:
		tile["button"]["bg"] = "#7CC0D9"
		if tile["isBomb"]:
			tile["button"]["fg"] = "red"
			tile["button"]["text"] = "¤"
			tile["button"]["bg"] = "black"
		else:
			if tile["ab"] > 0:
				tile["button"]["fg"] = "black"
				tile["button"]["text"] = tile["ab"]
			else:
				tile["button"]["bg"] = "#437EC3" 
# Resets all tiles
def ResetGame():
	for tile in tiles:
		tile["isBomb"] = False
		tile["checked"] = False
		tile["ab"] = 0
		tile["flagged"] = False
		updateTile(tile)
	InitializeTiles()
# Pop
def WonGame():
	for tile in tiles:
		if tile["isBomb"] == True:
			tile["checked"] = True
			updateTile(tile)
	messagebox.showinfo(gameName, "You Won! get a life...")
	ResetGame()
#
def LostGame():
	for tile in tiles:
		if tile["isBomb"] == True:
			tile["checked"] = True
			updateTile(tile)
	messagebox.showinfo(gameName, "You lost scrub")
	ResetGame()
#
def InitializeTiles():
	global tiles
	global flagsLeft 
	
	flagsLeft = numberOfMines
	flagLabel["text"] = str(flagsLeft) + " flags left"
	# Place bombs
	for i in range(numberOfMines):
		num = random.randint(0, len(tiles)-1)
		tiles[num]["isBomb"] = True

	# Change Adjacent bombs
	for tile in tiles:
		if tile["isBomb"] == True:
			tempa = getAdjacentCoordinateList(tile["x"], tile["y"])
			for x in range(len(tempa)):
				findTileWithCoordinates(tiles, tempa[x]["x"], tempa[x]["y"])["ab"] += 1

flaggingButton = tkinter.Button(window2,text=u"\u2691", width = 16, height = 4, command=changeFlaggedState)
flagLabel = tkinter.Label(window2, text = str(flagsLeft) + " flags left")
flagLabel.pack()
flaggingButton.pack()

# Create tiles
for x in range(size):
	for y in range(size):
		tempTile = {}
		tempTile["ID"] = len(tiles)
		tempTile["x"] = x
		tempTile["y"] = y
		tempTile["isBomb"] = False
		tempTile["ab"] = 0
		tempTile["checked"] = False
		tempTile["flagged"] = False
		tempTile["button"] = tkinter.Button(window, width = 2, height = 1, background= "#84C343", command = lambda index = tempTile["ID"]: CheckTile(index))
		tempTile["button"].grid(column = x, row = y) 
		tiles.append(tempTile)

InitializeTiles()
window.mainloop()
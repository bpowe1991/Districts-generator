""""
Programmer: Briton A. Powe          Program Homework Assignment #4
Date: 2/14/18                       Class: Introduction to the Software Profession
Version: 1.3.2
------------------------------------------------------------------------
Program Description:
Creates a graphics window and outputs results of 5 by 5 election grid.
Each result is output to the window and closes when all elections have been read.
The input file is called districts.txt. It has a specific format given by Professor Miller.
***This program uses the graphics.py library created by John Zelle***
***This program follows the read input file method given by Professor Miller on 2/12/18***

Sources:
Some parts are borrowed and redesigned from HW2Powe.py
For basic syntax - https://www.tutorialspoint.com/python/index.htm
For continue button action - https://stackoverflow.com/questions/39867464/adding-button-to-python-graphics-py-window
For color reference - http://cng.seas.rochester.edu/CNG/docs/x11color.html
Documentation for graphics.py - https://www.math.uci.edu/icamp/computing/python/zellegraphics.pdf
Reference guide for using graphics.py - https://twu.seanho.com/09fall/cmpt140/lectures/33-graphics.pdf
"""
#The graphics.py library by John Zelle is used to create the graphics
from graphics import *
import re

#Opening input file by the name districts.txt with specific format. Storing in string
inputFile = open("districts.txt")
readFile = str(inputFile.read())

#Removing newline character from readFile variable
fileElements = re.findall(r"[\w']+", readFile)

#List to hold every election district and list to hold counted votes
districtList = []
talliedVotes = []

#Dictionary to apply color to the 5 districts
districtColorMap = {1:"RoyalBlue",
                    2:"Red",
                    3:"Orange",
                    4:"Gold",
                    5:"ForestGreen"}

#List that holds the placement of voters
voters = ["P","G","G","G","G",
          "G","P","P","P","G",
          "G","P","G","G","G",
          "G","G","G","P","P",
          "P","G","P","G","P"]

#Function to fill districtList for every election
def getDistricts():
    count = 0
    district = []

    #Reading each character from input file to split up each election
    for element in fileElements:

        #'C' is the delimiter between elections
        if(element == 'C' or count == 25):
            districtList.append(district)
            district = []
            count = 0

        #'D' is the delimiter for the end of the file or elections that are considered
        elif(element == 'D'):
            break
        else:
            district.append(int(element))
            count+= 1

#Function to print matrix to graphics window
def printMatrix():
    for z in range(0,5):
        for i in range(0,5):
            x=i*60+25
            y=z*30+55
            x2=x+60
            y2=y+30

            #Creating and Printing each cell
            cell = Rectangle(Point(x, y), Point(x2, y2))
            cell.setFill(districtColorMap[districtList[currentElection][((z * 5) + i)]])
            cell.draw(win)

            #Labeling each cell with designated voter from voters list
            voter = Text(cell.getCenter(), voters[((z * 5) + i)])
            voter.draw(win)

#Function to create legend in graphics window
def printLengend():
    legend = Rectangle(Point(360,55), Point(445, 150))
    legend.setFill("White")
    legend.setOutline("Black")
    legend.draw(win)

    #Printing each label in legend
    for q in range(0,5):
        districtLegend = Rectangle(Point(370,65+q*15), Point(380,75+q*15))
        districtLegend.setFill(districtColorMap[q+1])
        districtLegend.draw(win)
        districtLabel = Text(Point(410,70+q*15), str("- District "+str(q+1)))
        districtLabel.draw(win)


#Function to count votes for each district in an election
def tallyVotes(voterCount):
    voterCount = [[0,0],[0,0],[0,0],[0,0],[0,0]]

    for p in range(0,len(voters)):
        if (voters[p] == "G"):
            voterCount[(districtList[currentElection][p]) - 1][0] += 1
        else:
            voterCount[(districtList[currentElection][p]) - 1][1] += 1

    #Return list to be used in main section of program
    return voterCount


#Function to calculate results from talliedVotes list
def calculateResults(votes):

    #Variables to keep track of results
    greenDistrictVictory = 0
    purpleDistrictVictory = 0
    greenWinBy5 = 0
    greenWinBy4 = 0
    greenWinBy3 = 0
    purpleWinBy5 = 0
    purpleWinBy4 = 0
    purpleWinBy3 = 0
    winner = ""

    for c in range(len(votes)):
        if votes[c][0] > votes[c][1]:
            greenDistrictVictory += 1
            if votes[c][0] == 5:
                greenWinBy5 += 1
            elif votes[c][0] == 4:
                greenWinBy4 += 1
            elif votes[c][0] == 3:
                greenWinBy3 += 1
        else:
            purpleDistrictVictory += 1
            if votes[c][1] == 5:
                purpleWinBy5 += 1
            elif votes[c][1] == 4:
                purpleWinBy4 += 1
            elif votes[c][1] == 3:
                purpleWinBy3 += 1

    if greenDistrictVictory > purpleDistrictVictory:
        winner = "Green"
    else:
        winner = "Purple"

    #Constructing string for finished results
    results = str("Election Results: \n\n"+
                  "Green Districts Won: "+str(greenDistrictVictory)+"\t\t"+
                  "    Purple Districts Won: "+str(purpleDistrictVictory)+"\n\n"+
                  "Green Win 5 to 0: "+str(greenWinBy5)+"\t\t"+
                  "Purple Win 5 to 0: " + str(purpleWinBy5) + "\n" +
                  "Green Win 4 to 1: " + str(greenWinBy4) + "\t\t" +
                  "Purple Win 4 to 1: " + str(purpleWinBy4) + "\n" +
                  "Green Win 3 to 2: " + str(greenWinBy3) + "\t\t" +
                  "Purple Win 3 to 2: " + str(purpleWinBy3) + "\n\n" +
                  "Election Winner: "+str(winner))

    return results


#Function for clicking conintue button
def inside(point, button, currentElection):
    bottomLeftCorner = button.getP1()
    topRightCorner = button.getP2()

    return bottomLeftCorner.getX() < point.getX() < topRightCorner.getX() and \
           bottomLeftCorner.getY() < point.getY() < topRightCorner.getY()

#Create window for graphics
win = GraphWin("Results", 470, 450, autoflush=False)
win.setBackground("Cornsilk")

#Setting Districts
getDistricts()

#Main loop for reading through every election
for currentElection in range(len(districtList)):

    #Setting header for election result window
    title = Text(Point(235, 25), str("Election Scheme - " + str(currentElection + 1)))
    title.setOutline("Black")
    title.setStyle("bold")
    title.draw(win)

    #Print matrix to graphics window
    printMatrix()
    printLengend()

    talliedVotes = tallyVotes(talliedVotes)

    #Creating border for election results
    border = Rectangle(Point(25,230), Point(445,380))
    border.setFill("LemonChiffon")
    border.setOutline("Black")
    border.draw(win)

    #Output results to graphics window
    resultText = Text(Point(240, 305), calculateResults(talliedVotes))
    resultText.draw(win)

    #Create Countinue button for next election
    continueButton = Rectangle(Point(200, 395), Point(270, 430))
    continueButton.setFill("Wheat")
    continueButton.draw(win)
    quitButtonLabel = Text(continueButton.getCenter(), "Continue")
    quitButtonLabel.draw(win)

    #Loop to keep window open until Continue button is pressed
    while True:
        clickPoint = win.getMouse()

        if inside(clickPoint, continueButton, currentElection):

            #Clear graphics window for next election output
            for element in win.items[:]:
                element.undraw()
            win.update()
            break
        else:
            continue

inputFile.close()

#Message to console for program ending
print("End of Program")
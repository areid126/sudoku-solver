# Read in the sudoku from the file
import sys
import math

# Define constant values for the instance variable
ROW = 0
COLUMN = 1
BOX = 2

# Get the name of the file to read in from the commandline
fileName = "input.csv" # Default input file name
if(len(sys.argv) > 1):
    fileName = sys.argv[1]

# Read in the file
lines = [] # Array to read the file into
try:
    file = open(fileName, "r")
    lines = file.readlines() # Gets an array of the whole file
except:
    print("Error: could not read file", fileName)
    sys.exit()

grid = [] # Array to store the read in board

# Process the input file
for line in lines:
    parts = line.split(",") # Split the line into parts

    row = []
    # Read the parts into the array
    for part in parts:
        if(part.isdigit()):
            row.append(int(part))
        elif(part == ""):
            row.append(" ") # Use ' ' to represent empty cells
        elif(part != "\n"): # Do nothing if it is the end of the line
            print("Invalid input format")

    grid.append(row)

# Print the sudoku from the grid array
def makeBoardPrinter():
    outerBar = '+===========+===========+===========+\n'
    innerBar = '+ -- --- -- + -- --- -- + -- --- -- +\n'
    innerLine = '|' +((' {:} :')* 2 + ' {:} |')*3 + '\n'
    boardFormat = outerBar + ((innerLine + innerBar)*2 + innerLine + outerBar)*3
    return (lambda board:print(boardFormat.format(*(cell for row in board for cell in row))))

# Set up the candidates for a specific cell
def getCandidates(row, column):
    # If the cell has a value in it do nothing
    if(grid[row][column] != " "):
        return [False] * 9 # There are no candidates for this cell, as it is already full
    
    
    # Set all candidates to be true and then eliminate the ones that are not
    curCandidates = [True] * 9

    # Check the row and column the cell is in
    for i in range(9):

        # Eliminate any numbers already in the row
        if (grid[i][column] != " "):
            curCandidates[grid[i][column] - 1] = False

        # Eliminate any numbers already in the column
        if (grid[row][i] != " "):
            curCandidates[grid[row][i] - 1] = False


    # Get the box the cell is in
    boxColumn = math.floor(column/3)
    boxRow = math.floor(row/3)

    # Check the box the cell is in
    for i in range(3):
        for j in range(3):

            # Remove any candidates that are in the same box as the cell
            if (grid[(boxRow*3) + i][(boxColumn*3) + j] != " "):
                curCandidates[grid[(boxRow*3) + i][(boxColumn*3) + j] - 1] = False


    # Return the completed candidate list
    return curCandidates

# Set up the initial candidates for the whole grid
def setUpCandidates():
    candidates = []

    for i in range(9):
        row = []

        for j in range(9):
            row.append(getCandidates(i, j))

        # Add the row to the candidate array
        candidates.append(row)

    return candidates

# Print all the candidates for each cell
def printCandidates():

    for i in range(9):
        for j in range(9):
            line = ""
            for k in range(9):
                if(candidates[i][j][k] == True):
                    line += str(k+1) + " "
            
            print(f"[{i}, {j}]: " + line)

# Function for filling cells with only one candidate
def onlyOneCandidate(byStep=False):
    updated = False

    for i in range(9):
        for j in range(9):

            # Continue if there is already a value in the cell
            if (grid[i][j] != " "):
                continue

            NO_CANDIDATE = 10 # represents there being no candidate

            first = NO_CANDIDATE # The first valid candidate for the cell
            last = NO_CANDIDATE # The last valid candidate for the cell

            for k in range(9):
                if(candidates[i][j][k] == True):
                    # If it is the first candidate mark it
                    if (first == NO_CANDIDATE):
                        first = k + 1
                    
                    # Update the last found candidate
                    last = k + 1
            
            # If the first and last candidate are the same then there is only one candidate
            if (first != NO_CANDIDATE and first == last):
                # Set the field in the grid
                grid[i][j] = first
                updateCandidates(i, j) # Update the candidates
                updated = True

                # If going step by step return
                if (byStep):
                    return True
                
    return updated
                
# Function for filling cells where the candidate can only go in that cell
def onlyOneCell(byStep=False):
    updated = False

    # Go number by number looking for places the number can be inserted
    for toFind in range(9):

        # Loop through every column and row, looking for the value as a candidate
        for i in range(9):

            colCount = 0
            rowCount = 0
            colFound = -1
            rowFound = -1

            for j in range(9):

                # If it already appears in the row or the column, set the count to be large
                if (grid[i][j] == toFind + 1):
                    rowCount = 10

                if (grid[j][i] == toFind + 1):
                    colCount = 10

                # Check if it is a candidate for the cell in the column
                if (grid[i][j] == " " and candidates[i][j][toFind]):
                    rowCount += 1
                    rowFound = j
                
                # Check if it is a condidate for the cell in the column
                if (grid[j][i] == " " and candidates[j][i][toFind]):
                    colCount += 1
                    colFound = j


            # If it was found exactly once as a candidate in the row then assign it
            if (rowCount == 1):
                grid[i][rowFound] = toFind + 1
                updateCandidates(i, rowFound)
                updated = True


                if (byStep):
                    return True


            # If it was found exactly once as a candidate in the column then assign it
            if (colCount == 1):
                grid[colFound][i] = toFind + 1
                updateCandidates(colFound, i)
                updated = True

                if (byStep):
                    return True
        
        # Loop through every cell looking for it
        for i in range(3):
            for j in range(3):

                boxCount = 0
                boxFoundCol = -1
                boxFoundRow = -1

                for k in range(3):
                    for t in range(3):

                        if (grid[(i*3) + k][(j*3) + t] == toFind + 1):
                            boxCount = 10

                        # Check if it is a candidate for the cell in the column
                        if (grid[(i*3) + k][(j*3) + t] == " " and candidates[(i*3) + k][(j*3) + t][toFind]):
                            boxCount += 1
                            boxFoundRow = (i*3) + k
                            boxFoundCol = (j*3) + t


                if (boxCount == 1):
                    grid[boxFoundRow][boxFoundCol] = toFind + 1
                    updateCandidates(boxFoundRow, boxFoundCol)
                    updated = True

                    if (byStep):
                        return True
                    
    return updated

# Function for updating the candidates after filling a cell
def updateCandidates(row, column):
    value = grid[row][column]
    # Update the candidates for the current cell (as it can no longer be anything)
    candidates[row][column] = [False]*9

    # Remove all the candidates in the row and column
    for i in range(9):
        candidates[row][i][value - 1] = False
        candidates[i][column][value - 1] = False
    
    # Get the box the cell is in
    boxColumn = math.floor(column/3)
    boxRow = math.floor(row/3)

    # Check the box the cell is in
    for i in range(3):
        for j in range(3):

            candidates[(boxRow*3) + i][(boxColumn*3) + j][value - 1] = False

# Function to output the results to a file (which can then be checked for debugging)
def outputGrid():
    # Construct one long string
    output = ""
    for i in range(9):
        for j in range(9):

            if(grid[i][j] != " "):
                output += str(grid[i][j]) + ","

            # If there is no value then print all the candidates instead
            else:
                output += "("

                for k in range(9):
                    if (candidates[i][j][k]):
                        output += str(k + 1) + ":"

                output += "),"


        output += "\n"

    # Print that string to a file
    with open("output.csv", "w") as f:
        f.write(output)

def hiddenPairs(instance, byStep=False):

    # Exit if the function is not called for a valid instance
    if instance != ROW and instance != COLUMN and instance != BOX:
        return False

    # Loop through every box/row/column
    for i in range(9):

        # The list of all possible combinations of candidates in the box/row/column
        combinations = []
        # Set the first index to be the index of no candidates
        combinations.append({
            "candidates": 0,    # The number of candidates being counted in
            "cells": [False]*9  # The number of cells that list of candidates appears in
            }) 
        
        # Whether a hidden pair has been found in this box (initially false)
        found = False

        # Loop through all the possible candidates
        for j in range(9):
            
            # If a pair has already been found in this box/row/column then break
            if found:
                break

            currentCells = [False]*9

            # Get the cells this candidate appears in
            for k in range(9):

                # If the current value appears as a candidate in a cell and the cell is empty then log it
                if isCandidate(i, j, k, instance):
                    currentCells[k] = True

                # If the current candidate appears as a value in the cell then make it a candidate for all cells (which will stop it from being part of a hidden pair)
                if getValue(i, k, instance) == j+1:
                    currentCells = [True]*9
                    break

            print(currentCells)

            # Loop through every possible combination of candidates (that is all all indexes < 2^j)
            for k in range(int(math.pow(2, j))):

                # Get the current combination
                currentCombination = combinations[k]
                # Create a new combination to store the currnet combenation plus the current cell
                newCombination = [False]*9 
                # Get the cells that this combination of candidates appears in
                cellCount = getNewCombination(currentCombination, currentCells, newCombination)

                # Store this information in the correct index
                combinations.append({"candidates": currentCombination["candidates"] + 1, "cells": newCombination}) 
                
                # Check if a hidden pair has been identified
                # This means there are the same number of combined possible cells for the candidates as there are candidates
                if(currentCombination["candidates"] + 1 == cellCount and cellCount > 0):

                    # Reveal the hidden pair
                    revealHiddenPair(i, newCombination, k+math.pow(2, j), instance)

                    # Update the found value to indicate a hidden pair has been found
                    found = True
                    
                    # Exit if going by step
                    if byStep:
                        return True
                    
                    # Exit the loop as all cached information will now be incorrect
                    break 
    
    # Return whether a candidate was found
    return found

def revealHiddenPair(i, newCombination, candidateIndex, instance):
    currentCandidates = getCandidatesFromIndex(candidateIndex)

    # Loop through all the cells in the box/row/column again (the box/column/row is 'i')
    for t in range(9):

        # If the cell is in the pair
        if (newCombination[t]):

            # Remove all the candidates that are not in the pair
            for s in range(9):
                if(not currentCandidates[s]):

                    # Handle removing candidates from the row
                    if instance == ROW:
                        candidates[i][t][s] = False
                    # Handle removing candidates from the column
                    if instance == COLUMN:
                        candidates[t][i][s] = False
                    # Handle removing candidates from the box
                    if instance == BOX:
                        candidates[getCellRow(i, t)][getCellColumn(i, t)][s] = False

def isCandidate(i, j, k, instance):
    # Get if the cell contains the candidate when checking for a box
    candidate = candidates[getCellRow(i, k)][getCellColumn(i, k)][j] and grid[getCellRow(i, k)][getCellColumn(i, k)] == " " and instance == BOX
    # Get if the cell contains the candidate when checking for a row
    candidate = candidate or (candidates[i][k][j] and grid[i][k] == " " and instance == ROW)
    # Get if the cell contains the candidate when checking for a column
    candidate = candidate or (candidates[k][i][j] and grid[k][i] == " " and instance == COLUMN)

    return candidate

def getValue(i, k, instance):
    # Get the current candidate of the cell
    value = " "
    if instance == ROW: # If checking a row
        value = grid[i][k]
    if instance == COLUMN: # If checking a column
        value = grid[k][i]
    if instance == BOX: # If checking a box
        value = grid[getCellRow(i, k)][getCellColumn(i, k)]

    return value

def getNewCombination(currentCombination, currentCells, newCombination):

    # Count the number of possible cells the candidate can appear in
    cellCount = 0

    # Create the new combination by looping through every cell
    for t in range(9):

        # If the cell is contained in either the old combination or the current candidate list then set it to true
        newCombination[t] = currentCombination["cells"][t] or currentCells[t]

        # If a cell is in the combination then add to the count of all cells in the combination
        if newCombination[t]:
            cellCount += 1

    return cellCount

# Function for identifying naked pairs within boxes
def nakedPairs():

    # Loop through every box
    for i in range(9):

        # The list of all possible combinations of cells in the box
        combinations = []
        # Set the first index to be the index of no cells
        combinations.append({
            "cells": 0,             # How many cells are in the combination
            "candidates": [False]*9 # Whether a candidate is present in the combination of cells
            }) 
        
        # Whether a naked pair has been found in this box (initially false)
        found = False

        # Loop through all the cells in the box
        for j in range(9):
            
            # If a value has already been found in this box then break
            if found:
                break

            # Loop through every possible combination of cells (that is all all indexes < 2^j)
            for k in range(int(math.pow(2, j))):

                # Get the current combination of cells
                currentCombination = combinations[k]
                # Create a new combination to store the current combination and the current cell
                newCombination = [False]*9 
                # Couter to count the number of candidates there are between all the cells in the combination
                candidateCount = 0

                # Create the new combination
                for t in range(9):
                    # If the cell already has a value, then make all the candidates true to avoid adding it to a hidden pair
                    newCombination[t] = currentCombination["candidates"][t] or candidates[getCellRow(i, j)][getCellColumn(i, j)][t] or grid[getCellRow(i, j)][getCellColumn(i, j)] != " "
                    
                    # Count the number of candidates in the combination of cells
                    if newCombination[t]:
                        candidateCount += 1

                # Store this information in the correct index
                combinations.append({"cells": currentCombination["cells"] + 1, "candidates": newCombination}) 
                
                # Check if a pair has been identified (A pair means there are the same number of candidates for cells as there are cells)
                if(currentCombination["cells"] + 1 == candidateCount and candidateCount > 0):

                    print("Identified a naked pair")

                    # If a pair has been identified them remove all the candidates in the combination of cells from all other cells
                    currentCells = getCandidatesFromIndex(k+math.pow(2, j))

                    # Loop through all the cells in the box again
                    for t in range(9):

                        # If the cell is not in the pair
                        if (not currentCells[t]):

                            # Remove all the candidates that are in the pair
                            for s in range(9):
                                if(newCombination[s]):
                                    candidates[getCellRow(i, t)][getCellColumn(i, t)][s] = False


                    # Indicate that a pair has been found
                    found = True
                    break

    # Return if something was found
    return found

def getIndexFromCandidates(present):

    # If the list does not contain the correct number of elements then return -1 (to indicate error)
    if (len(present) != 9):
        return -1
    
    index = 0
    for i in range(9):

        # If the value is present then add to the index
        if(present[i]):
            index += math.pow(2, 8-i)

    return index

def getCandidatesFromIndex(index):

    # Return an empty list if the index is out of range
    if (index < 0 or index > 512):
        return []
    
    output = [False]*9

    # Construct the list of indexes by dividing by powers of 2
    for i in range(9)[::-1]:

        # If the index divides by the power of nine, update the index value and the output
        if(index >= math.pow(2, i)):
            index -= math.pow(2, i)
            output[i] = True # Update the value to be present in the array

    return output

# Function to turn a box and cell combination into indexes
def getCellRow(box, cell):

    boxRow = math.floor((box)/3)
    cellRow = math.floor((cell)/3)

    return (boxRow*3) + cellRow

def getCellColumn(box, cell):


    boxColumn = (box) % 3
    cellColumn = (cell) % 3

    return (boxColumn * 3) + cellColumn


# Make a printer for the board
printBoard = makeBoardPrinter()

# Print the board
printBoard(grid)

candidates = setUpCandidates()

# Output all the possible candidates
outputGrid()
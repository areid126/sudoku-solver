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

# Get if the user wants to solve the puzzle step by step
runByStep = False
if(len(sys.argv) > 2 and sys.argv[2] == "-s"):
    runByStep = True

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

# Function for filling in candidates that only appear in one cell   
def onlyOneCell(byStep=False):
    updated = False

    # Loop through every candidate to see if there is somewhere it can be inserted
    for toFind in range(9):

        # Loop through every column/row/box, looking for the value as a candidate
        for i in range(9):
            count = [0]*3
            found = [-1]*3

            # Loop through every cell in the column/row/box
            for j in range(9):
                
                # If the value already exists in the row, set the count to a number higher than 1
                if (grid[i][j] == toFind + 1):
                    count[ROW] = 10

                if (grid[j][i] == toFind + 1):
                    count[COLUMN] = 10

                if (grid[getCellRow(i, j)][getCellColumn(i, j)] == toFind + 1):
                    count[BOX] = 10

                # Check if it is a candidate in the column/box/row
                if (grid[i][j] == " " and candidates[i][j][toFind]):
                    count[ROW] += 1
                    found[ROW] = j
                
                if (grid[j][i] == " " and candidates[j][i][toFind]):
                    count[COLUMN] += 1
                    found[COLUMN] = j

                if (grid[getCellRow(i, j)][getCellColumn(i, j)] == " " and candidates[getCellRow(i, j)][getCellColumn(i, j)][toFind]):
                    count[BOX] += 1
                    found[BOX] = j


            # If it was found exactly once as a candidate in the row then assign it
            if (count[ROW] == 1):
                grid[i][found[ROW]] = toFind + 1
                updateCandidates(i, found[ROW])
                updated = True

                if (byStep):
                    return True

            # If it was found exactly once as a candidate in the column then assign it
            if (count[COLUMN] == 1):
                grid[found[COLUMN]][i] = toFind + 1
                updateCandidates(found[COLUMN], i)
                updated = True

                if (byStep):
                    return True
                
            # If it was found exactly once as a candidate in the box then assign it
            if (count[BOX] == 1):
                grid[getCellRow(i, found[BOX])][getCellColumn(i, found[BOX])] = toFind + 1
                updateCandidates(getCellRow(i, found[BOX]), getCellColumn(i, found[BOX]))
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

# Function for identifying hidden pairs
def hiddenPairs(instance, byStep=False):

    # Exit if the function is not called for a valid instance
    if instance != ROW and instance != COLUMN and instance != BOX:
        return False
    
    updated = False

    # Loop through every box/row/column
    for i in range(9):

        # The list of all possible combinations of candidates in the box/row/column
        combinations = []
        # Set the first index to be the index of no candidates
        combinations.append({
            "candidates": 0,    # The number of candidates being counted in
            "cells": [False]*9  # The number of cells that list of candidates appears in
            }) 
        
        # Count how many empty cells there are
        empty = 0
        for j in range(9):
            if instance == ROW and grid[i][j] == " ":
                empty += 1
            if instance == COLUMN and grid[j][i] == " ":
                empty += 1
            if instance == BOX and grid[getCellRow(i, j)][getCellColumn(i, j)] == " ":
                empty += 1
        
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
                # Do not count a pair if it contains the same number of cells as there are empty cells
                if(currentCombination["candidates"] + 1 == cellCount and cellCount > 0 and cellCount < empty):

                    # Reveal the hidden pair 
                    # Only consider a pair to be found if the state of the board changes
                    if revealHiddenPair(i, newCombination, k+math.pow(2, j), instance):

                        found = True
                        updated = True
                        
                        # Exit if going by step
                        if byStep:
                            return True
                        
                        # Exit the loop as all cached information will now be incorrect
                        break 
    
    # Return whether a candidate was found
    return updated

# Returns true if the state of the board changed and false if not
def revealHiddenPair(i, newCombination, candidateIndex, instance):
    currentCandidates = getCandidatesFromIndex(candidateIndex)

    # Store whether anything changed
    updated = False

    # Loop through all the cells in the box/row/column again (the box/column/row is 'i')
    for t in range(9):

        # If the cell is in the pair
        if (newCombination[t]):

            # Remove all the candidates that are not in the pair
            for s in range(9):
                if(not currentCandidates[s]):

                    # Handle removing candidates from the row
                    if instance == ROW:
                        # If it has already been updated, or the current cell is true (and so will have its value updated)
                        updated = updated or candidates[i][t][s]
                        candidates[i][t][s] = False
                    # Handle removing candidates from the column
                    if instance == COLUMN:
                        # If it has already been updated, or the current cell is true (and so will have its value updated)
                        updated = updated or candidates[t][i][s]
                        candidates[t][i][s] = False
                    # Handle removing candidates from the box
                    if instance == BOX:
                        # If it has already been updated, or the current cell is true (and so will have its value updated)
                        updated = updated or candidates[getCellRow(i, t)][getCellColumn(i, t)][s]
                        candidates[getCellRow(i, t)][getCellColumn(i, t)][s] = False


    return updated

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

# Functions for backtracking to solve any sudoku
def checkValid():

    # Loop through every row/column/box
    for i in range(9):

        # Define a list of values that have appeared in that row/column/box
        rowValues = [False]*9
        columnValues = [False]*9
        boxValues = [False]*9


        # Loop through every cell in the row/column/box
        for j in range(9):
            
            # If there is a value in the row then mark it as true
            if grid[i][j] != " ":

                # If the value already exists in the row then return, otherwise mark it as being in the row
                if rowValues[grid[i][j] - 1]:
                    return False
                else:
                    rowValues[grid[i][j] - 1] = True

            # If there is a value in the column then mark it as true
            if grid[j][i] != " ":

                # If the value already exists in the column then return, otherwise mark it as being in the column
                if columnValues[grid[j][i] - 1]:
                    return False
                else:
                    columnValues[grid[j][i] - 1] = True

            # If there is a value in the box then mark it as true
            if grid[getCellRow(i, j)][getCellColumn(i, j)] != " ":

                # If the value already exists in the box then return, otherwise mark it as being in the box
                if boxValues[grid[getCellRow(i, j)][getCellColumn(i, j)] - 1]:
                    return False
                else:
                    boxValues[grid[getCellRow(i, j)][getCellColumn(i, j)] - 1] = True

    # If the loop exits then every row and column is valid, so the board is valid
    return True

# Function for checking if an addition is valid for a row/column
def checkValidCell(row, column):
    value = grid[row][column]
    if value == " ":
        return True # a blank cell is always valid
    
    # Get the box the cell is in
    box = math.floor(column/3) + (math.floor(row/3)*3)
    
    # Loop through the row/column/box
    for i in range(9):

        if grid[row][i] == value and i != column:
            return False
        
        if grid[i][column] == value and i != row:
            return False
        
        if grid[getCellRow(box, i)][getCellColumn(box, i)] == value and getCellRow(box, i) != row and getCellColumn(box, i) != column:
            return False
        
    # If the loop exits then the cell has a valid value
    return True
    
def backtrack():

    # Set up the grid to track guesses
    guesses = []
    for i in range(9):
        guesses.append([False]*9)
        
    # Begin the recursion
    return backtrackStep(0, 0, guesses)

# Function for backtracking to solve puzzles the other rules will not solve
def backtrackStep(i, j, guesses):

    # If the end of the grid has been reached return true (as the board is valid for all previous cells)
    if (i > 8 or j > 8):
        return True
    
    # If the cell already has a value call the function for the next cell
    if (not guesses[i][j] and grid[i][j] != " "):
        return backtrackStep(i if (j < 8) else i + 1, j+1 if (j < 8) else 0, guesses)
    
    # Try to put the numbers into the board
    for k in range(9):

        # Assign the guessed value
        grid[i][j] = k + 1

        # Check if the guessed value is correct
        if checkValidCell(i, j):

            # Fill in the next cell
            if backtrackStep(i if (j < 8) else i + 1, j+1 if (j < 8) else 0, guesses):
                return True
            
        # If the guessed value was incorrect then reset the value
        grid[i][j] = " "
    
    # If the loop is exited then there is no guessed value that fits so the program needs to backtrack
    return False

# Function to determine if the puzzle has been solved
def isSolved():
    for i in range(9):
        for j in range(9):
            if grid[i][j] == " ":
                return False
            
    return True

# Function to solve the input sudoku
def solve(byStep):
    
    printBoard = makeBoardPrinter() # Make a printer for the board
    printBoard(grid) # Print the board

    # If not going by step, solve the sudoku and output the solution
    if not byStep:
        solveFull(printBoard)
    
    # If going by step, solve the sudoku step by step, printing the results at each stage
    else:
        solveByStep(printBoard)
            

def solveByStep(printBoard):
    while(not isSolved()):

        print("Would you like to see the next step in the solution? (Y-N)")
        ans = input()

        # Exit if the user would not like to see any more of the solution
        if (ans != "y" and ans != "Y"):
            return
        
        # If the user would like to see more of the solution then get the answer step by step
        cont = onlyOneCell(True) or onlyOneCandidate(True)
        hidden = False

        # If unable to fill in a cell, update the candidates
        if not cont:
            hidden = hiddenPairs(ROW, True) or hiddenPairs(COLUMN, True) or hiddenPairs(BOX, True)
            if (hidden):
                cont = True

        # Return if the sudoku is deemed invalid
        if not checkValid():
            print("Error: Sudoku does not have a valid solution")
            return
        
        # Is unable to solve the sudoku by step, exit with an error message
        if not cont:
            outputGrid() # Output the candidates for testing purposes
            print("Unable to solve the sudoku by step any further.")
            print("Would you like to see the full solution? (Y-N)")
            ans = input()

            # Exit if the user would not like to see any more of the solution
            if (ans == "y" or ans == "Y"):
                if backtrack():
                    printBoard(grid)
                else:
                    print("Error: Sudoku does not have a valid solution")

            return
        
        # If only able to continue by updating candidates
        if hidden:
            outputGrid()
            print("Candidate values were updated. See new candidates in output.csv")

        else:
            # Print the new board to the user
            printBoard(grid)
            

def solveFull(printBoard):

    while(onlyOneCell() or onlyOneCandidate() or hiddenPairs(ROW) or hiddenPairs(COLUMN) or hiddenPairs(BOX)):
        continue

    solved = isSolved()

    # If the puzzle is not solved, but still appears solvable then backtrack to solve it
    if(not solved and checkValid()):

        # If backtracking does not solve it print an error message
        if not backtrack():
            print("Error: Sudoku does not have a valid solution")
            return

    # If the sudoku is not in a valid state then print an error message
    elif not solved:
        print("Error: Sudoku does not have a valid solution")
        return
    
    # If the sudoku is solved and is valid then print the solution
    if checkValid():
        printBoard(grid)
        return
    
    # Otherwise print an error message, as the sudoku does not have a valid solution
    else:
        print("Error: Sudoku does not have a valid solution")
        return
            

# Set up the candidates for the board
candidates = setUpCandidates()
# Solve the sudoku
solve(runByStep)

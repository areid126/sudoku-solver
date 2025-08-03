# Read in the sudoku from the file
import sys
import math

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

                # If going step by step return
                if (byStep):
                    return
                


# Function for filling cells where the candidate can only go in that cell
def onlyOneCell(byStep=False):

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

                if (byStep):
                    return


            # If it was found exactly once as a candidate in the column then assign it
            if (colCount == 1):
                grid[colFound][i] = toFind + 1
                updateCandidates(colFound, i)

                if (byStep):
                    return 
        
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

                    if (byStep):
                        return 



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


# Make a printer for the board
printBoard = makeBoardPrinter()

# Print the board
printBoard(grid)

candidates = setUpCandidates()
outputGrid()
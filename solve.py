# Read in the sudoku from the file
import sys

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
            # print(int(part))
        elif(part == ""):
            row.append(" ") # Use ' ' to represent empty cells
            # print(" ")
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

# Make a printer for the board
printBoard = makeBoardPrinter()

# Print the board
printBoard(grid)
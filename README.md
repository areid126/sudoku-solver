# Sudoku Solver

## Summary 

This program can be used to solve any sudoku in one go. It can also be used to solve any simple sudoku step by step. This program is currently capable of applying the following sudoku solving techniques:

- Hidden singles
- Obvious/Naked singles
- Hidden groups


## How to run

Clone the repository

Write the content of the sudoku into the provided excel template file

Save the template file as a '.csv' file

To solve all at once run 'python solve.py <sudokuFileName.csv>'

```
$ python solve.py <sudokuFileName.csv>
```

Alternatively, to solve step by step run 'python solve.py <sudokuFileName.csv> -s'

```
$ python solve.py <sudokuFileName.csv> -s
```
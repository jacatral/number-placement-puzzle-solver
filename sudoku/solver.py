import copy
import csv
import math
import os
import time

from os import path

N = 9
C = math.floor(math.sqrt(N))


current_directory = os.getcwd()
test_validation_directory = path.join(current_directory, "data", "validation")
test_data_directory = path.join(current_directory, "data", "cases")

def read_csv(file_path):
    file = open(file_path, encoding="utf-8-sig", mode="r")

    test_data = file.read().splitlines()
    reader = csv.reader(test_data, delimiter=",")
    file.close()

    rows = []
    for row in reader: 
        rows.append(row)
    return rows

def parse_string_data(line):
    grid = [['' for i in range(N)] for j in range(N)]
    for idx in range(N**2):
        try:
            y = math.floor(idx / N)
            x = idx % N
            grid[y][x] = line[idx]
        except:
            continue
    return grid


# 2-dimensions
# 0 = row
# 1 = column
def valid_digit(cell):
    try:
        cell_value = int(cell)
        return (0 < cell_value and cell_value <= N)
    except:
        return False

def get_row_digits(grid=[[]], row=0):
    return grid[row]
def get_column_digits(grid=[[]], column=0):
    return [grid[i][column] for i in range(N)]
def get_grid_digits(grid=[[]], y=0, x=0):
    return [grid[i + (x * C)][j + (y * C)] for i in range(C) for j in range(C)]

def validate_row(grid=[[]], row=0):
    digits = get_row_digits(grid, row)
    missing_digits = find_missing_digits(digits)
    return len(missing_digits) == 0

def validate_column(grid=[[]], column=0):
    digits = get_column_digits(grid, column)
    missing_digits = find_missing_digits(digits)
    return len(missing_digits) == 0

def validate_grid(grid=[[]], x=0, y=0):
    digits = get_grid_digits(grid, x, y)
    missing_digits = find_missing_digits(digits)
    return len(missing_digits) == 0

def find_missing_digits(digits=[]):
    index_list = [-1 for x in range(N + 1)]
    for index, number in enumerate(digits):
        try:
            digit = int(number)
            index_list[digit] = index
        except:
            #print("Invalid input:", number)
            continue

    missing_numbers = []
    for i in range(1, N + 1):
        if (index_list[i] == -1):
            missing_numbers.append(i)
    return missing_numbers


def sudoku_validate(grid=[[]]):
    invalid_rows = []
    invalid_columns = []
    invalid_grids = []
    for y in range(0, N):
        if (validate_row(grid, y) != True):
            invalid_rows.append(y + 1)
        if (validate_column(grid, y) != True):
            invalid_columns.append(y + 1)

        if (y < C):
            for x in range(0, C):
                if (validate_grid(grid, y, x) != True):
                    invalid_grids.append([y, x])

    is_valid = True
    if (len(invalid_rows) > 0):
        #print("Invalid rows", invalid_rows)
        is_valid = False
    if (len(invalid_columns) > 0):
        #print("Invalid columns", invalid_columns)
        is_valid = False
    if (len(invalid_grids) > 0):
        #print("Invalid grids", invalid_grids)
        is_valid = False
    return is_valid

def find_cell_options(grid=[[]], y=0, x=0):
    gridy = math.floor(y / C)
    gridx = math.floor(x / C)

    dr = get_row_digits(grid, y)
    dc = get_column_digits(grid, x)
    dg = get_grid_digits(grid, gridx, gridy)

    mr = find_missing_digits(dr)
    mc = find_missing_digits(dc)
    mg = find_missing_digits(dg)
    #print(y, dr, mr)
    #print(x, dc, mc)
    #print(gridy, gridx, dg, mg)
    #print(set(mr + mc + mg), list(set(mr + mc + mg)))
    #return list(set(mr + mc + mg))
    return find_missing_digits(dr + dc + dg)

def sudoku_solve(grid=[[]]):
    empty_cells = []
    for y in range(N):
        for x in range(N):
            if not valid_digit(grid[y][x]):
                empty_cells.append([y, x])
    return sudoku_solve_cell(grid, empty_cells)

def sudoku_solve_cell(grid=[[]], cells=[], idx=0):
    if (idx < len(cells)):
        [y, x] = cells[idx]
        missing_digits = find_cell_options(grid, y, x)
        #print(y, x, missing_digits)
        for z in missing_digits:
            #print(y, x, z)
            grid_step = copy.deepcopy(grid)
            grid_step[y][x] = str(z)
            solution = sudoku_solve_cell(grid_step, cells, idx + 1)
            if (solution != None):
                #print("Solution found")
                return solution
    else:
        is_solution_valid = sudoku_validate(grid)
        #for row in grid:
        #    print(row)
        #print(is_solution_valid)
        if (is_solution_valid):
            return grid
        


print("  Testing positive cases")
positive_case_directory = path.join(test_validation_directory, "positive")
positive_case_files = os.listdir(positive_case_directory)
for file_name in positive_case_files:
    file_path = path.join(positive_case_directory, file_name)
    rows = read_csv(file_path)

    case_name = file_name.split(".")[0]
    validation = sudoku_validate(rows)
    print("Expect test-case, " + case_name + ", to be True. Validation found it to be " + str(validation) + "...")
print()

print("  Testing negative cases")
negative_case_directory = path.join(test_validation_directory, "negative")
negative_case_files = os.listdir(negative_case_directory)
for file_name in negative_case_files:
    file_path = path.join(negative_case_directory, file_name)
    rows = read_csv(file_path)

    case_name = file_name.split(".")[0]
    validation = sudoku_validate(rows)
    print("Expect test-case, " + case_name + ", to be False. Validation found it to be " + str(validation) + "...")
print()

print("  Running cases")
case_files = os.listdir(test_data_directory)
for file_name in case_files:
    print(file_name)
    start_time_ms = int(time.time() * 1000)
    file_path = path.join(test_data_directory, file_name)
    rows = read_csv(file_path)
    solution = sudoku_solve(rows)
    if (solution != None):
        #for row in solution:
        #    print(row)
        end_time_ms = int(time.time() * 1000)
        print("Runtime: " + str(round(end_time_ms - start_time_ms)) + "ms")

'''
file_path = path.join(current_directory, "data", "top1465.txt")
file = open(file_path, mode="r")
test_data = file.read().splitlines()
file.close()
for raw_data in test_data[0:2]:
    print(raw_data)
    rows = parse_string_data(raw_data)
    start_time_ms = int(time.time() * 1000)
    
    for row in rows:
        print(row)
    solution = sudoku_solve(rows)
    print(solution)
    if (solution != None):
        for row in solution:
            print(row)
        end_time_ms = int(time.time() * 1000)
        print("Runtime: " + str(round(end_time_ms - start_time_ms)) + "ms")
'''

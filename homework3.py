import collections
import os
from queue import PriorityQueue


def BFS(matrix, start_col, start_row, end_col, end_row, rockHeight):
    rows = len(matrix)
    cols = len(matrix[0])
    visited = set()
    prev = [[set() for i in range(cols)] for j in range(rows)]
    #print(len(prev), len(prev[0]))
    #prev[start_col][start_row] = (None)
    prev[start_row][start_col] = (None)

    if (start_col, start_row) == (end_col, end_row):
        return [(start_col, start_row)]

    queue = collections.deque([(start_col, start_row)])
    visited.add((start_col, start_row))

    while queue:
        col, row = queue.popleft()
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]

        if (col, row) == (end_col, end_row):
            break

        for dr, dc in directions:
            r = row + dr
            c = col + dc

            if c in range(cols) and r in range(rows) and (c, r) not in visited:
                #if r == 724 and c == 685 and row == 725 and col == 684:
                    #print(row, col, matrix[row][col], r, c, matrix[r][c], rockHeight)
                if matrix[r][c] >= 0 and matrix[row][col] >= 0:
                    diff = 0

                elif matrix[r][c] < 0 and matrix[row][col] >= 0:
                    diff = abs(matrix[r][c])

                elif matrix[row][col] < 0 and matrix[r][c]>=0:
                    diff = abs(matrix[row][col])

                else:
                    diff = abs(matrix[r][c] - matrix[row][col])


                if diff <= rockHeight:
                        queue.append((c, r))
                        visited.add((c, r))
                        prev[r][c] = (col, row)

                        # print(prev, end_col, end_row, len(prev), len(prev[0]))

    result = []
    if prev[end_row][end_col] == set():
        return False

    while (end_col, end_row) != (start_col, start_row):
        result.append((end_col, end_row))
        (end_col, end_row) = prev[end_row][end_col]

    result.append((start_col, start_row))
    return result[::-1]

def UCS(matrix, start_col, start_row, end_col, end_row, rockHeight):
    queue = PriorityQueue()
    queue.put((0, (start_col, start_row)))
    start = (start_col, start_row)

    if (start_col, start_row) == (end_col, end_row):
        return [(start_col, start_row)]

    came_from = dict()
    cost_so_far = dict()

    came_from[start] = None
    came_from[(end_col, end_row)] = None
    cost_so_far[start] = 0

    while not queue.empty():
        priorityNum, rowCol = queue.get()
        #print(rowCol)
        col, row = rowCol[0], rowCol[1]
        # col, row = queue.get()
        if (col, row) == (end_col, end_row):
            break

        axial_dir = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        diagonal_dir = [[1, 1], [1, -1], [-1, 1], [-1, -1]]

        for dr, dc in axial_dir:
            r = row + dr
            c = col + dc

            if c in range(len(matrix[0])) and r in range(len(matrix)):
                #print(row, col, r, c)
                if matrix[r][c] >= 0 and matrix[row][col] >= 0:
                    diff = 0

                elif matrix[r][c] < 0 and matrix[row][col] >= 0:
                    diff = abs(matrix[r][c])

                elif matrix[row][col] < 0 and matrix[r][c]>=0:
                    diff = abs(matrix[row][col])

                else:
                    diff = abs(matrix[r][c] - matrix[row][col])


                if diff <= rockHeight:
                    # new_cost = cost_so_far[(col, row)] + 10
                    if matrix[row][col] >= 0:
                        new_cost = cost_so_far[(col, row)] + 10

                    else:
                        new_cost = cost_so_far[(col, row)] + 10

                    if (c, r) not in cost_so_far or new_cost < cost_so_far[(c, r)]:
                        cost_so_far[(c, r)] = new_cost
                        queue.put((new_cost, (c, r)))
                        came_from[(c, r)] = (col, row)

        for dr, dc in diagonal_dir:
            r = row + dr
            c = col + dc

            if c in range(len(matrix[0])) and r in range(len(matrix)):
                if matrix[r][c] >= 0 and matrix[row][col] >= 0:
                    diff = 0

                elif matrix[r][c] < 0 and matrix[row][col] >= 0:
                    diff = abs(matrix[r][c])

                elif matrix[row][col] < 0 and matrix[r][c]>=0:
                    diff = abs(matrix[row][col])

                else:
                    diff = abs(matrix[r][c] - matrix[row][col])

                if diff <= rockHeight:
                    # new_cost = cost_so_far[(col, row)] + 10
                    if matrix[row][col] >= 0:
                        new_cost = cost_so_far[(col, row)] + 14

                    else:
                        new_cost = cost_so_far[(col, row)] + 14

                    if (c, r) not in cost_so_far or new_cost < cost_so_far[(c, r)]:
                        cost_so_far[(c, r)] = new_cost
                        queue.put((new_cost, (c, r)))
                        came_from[(c, r)] = (col, row)


    #print(came_from)
    col, row = end_col, end_row
    res = []
    if came_from[(end_col, end_row)] == None:
        return

    while (col, row) != (start_col, start_row):
        res.append((col, row))
        col, row = came_from[(col, row)]
    res.append((start_col, start_row))

    return res[::-1]


def heuristics(start_col, start_row, goal_col, goal_row):
    D = 1
    D2 = 1
    dx = abs(start_row - goal_row)
    dy = abs(start_col - goal_col)
    return D * (dx + dy) + (D2 - (2 * D)) * min(dx, dy)

def a_star(matrix, start_col, start_row, end_col, end_row, rockHeight):
    queue = PriorityQueue()
    queue.put((0, (start_col, start_row)))
    start = (start_col, start_row)

    if (start_col, start_row) == (end_col, end_row):
        return [(start_col, start_row)]

    came_from = dict()
    cost_so_far = dict()

    came_from[start] = None
    came_from[(end_col, end_row)] = None
    cost_so_far[start] = 0

    while not queue.empty():
        priorityNum, rowCol = queue.get()
        #print(priorityNum, rowCol)
        col, row = rowCol[0], rowCol[1]
        if (col, row) == (end_col, end_row):
            break

        axial_dir = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        diagonal_dir = [[1, 1], [1, -1], [-1, 1], [-1, -1]]

        for dr, dc in axial_dir:
            r = row + dr
            c = col + dc
            #if r == 513 and c == 38 and row == 512 and col == 38:
                #print(matrix[r][c], matrix[row][col], rockHeight )
            if c in range(len(matrix[0])) and r in range(len(matrix)):
                if matrix[r][c] >= 0 and matrix[row][col] >= 0:
                    diff = abs(matrix[r][c])

                elif matrix[row][col] < 0 and matrix[r][c]>=0:
                    diff = abs(matrix[row][col])

                elif matrix[r][c] < 0 and matrix[row][col] >= 0:
                    diff = abs(matrix[r][c])

                else:
                    diff = abs(matrix[r][c] + matrix[row][col])
                    #diff = abs(matrix[r][c] - matrix[row][col])

                if diff <= rockHeight:
                    # new_cost = cost_so_far[(col, row)] + 10
                    if matrix[row][col] >= 0:
                        new_cost = cost_so_far[(col, row)] + 10 + abs(matrix[r][c]) + diff

                    else:
                        new_cost = cost_so_far[(col, row)] + 10 + abs(matrix[r][c]) + diff

                    if (c, r) not in cost_so_far or new_cost < cost_so_far[(c, r)]:
                        cost_so_far[(c, r)] = new_cost
                        priority = new_cost + heuristics(c, r, end_col, end_row)
                        queue.put((priority, (c, r)))
                        came_from[(c, r)] = (col, row)

        for dr, dc in diagonal_dir:
            r = row + dr
            c = col + dc
            #if r == 513 and c == 38 and row == 512 and col == 38:
                #print(matrix[r][c], matrix[row][col], rockHeight)

            if c in range(len(matrix[0])) and r in range(len(matrix)):
                if matrix[r][c] >= 0 and matrix[row][col] >= 0:
                    diff = 0

                elif matrix[r][c] < 0 and matrix[row][col] >= 0:
                    diff = abs(matrix[r][c])

                elif matrix[row][col] < 0 and matrix[r][c]>=0:
                    diff = abs(matrix[row][col])
                    #print(diff, rockHeight, matrix[r][c], matrix[row][col], 'OTHER')

                else:
                    diff = abs(matrix[r][c] + matrix[row][col])

                if diff <= rockHeight:
                    new_cost = cost_so_far[(col, row)] + 14 + matrix[r][c] + diff

                    if (c, r) not in cost_so_far or new_cost < cost_so_far[(c, r)]:
                        cost_so_far[(c, r)] = new_cost
                        priority = new_cost + heuristics(c, r, end_col, end_row)
                        #print(queue.qsize(), 'size')
                        queue.put((priority, (c, r)))
                        came_from[(c, r)] = (col, row)

    col, row = end_col, end_row
    res = []
    if came_from[(end_col, end_row)] is None:
        return

    while (col, row) != (start_col, start_row):
        res.append((col, row))
        col, row = came_from[(col, row)]
    res.append((start_col, start_row))

    return res[::-1]

input_file = open(r'input47.txt','r')
with input_file as f:
    file_content = ((f.readlines()))

if os.path.exists('output.txt'):
    os.remove('output.txt')
algorithm = file_content[0].replace("\n", "")

width, height = file_content[1].replace("\n", "").split()
width, height = int(width), int(height)

x_start, y_start = file_content[2].replace("\n", "").split()
x_start, y_start = int(x_start), int(y_start)

rockHeight = int(file_content[3].replace("\n", ""))

settling_sites = int(file_content[4].replace("\n", ""))
all_sites = []

for i in range(5, 5+settling_sites):
    sites = file_content[i].split()
    sites_Arr = []
    for num in sites:
        sites_Arr.append(int(num))
    all_sites.append(sites_Arr)

matrix = []
for i in range(5+settling_sites, len(file_content)):
    rows = file_content[i].split()
    row_arr = []
    for num in rows:
        row_arr.append(int(num))
    matrix.append(row_arr)



#print(algorithm, width, height, x_start, y_start, rockHeight)
#print(all_sites, (matrix))

if algorithm == "BFS":
    output = ''
    for idx in range(len(all_sites)):
        #print(all_sites[idx][0], all_sites[idx][1])
        BFS_result = BFS(matrix, x_start, y_start, all_sites[idx][0], all_sites[idx][1], rockHeight)
        if not BFS_result:
            #print("FAIL")
            output = 'FAIL '
        else:
            #print(BFS_result)
            for tup in BFS_result:
                output += str(tup[0]) + ',' + str(tup[1]) + ' '
        output = output[:len(output)-1] + '\n'
        output_file = open(r'output.txt', 'a')
        output_file.write(output)
        output = ''
    output_file.close()

if algorithm == "UCS":
    output = ''
    for idx in range(len(all_sites)):
        # print(all_sites[idx][0], all_sites[idx][1])
        UCS_result = UCS(matrix, x_start, y_start, all_sites[idx][0], all_sites[idx][1], rockHeight)
        if not UCS_result:
            #print("FAIL")
            output = 'FAIL '
        else:
            #print(UCS_result)
            for tup in UCS_result:
                output += str(tup[0]) + ',' + str(tup[1]) + ' '

        output = output[:len(output) - 1]
        output += '\n'

        output_file = open(r'output.txt', 'a')
        output_file.write(output)
        output = ''
    output_file.close()

if algorithm == "A*":
    output = ''
    for idx in range(len(all_sites)):
        # print(all_sites[idx][0], all_sites[idx][1])
        a_star_result = a_star(matrix, x_start, y_start, all_sites[idx][0], all_sites[idx][1], rockHeight)
        if not a_star_result:
            #print("FAIL")
            output = 'FAIL '
        else:
            #print(a_star_result)
            for tup in a_star_result:
                output += str(tup[0]) + ',' + str(tup[1]) + ' '

        output = output[:len(output) - 1]
        output += '\n'

        output_file = open(r'output.txt', 'a')
        output_file.write(output)
        output = ''
    output_file.close()
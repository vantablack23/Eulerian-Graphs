#jakis losowy tekst

def neighbour_manual_generator():
    print("Podawaj:")
    initial = [int(x) for x in input().split()]
    matrix = [[0 for x in range(initial[0])] for row in range(initial[0])]

    for i in range(initial[1]):
        edge = [int(x) for x in input().split()]
        matrix[edge[0]-1][edge[1]-1] = 1
        matrix[edge[1]-1][edge[0]-1] = 1
    return matrix

def DFS(matrix, vertice, output = []):
    output.append(vertice)
    for i in range(len(matrix[vertice])):
        if (matrix[vertice][i] == 1) and (i not in output):
            DFS(matrix, i, output)
    return(output)

def check_euler_cycle_undirected(matrix):
    #find isolated vertices
    isolated = 0
    isolated_flag = True
    for i in range(len(matrix)):
        isolated_flag = True
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                isolated_flag = False
                break
        if isolated_flag:
            isolated += 1

    #check if verticies even
    all_even = True
    for i in range(len(matrix)):
        sum = 0
        for j in range(len(matrix[i])):
            sum += matrix[i][j]
        if sum % 2 != 0:
            all_even = False
            break
    
    if all_even and (isolated+len(DFS(matrix,0)) == len(matrix)):
        return True
    else:
        return False

def find_euler_cycle_undirected(matrix, vertice, output=[]):
    for i in range(len(matrix[vertice])):
        if matrix[vertice][i] == 1:
            matrix[vertice][i] = 0
            matrix[i][vertice] = 0
            find_euler_cycle_undirected(matrix, i, output)
    output.append(vertice)
    return(output)


matrix = neighbour_manual_generator()
print(matrix)
if check_euler_cycle_undirected(matrix):
    print(find_euler_cycle_undirected(matrix, 0))
else:
    print("Graf wejściowy nie zawiera cyklu Eulera")


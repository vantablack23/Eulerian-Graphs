import copy

def create_graph_matrix(successors_list, predecessors_list, no_incident_list):
    matrix = [[0 for x in range(len(successors_list)+3)] for row in range(len(successors_list))]

    #step 1 - insert first successor and arcs
    for i in range(len(matrix)):
        matrix[i][len(matrix[0])-3] = successors_list[i][0]
        for v in successors_list[i]:
            matrix[i][v-1] = successors_list[i][len(successors_list[i])-1]

    #step 2 - insert first predecessor and arcs
    for i in range(len(matrix)):
        matrix[i][len(matrix[0])-2] = predecessors_list[i][0]
        for v in predecessors_list[i]:
            matrix[i][v-1] = predecessors_list[i][len(predecessors_list[i])-1] + len(matrix)

    #step 3 - insert not incident vertices and mark lack of arcs
    for i in range(len(matrix)):
        matrix[i][len(matrix[0])-1] = no_incident_list[i][0]
        for v in no_incident_list[i]:
            matrix[i][v-1] = -no_incident_list[i][len(no_incident_list[i])-1]

    return matrix

def neighbour_manual_generator():
    print("Podawaj:")
    initial = [int(x) for x in input().split()]
    #neighbours matrix
    matrix = [[0 for x in range(initial[0])] for row in range(initial[0])]

    #elements needed to create graph matrix
    list_of_successors = [[0] for row in range(initial[0])]
    list_of_predecessors = [[0] for row in range(initial[0])]
    no_incident_list = [[x for x in range(1,initial[0]+1)] for row in range(initial[0])]

    for i in range(initial[1]):
        edge = [int(x) for x in input().split()]
        matrix[edge[0]-1][edge[1]-1] = 1
        matrix[edge[1]-1][edge[0]-1] = 1

        #create lis of successors
        if 0 in list_of_successors[edge[0]-1]:
            list_of_successors[edge[0]-1].remove(0)
        list_of_successors[edge[0]-1].append(edge[1])


        #create list of predecessors
        if 0 in list_of_predecessors[edge[1]-1]:
            list_of_predecessors[edge[1]-1].remove(0)
        list_of_predecessors[edge[1]-1].append(edge[0])
        
    for vertice in list_of_successors:
        vertice.sort()
    
    for vertice in list_of_predecessors:
        vertice.sort()
    
    #create no incident list
    for i in range(len(no_incident_list)):
        for elem in list_of_successors[i]:
            if elem != 0:
                no_incident_list[i].remove(elem)
        for elem in list_of_predecessors[i]:
            if elem != 0:
                no_incident_list[i].remove(elem)

    graph_matrix = create_graph_matrix(list_of_successors, list_of_predecessors, no_incident_list)

    return matrix, graph_matrix

def DFS(matrix, vertice, output = []):
    output.append(vertice)
    for i in range(len(matrix[vertice])):
        if (matrix[vertice][i] == 1) and (i not in output):
            DFS(matrix, i, output)
    return(output)

def DFS_directed(successors_list, vertice, output = []):
    output.append(vertice+1)
    for successor in successors_list[vertice]:
        if successor not in output:
            DFS_directed(successors_list, successor-1, output)
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
    
    flag = all_even and (isolated+len(DFS(matrix,0,[])) == len(matrix))
    return flag

def check_euler_cycle_directed(matrix):
    #find isolated verticies
    isolated = 0
    for i in range(len(matrix)):
        if matrix[i][len(matrix[i])-3] == 0 and matrix[i][len(matrix[i])-2] == 0:
            isolated += 1

    #check if number of successors = number of predecessors
    number_ok = True
    for i in range(len(matrix)):
        successors = 0
        predecessors = 0
        for j in range(len(matrix[i])-3):
            if matrix[i][j] > 0 and matrix[i][j] <= len(matrix):
                successors += 1
            if matrix[i][j] > len(matrix):
                predecessors += 1
        if successors != predecessors:
            number_ok = False
            break

    #create neighbours matrix
    neigbours_matrix = [[0 for x in range(len(matrix))] for row in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] > 0:
                neigbours_matrix[i][j] = 1

    if number_ok and (isolated+len(DFS(neigbours_matrix,0,[])) == len(matrix)):
        return True
    else:
        return False

def find_euler_cycle_undirected(matrix, vertice, output=[]):
    for i in range(len(matrix[vertice])):
        if matrix[vertice][i] == 1:
            matrix[vertice][i] = 0
            matrix[i][vertice] = 0
            find_euler_cycle_undirected(matrix, i, output)
    output.append(vertice+1)
    return(output)

def create_successors_list(graph_matrix): #create list of successors out of graph matrix
    list_of_successors = [[0] for row in range(len(graph_matrix))]
    for i in range(len(graph_matrix)):
        for j in range(len(graph_matrix)):
            if (graph_matrix[i][j] > 0) and (graph_matrix[i][j] <= len(graph_matrix)):
                if 0 in list_of_successors[i]:
                    list_of_successors[i].remove(0)
                list_of_successors[i].append(j+1)
    return list_of_successors

def is_bridge(succesors_list, vertice, successor): #basically check if removing given arc turns graph into inconsistent graph
    isolated = 0
    # print(succesors_list)
    succesors_list[vertice].remove(successor) #remove given arc
    for i in range(len(succesors_list)): #find isolated vertices
        flag = True
        for j in range(len(succesors_list)):
            if i+1 in succesors_list[j]:
                flag = False
                break
        if flag and len(succesors_list[i]) == 0:
            isolated += 1

    # print(f"isolated: {isolated}")
    # print(f"dfs: {isolated+len(DFS_directed(succesors_list, successor-1,[]))}")
    # print(len(succesors_list))
    return not((isolated+len(DFS_directed(succesors_list, successor-1,[]))) == len(succesors_list))

def find_euler_cycle_directed(successors_list, vertice, output=[]):
    output.append(vertice+1) 
    flag = True
    count = 0
    for successor in successors_list[vertice]:
        # print(f"przed if: {successors_list}")
        if not(is_bridge(copy.deepcopy(successors_list), vertice, successor)): #check if arc is a bridge
            flag = False
            # print(f"po if: {successors_list}")
            successors_list[vertice].remove(successor)
            find_euler_cycle_directed(successors_list, successor-1, output)
        count += 1
        if flag and count == len(successors_list[vertice]): #if all arcs are bridges choose last one 
            successors_list[vertice].remove(successor)
            find_euler_cycle_directed(successors_list, successor-1, output)
    return(output)

matrix, graph_matrix = neighbour_manual_generator()
print(f"Macierz sąsiedztwa: {matrix}")
print(f"Macierz grafu: {graph_matrix}")
print("Graf nieskierowany:")
if check_euler_cycle_undirected(matrix):
    print(find_euler_cycle_undirected(matrix, 0))
else:
    print("Graf wejściowy nie zawiera cyklu Eulera")

print("Graf skierowany:")
if check_euler_cycle_directed(graph_matrix):
    print(find_euler_cycle_directed(create_successors_list(graph_matrix),0,[]))
else:
    print("Graf wejściowy nie zawiera cyklu Eulera")

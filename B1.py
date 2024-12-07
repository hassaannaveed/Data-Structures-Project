from tabulate import tabulate

def Task1(filename):

    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Sorry! Find not found.")

    else:
        cleaned_lines = [line for line in lines if line.strip()]

        adj_list = {}

        nodes = cleaned_lines[0].split()
        for line in cleaned_lines[1:]:
            parts = line.split()
            node = parts[0]
            edges = list(map(int, parts[1:]))

        
            adj_list[node] = {nodes[i]: edges[i] for i in range(len(edges)) if edges[i] != 0}

    
        #for node, neighbors in adj_list.items():
            #print(node + ": " + str(neighbors))
    
        data = [[node, neighbors] for node, neighbors in adj_list.items()]
        headers = ["Start", "End"]

        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
    
        return adj_list



fn = "graph_directed_weighted.txt"
adjacency_list = Task1(fn)
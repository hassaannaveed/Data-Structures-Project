from tabulate import tabulate

#filename is the name of the file to be read
def task1(filename):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Sorry! Find not found.")
        return None
    else:
        cleaned_lines = [line for line in lines if line.strip()]

        nodes = cleaned_lines[0].split()

        adj_matrix = [[0 for _ in range(len(nodes))] for _ in range(len(nodes))]
        node_to_index = {node: i for i, node in enumerate(nodes)}
        for line in cleaned_lines[1:]:
            parts = line.split()
            node = parts[0]
            edges = list(map(int, parts[1:]))

            row = node_to_index[node]
            for col, weight in enumerate(edges):
                adj_matrix[row][col] = weight
        data = []
        for i in range(len(nodes)):
            data.append([nodes[i]] + adj_matrix[i])

        headers = ["Node"] + nodes

        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

        return adj_matrix


fn = "graph_directed_weighted.txt"
adjacency_matrix = task1(fn)
#Design notes:
# 1. Squardle is not always square (bastards don't know how to name things)
# 2. We want to do a graph traversal on the puzzle, along with a tree traversal on a dictionary
# 3. Therefore, we have to generate a graph based on the input, and a tree based on a dictionary
# 4. Since (1) is true (curses!) spaces can fill in for blank spaces in a row, and the input should be of the bounding box of the puzzle
# 5. Generating the dictionary tree shouldn't be too difficult, just don't make stupid mistakes which slow it down too bad
# 6. Drawing the output lines to draw would be a nice touch, but isn't necessary and would be a bit of a pain

#Pitfalls to watch out for:
# - Letters can't be used twice

def create_dict(dict_filename):
    root = ('', {})
    with open(dict_filename) as dict_file:
        for word in dict_file:
            add_word(root, word.strip())
    return root

def add_word(dict_root, word):
    if len(word) == 0:
        return
    if word[0] not in dict_root[1]:
        dict_root[1][word[0]] = (word[0],{})
    add_word(dict_root[1][word[0]], word[1:])

def print_tree(dict_root):
    for e in dict_root[1]:
        print_tree_node(dict_root[1][e], 0)

def print_tree_node(n, depth):
    print(' '*depth, end='')
    print(n[0])
    for e in n[1]:
        print_tree_node(n[1][e],depth+1)

def get_input_bounding_box(lines):
    rows = len(lines)
    cols = len(lines[0])
    for l in lines:
        if len(l) != cols:
            print("All lines in input must have the same length as the bounding box of the puzzle")
            return None
    return(rows, cols)

def parse_input(lines):
    """
    :arg lines: List of input lines from the user which make up the puzzle
    :returns: Graph (adj list) of the puzzle
    """
    row_max,col_max = get_input_bounding_box(lines)
    G = {}
    for row,line in enumerate(lines):
        for col,c in enumerate(line):
            if c != ' ':
                G[(c,row,col)] = []
                # Check to the left
                if col-1 >= 0 and line[col-1] != ' ':
                    G[(c,row,col)].append((line[col-1],row,col-1))
                # Check to the Right
                if col+1 < col_max and line[col-1] != ' ':
                    G[(c,row,col)].append((line[col+1],row,col+1))
                # Check above
                if row-1 >= 0 and lines[row-1][col] != ' ':
                    G[(c,row,col)].append((lines[row-1][col],row-1,col))
                # Check below
                if row+1 < row_max and lines[row+1][col] != ' ':
                    G[(c,row,col)].append((lines[row+1][col],row+1,col))
                # Check above left
                if col-1 >= 0 and row-1 >= 0 and lines[row-1][col-1] != ' ':
                    G[(c,row,col)].append((lines[row-1][col-1],row-1,col-1))
                # Check above right
                if col+1 < col_max and row-1 >= 0 and lines[row-1][col+1] != ' ':
                    G[(c,row,col)].append((lines[row-1][col+1],row-1,col+1))
                # Check below left
                if col-1 >= 0 and row+1 < row_max and lines[row+1][col-1] != ' ':
                    G[(c,row,col)].append((lines[row+1][col-1],row+1,col-1))
                # Check below right
                if col+1 < col_max and row+1 < row_max and lines[row+1][col+1] != ' ':
                    G[(c,row,col)].append((lines[row+1][col+1],row+1,col+1))
    return G

def main():
    line = input()
    lines = []
    while line != "":
        lines.append(line)
        line = input()
    G = parse_input(lines)
    print(G)
    words = create_dict('testdict.txt')
    print_tree(words)

if __name__ == "__main__":
    main()

#Design notes:
# 1. Squardle is not always square (bastards don't know how to name things)
# 2. We want to do a graph traversal on the puzzle, along with a tree traversal on a dictionary
# 3. Therefore, we have to generate a graph based on the input, and a tree based on a dictionary
# 4. Since (1) is true (curses!) spaces can fill in for blank spaces in a row, and the input should be of the bounding box of the puzzle
# 5. Generating the dictionary tree shouldn't be too difficult, just don't make stupid mistakes which slow it down too bad
# 6. Drawing the output lines to draw would be a nice touch, but isn't necessary and would be a bit of a pain

#Pitfalls to watch out for:
# - Letters can't be used twice

def create_dict(dict_filename, min_len=0, max_len=100000, ignored_letters=''):
    """
    :arg dict_filename: The path to the dictionary file to read in.
    The dictionary should be a lower-case, alphabetically ordered, newline separated list of words.
    :arg min_len: The minimum length of words to consider.
    Any words in the dictionary shorter than this will not be in the output.
    :arg max_len: The maximum length of words to consider.
    Similar in function to min_len.
    :arg ignored_letters: String of letters which should be ignored.
    Any words containing any of the letters in the string will not be in the output dictionary.
    :return: A dictionary tree with the structure Tuple[<letter>, Dict<next letter>].
    <letter> is the current letter in the tree dictionary, and the next letter dictionary is 
    <letter>->Tuple[<letter>, Dict<nextLetter>] (i.e. it is recursively defined)
    """
    root = ('', {})
    with open(dict_filename) as dict_file:
        for word in dict_file:
            s_word = word.strip()
            if len(s_word) >= min_len and len(s_word) <= max_len:
                add_word(root, s_word, ignored_letters)
    return root

def add_word(dict_root, word, ignored_letters=''):
    if len(word) == 0:
        dict_root[1][''] = ('', None)
        return True
    if word[0] in ignored_letters:
        return False
    if word[0] not in dict_root[1]:
        dict_root[1][word[0]] = (word[0],{})
    if not add_word(dict_root[1][word[0]], word[1:], ignored_letters):
        if len(dict_root[1][word[0]][1]) == 0:
            del dict_root[1][word[0]]
        return False
    return True

def print_words(dict_root, so_far=''):
    if len(dict_root[0]) == 0:
        print(so_far)
    else:
        for e in dict_root[1]:
            print_words(dict_root[1][e], so_far+dict_root[0])

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

def get_puzzle_letters(puzzle_graph):
    letters = []
    for l in puzzle_graph:
        if l[0] not in letters:
            letters.append(l[0])
    return letters

def get_ignored_letters(puzzle_graph):
    ig_letters = []
    puz_letters = get_puzzle_letters(puzzle_graph)
    for l in 'abcdefghijklmnopqrstuvwxyz':
        if l not in puz_letters:
            ig_letters.append(l)
    return ig_letters

def get_step(letter, dict_node):
    if letter in dict_node[1]:
        return dict_node[1][letter]
    return None

def get_neighbors(n, puzzle_graph):
    return puzzle_graph[n]

def solve(puzzle_graph, dictionary):
    words = []
    for n in puzzle_graph:
        words.extend(get_words(n, [], dictionary, puzzle_graph))
    return words

def get_word_from_visited(visited):
    w = []
    for v in visited:
        w.append(v[0])
    return str(w)

def get_words(start, visited, dict_node, puzzle_graph):
    words = []
    neighbors = get_neighbors(start, puzzle_graph)
    if '' in dict_node[1]:
        words.append(get_word_from_visited(visited));
    for n in neighbors:
        next_dict_step = get_step(n[0], dict_node)
        if next_dict_step is not None and n not in visited:
            words.extend(get_words(n, visited + [n], next_dict_step, puzzle_graph))
    return words

def main():
    line = input()
    lines = []
    while line != "":
        lines.append(line)
        line = input()
    G = parse_input(lines)
    print(G)
    print(get_puzzle_letters(G))
    words = create_dict('words_alpha.txt', min_len=4, ignored_letters=get_ignored_letters(G))
    print_words(words)
    solve(G, words)

if __name__ == "__main__":
    main()

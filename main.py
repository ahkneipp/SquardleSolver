#Design notes:
# 1. Squardle is not always square (bastards don't know how to name things)
# 2. We want to do a graph traversal on the puzzle, along with a tree traversal on a dictionary
# 3. Therefore, we have to generate a graph based on the input, and a tree based on a dictionary
# 4. Since (1) is true (curses!) spaces can fill in for blank spaces in a row, and the input should be of the bounding box of the puzzle
# 5. Generating the dictionary tree shouldn't be too difficult, just don't make stupid mistakes which slow it down too bad
# 6. Drawing the output lines to draw would be a nice touch, but isn't necessary and would be a bit of a pain

#Pitfalls to watch out for:
# - Letters can't be used twice

import sys

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
    """
    Recursive function to add a word to the dictionary tree
    :arg dict_root: The node to add the next letter to (See create_dict for a datastructure description)
    :arg word: The word to recursively add to the tree
    :arg ignored_letters: String containing the letters which prevent a word from being added
    :return: True if the word was added, false if it wasn't because it contained a letter in ignored_letters
    """
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
    """
    Recursively prints every word in the dictionary tree
    :arg dict_root: The dictionary tree to print
    :arg so_far: Should not be included by top-level caller.
    String of the letters traversed in the tree so far
    """
    if len(dict_root[0]) == 0:
        print(so_far)
    else:
        for e in dict_root[1]:
            print_words(dict_root[1][e], so_far+dict_root[0])

def print_tree(dict_root):
    """
    Print a the dictionary tree "tree style" with one letter per line and the number of spaces indicating depth
    :arg dict_root: The dictionary tree to print
    """
    for e in dict_root[1]:
        print_tree_node(dict_root[1][e], 0)

def print_tree_node(n, depth):
    """
    Recursive support function for print_tree
    """
    print(' '*depth, end='')
    print(n[0])
    for e in n[1]:
        print_tree_node(n[1][e],depth+1)

def get_input_bounding_box(lines):
    """
    Find the size of the input bounding box for non-square squardles.
    Also, validate input from user to ensure it is rectangular.
    :arg lines: List of lines input by user.  Each must be the same length
    :return: Tuple of (rows, columns) in the bounding box, or None if the input is invalid
    """
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
    """
    Get all of the unique letters present in the puzzle
    :arg puzzle_graph: the Graph representing the puzzle
    :return: List of the unique letters present in the puzzle.
    """
    letters = []
    for l in puzzle_graph:
        if l[0] not in letters:
            letters.append(l[0])
    return letters

def get_ignored_letters(puzzle_graph):
    """
    Inverts the letters in the puzzle in the lowercase alphabetic space.
    """
    ig_letters = []
    puz_letters = get_puzzle_letters(puzzle_graph)
    for l in 'abcdefghijklmnopqrstuvwxyz':
        if l not in puz_letters:
            ig_letters.append(l)
    return ig_letters

def get_step(letter, dict_node):
    """
    Get the next node in the dictionary tree for the given letter
    :arg letter: The letter to get the node for
    :arg dict_node: The current node in the dictionary tree
    :return: The node corresponding to the given letter, or null if it's an invalid step
    """
    if letter in dict_node[1]:
        return dict_node[1][letter]
    return None

def get_neighbors(n, puzzle_graph):
    return puzzle_graph[n]

def solve(puzzle_graph, dictionary):
    """
    Recursively solves the puzzle
    """
    words = []
    # Try starting from each square in the puzzle
    for n in puzzle_graph:
        #print(f'Starting from {n}')
        words.extend(get_words(n, [], dictionary, puzzle_graph))
    return words

def get_word_from_visited(visited):
    """
    Reconstruct a full word from a list of visited graph nodes in forward order
    """
    w = []
    for v in visited:
        w.append(v[0])
    return ''.join(w)

def get_words(start, visited, dict_node, puzzle_graph):
    """
    Recursive solver for the squardle
    """
    words = []
    neighbors = get_neighbors(start, puzzle_graph)
    print(f'Checking {start}')
    # We're currently at the end of the word, add it to the list
    if '' in dict_node[1]:
        w = get_word_from_visited(visited)
        print(f'Reached end of word {w}')
        words.append(w);
    # recursively (DFS) search each of the neighbors
    for n in neighbors:
        print(f'Attempting to traverse to {n}')
        next_dict_step = get_step(n[0], dict_node)
        # If the next step can lead to a valid word and hasn't already been visited
        if next_dict_step is not None and n not in visited:
            words.extend(get_words(n, visited + [n], next_dict_step, puzzle_graph))
        #Debug info about why we didn't take the step
        else:
            if next_dict_step is None:
                print("Could not traverse (invalid word)")
            elif n in visited:
                print("Could not traverse (already visited)")
    return words

def main():
    #Grab the puzzle from the user
    line = input()
    lines = []
    while line != "":
        lines.append(line)
        line = input()
    # Compute the puzzle graph
    G = parse_input(lines)
    # Graph construction failed, quit
    if G is None:
        print("Invalid input!")
        sys.exit(1)
    # Create the tree dictionary, ignore words shorter than 4 letters and with letters not in the puzzle
    words = create_dict('words_alpha.txt', min_len=4, ignored_letters=get_ignored_letters(G))
    #Solve the puzzle
    solutions=solve(G, words)
    # Get the unique solution words in an ordered list
    sorted_solutions = sorted(list(set(solutions)))
    print(sorted_solutions)

if __name__ == "__main__":
    main()

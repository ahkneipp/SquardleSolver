#Design notes:
# 1. Squardle is not always square (bastards don't know how to name things)
# 2. We want to do a graph traversal on the puzzle, along with a tree traversal on a dictionary
# 3. Therefore, we have to generate a graph based on the input, and a tree based on a dictionary
# 4. Since (1) is true (curses!) spaces can fill in for blank spaces in a row, and the input should be of the bounding box of the puzzle
# 5. Generating the dictionary tree shouldn't be too difficult, just don't make stupid mistakes which slow it down too bad
# 6. Drawing the output lines to draw would be a nice touch, but isn't necessary and would be a bit of a pain

#Pitfalls to watch out for:
# - Letters can't be used twice

def parse_input(lines):
    """

    """
    pass

def main():
    line = input()
    lines = []
    while line != "":
        lines.append(line)
        line = input()
    print(lines)



if __name__ == "__main__":
    main()

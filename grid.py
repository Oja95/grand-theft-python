def getGrid(filename):
    f = open(filename)
    grid = f.read()
    grid = grid.replace(" ", "")
    grid = grid.split("\n")
    newGrid = []
    for line in grid:
        newGrid.append(list(line))
    return newGrid
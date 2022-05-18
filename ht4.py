import numpy
import random
import time
N = 9
mutationRate = 0.20
crossoverRate = 1
selectionRate = 0.90
populationQuantity = 500

def sudoku():
    sudokuBoard = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                  [6, 0, 0, 1, 9, 5, 0, 0, 0],
                  [0, 9, 8, 0, 0, 0, 0, 6, 0],
                  [8, 0, 0, 0, 6, 0, 0, 0, 3],
                  [4, 0, 0, 8, 0, 3, 0, 0, 1],
                  [7, 0, 0, 0, 2, 0, 0, 0, 6],
                  [0, 6, 0, 0, 0, 0, 2, 8, 0],
                  [0, 0, 0, 4, 1, 9, 0, 0, 5],
                  [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    return sudokuBoard

def generatePopulation(board):
    populationsBoard = [[]]

    # Generar un arreglo de arreglos que representa la poblacion (una serie de tableros)
    for i in range(N-1):
        populationsBoard.append([])
    for i in range(N):
        for j in range(N):
            populationsBoard[i].append([])

    # Recorrer todos los tableros (poblaciones) y validar cada uno de ellos 
    for i in range(N):
        for j in range(N):
            for k in range(1,N+1):
                # Validar que a la celda aun no se le haya asignado un valor
                if(board[i][j] == 0):
                    # Validar la columna, fila y bloque de 3X3
                    if(not(rowOk(board,i,k) or columnOk(board,j,k) or smallBlockOk(board,i,j,k))):
                        populationsBoard[i][j].append(k)
                else:
                    populationsBoard[i][j].append(board[i][j])
                    break

    populations = []
    for _ in range(1000):
        person = [[]]
        for _ in range(N - 1):
            person.append([])
        for i in range(N):
            row = numpy.zeros(N,dtype=int)
            for j in range(N):
                if (board[i][j] == 0):
                    row[j] = int(populationsBoard[i][j][random.randint(0, len(populationsBoard[i][j]) - 1)])
                else:
                    row[j] = board[i][j]

            while (len(list(set(row))) != N):
                for j in range(0, N):
                    if (board[i][j] == 0):
                        row[j] = int(populationsBoard[i][j][random.randint(0, len(populationsBoard[i][j]) - 1)])

            person[i] = row

        populations.append(person)

    return (populations, updateFit(populations))

def updateFit(populations):
    population = []
    for pop in populations:
        population.append(tuple((pop,findFitness(pop))))
    return population

def mutate(board, candidate):
    randomRate = random.uniform(0, mutationRate - 0.01)

    mutationComplete = False
    if (randomRate < mutationRate):
        while (not mutationComplete):

            firstColumn = 0
            secondColumn = 0

            while (firstColumn == secondColumn):
                firstColumn = random.randint(0, 8)
                secondColumn = random.randint(0, 8)

            randomRow = random.randint(0, 8)

            if (board[randomRow][firstColumn] == 0 and board[randomRow][secondColumn] == 0):
                if (not columnOk(board,secondColumn, candidate[randomRow][firstColumn])
                        and not columnOk(board,firstColumn, candidate[randomRow][secondColumn])
                        and not smallBlockOk(board,randomRow, secondColumn, candidate[randomRow][firstColumn])
                        and not smallBlockOk(board,randomRow, firstColumn, candidate[randomRow][secondColumn])):
                    tempVal = candidate[randomRow][secondColumn]
                    candidate[randomRow][secondColumn] = candidate[randomRow][firstColumn]
                    candidate[randomRow][firstColumn] = tempVal
                    mutationComplete = True

    return

def crossOver(firstParent, secondParent):

    firstChild = numpy.copy(firstParent)
    secondChild = numpy.copy(secondParent)

    randomRate = random.uniform(0, crossoverRate + 0.1)

    first = 2
    second = 1
    if(randomRate < crossoverRate):
        while(first > second):
            first = random.randint(0,8)
            second = random.randint(1,9)

        for i in range(first, second):
            firstChild[i], secondChild[i] = crossoverRows(firstChild[i], secondChild[i])

    return firstChild,secondChild

def crossoverRows(firstRow, secondRow):
    firstChildRow = numpy.zeros(N,dtype=int)
    secondChildRow = numpy.zeros(N,dtype=int)

    rowList = list(range(1, N + 1))
    cycle = 0

    while ((0 in firstChildRow) and (0 in secondChildRow)):
        if (cycle % 2 == 0):
            index = findInRow(firstRow,rowList)
            start = firstRow[index]
            rowList.remove(firstRow[index])
            firstChildRow[index] = firstRow[index]
            secondChildRow[index] = secondRow[index]
            next = secondRow[index]

            while (next != start):
                index = findVal(firstRow, next)
                rowList.remove(firstRow[index])
                firstChildRow[index] = firstRow[index]
                secondChildRow[index] = secondRow[index]
                next = secondRow[index]

            cycle += 1
        else:
            index = findInRow(firstRow, rowList)
            start = firstRow[index]
            rowList.remove(firstRow[index])
            firstChildRow[index] = secondRow[index]
            secondChildRow[index] = firstRow[index]
            next = secondRow[index]

            while (next != start):
                index =findVal(firstRow, next)
                rowList.remove(firstRow[index])
                firstChildRow[index] = secondRow[index]
                secondChildRow[index] = firstRow[index]
                next = secondRow[index]

            cycle += 1

    return firstChildRow, secondChildRow

def findInRow(row, rowList):
    for i in range(0, len(row)):
        if (row[i] in rowList):
            return i

def findVal(row, value):
    for i in range(0, len(row)):
        if (row[i] == value):
            return i

def findFitness(person):
    rowFitness = 0
    columnFitness = 0
    smallBlock = 0
    
    rowZeros = numpy.zeros(N,dtype=int)
    columnZeros = numpy.zeros(N,dtype=int)
    smallBlockZeros = numpy.zeros(N,dtype=int)

    for i in range(N):
        for j in range(N):
            rowZeros[person[i][j] - 1] += 1
        rowFitness += (1.0 / len(set(rowZeros)))/N
        rowZeros = numpy.zeros(N,dtype=int)

    for i in range(N):
        for j in range(N):
            columnZeros[int(person[j][i]) - 1] += 1
        columnFitness += (1.0 / len(set(columnZeros)))/N
        columnZeros = numpy.zeros(N,dtype=int)

    for i in range(0, N, 3):
        for j in range(0, N, 3):

            smallBlockZeros[int(person[i + 2][j] - 1)] += 1
            smallBlockZeros[int(person[i + 2][j + 1] - 1)] += 1
            smallBlockZeros[int(person[i + 2][j + 2] - 1)] += 1

            smallBlockZeros[int(person[i + 1][j] - 1)] += 1
            smallBlockZeros[int(person[i + 1][j + 1] - 1)] += 1
            smallBlockZeros[int(person[i + 1][j + 2] - 1)] += 1

            smallBlockZeros[int(person[i][j] - 1)] += 1
            smallBlockZeros[int(person[i][j + 1] - 1)] += 1
            smallBlockZeros[int(person[i][j + 2] - 1)] += 1

            smallBlock += (1.0 / len(set(smallBlockZeros))) / N
            smallBlockZeros = numpy.zeros(N,dtype=int)

    if (int(smallBlock) == 1 and int(columnFitness) == 1 and int(rowFitness) == 1):
        fitness = 1.0
    else:
        fitness = columnFitness * smallBlock

    return fitness

def columnOk(board, column, val):
    for i in range(N):
        if(board[i][column] == val):
            return True
    return False

def rowOk(baord, row, val):
    for i in range(N):
        if(baord[row][i] == val):
            return True
    return False

def smallBlockOk(board, row, column, val):
    row = 3 * (int(row / 3))
    column = 3 * (int(column / 3))

    if ((board[row][column] == val) or \
            (board[row][column + 1] == val)  or \
            (board[row][column + 2] == val)  or \
            (board[row + 1][column] == val)  or \
            (board[row + 1][column + 1] == val)  or \
            (board[row + 1][column + 2] == val)  or \
            (board[row + 2][column] == val)  or \
            (board[row + 2][column + 1] == val)  or \
            (board[row + 2][column + 2] == val)):
        return True
    else:
        return False

def sortPopulations(populations):

    sortedPopulations = sorted(populations, key=lambda tup: tup[1])
    sortedPopulations.reverse()
    return sortedPopulations

def compete(sortedPopulations):
    firstParent = sortedPopulations[random.randint(0, len(sortedPopulations) - 1)]
    secondParent = sortedPopulations[random.randint(0, len(sortedPopulations) - 1)]

    firstFit = findFitness(firstParent)
    secondFit = findFitness(secondParent)

    if (firstFit <= secondFit):
        better = secondParent
        worse = firstParent
    else:
        better = firstParent
        worse = secondParent

    competeRate = random.uniform(0, crossoverRate + 0.1)
    if (competeRate >= selectionRate):
        return worse
    else:
        return better

def solve(sudoku):

    start_time = time.time()

    initial, initialFit = generatePopulation(sudoku)

    for i in range(0, populationQuantity):
        sortedPopulations = sortPopulations(initialFit)
        if(int(sortedPopulations[0][1]) == 1):
            print("--- %s seconds ---" % (time.time() - start_time))
            print('Population ', i, ' of 500')
            return sortedPopulations[0][0]

        bestPopulations = []
        top5 = 20
        nextPopulation = []

        for i in range(0, top5):
            bestPopulations.append(numpy.copy(sortedPopulations[i]))

        for _ in range(top5, populationQuantity, 2):
            firstParent = compete(initial)
            secondParent = compete(initial)

            firstChild, secondChild = crossOver(firstParent, secondParent)

            mutate(sudoku, firstChild)
            mutate(sudoku, secondChild)

            nextPopulation.append(firstChild)
            nextPopulation.append(secondChild)


        for i in range(0, top5):
            nextPopulation.append(bestPopulations[i][0])

        initial = nextPopulation
        initialFit = updateFit(nextPopulation)

print(solve(sudoku()))
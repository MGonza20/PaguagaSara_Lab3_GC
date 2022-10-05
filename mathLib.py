# Libreria personal matematica

def mm(m1, m2):
        l_M1 = len(m1)
        l_M1_in, l_M2_in = len(m1[0]), len(m2[0])
        matrixR = []

        for rM1 in range(l_M1):
            new = []
            for cM2 in range(l_M2_in):
                new.append(sum(m1[rM1][rM2] * m2[rM2][cM2] for rM2 in range(l_M1_in)))
            matrixR = matrixR + [new]

        return matrixR

def subtractVectors(v1, v2):
    v1x, v1y, v1z = v1.x, v1.y, v1.z
    v2x, v2y, v2z = v2.x, v2.y, v2.z

    return [(v1x - v2x), (v1y - v2y), (v1z - v2z)]


def subtractVList(v1, v2):

    if len(v1) == 3:
        v1x, v1y, v1z = v1[0], v1[1], v1[2]
        v2x, v2y, v2z = v2[0], v2[1], v2[2]

        return [(v1x - v2x), (v1y - v2y), (v1z - v2z)]

    elif len(v1) == 2:
        v1x, v1y = v1[0], v1[1]
        v2x, v2y = v2[0], v2[1]

        return [(v1x - v2x), (v1y - v2y)]

def addVectors(v1, v2):
    v1x, v1y, v1z = v1[0], v1[1], v1[2]
    v2x, v2y, v2z = v2[0], v2[1], v2[2]

    return [(v1x + v2x), (v1y + v2y), (v1z + v2z)]


def crossProduct(v1, v2):
    v1x, v1y, v1z = v1[0], v1[1], v1[2]
    v2x, v2y, v2z = v2[0], v2[1], v2[2]

    x = (v1y * v2z) - (v2y * v1z)
    y = (v2x * v1z) - (v1x * v2z)
    z = (v1x * v2y) - (v2x * v1y)

    return [x, y, z]

def normV(v):
    x, y, z = v[0], v[1], v[2]
    xSquared = (x)**2
    ySquared = (y)**2
    zSquared = (z)**2
    norm = (xSquared + ySquared + zSquared)**0.5

    return  [(x/norm), (y/norm), (z/norm)] 

def norm(v):
    x, y, z = v[0], v[1], v[2]
    xSquared = (x)**2
    ySquared = (y)**2
    zSquared = (z)**2

    return (xSquared + ySquared + zSquared)**0.5

def dotProduct(v1, v2):
    v1x, v1y, v1z = v1[0], v1[1], v1[2]
    v2x, v2y, v2z = v2[0], v2[1], v2[2]

    return (v1x * v2x) + (v1y * v2y) + (v1z * v2z)


def mDet(matrix):

    det, sign = 0, -1
    # En caso de que la submatriz llegue a ser de 1X1
    # Se termina la recursion y se devuelve el valor obtenido
    if len(matrix) == 1: return matrix[0][0]
    
    #Por cada fila en la matriz
    for i in range(len(matrix)):
        #En cada loop se alterna el signo al multiplicarlo por 1
        
        #En cada loop se crea la submatriz correspondiente
        subM = []
        sign *= -1
        # Se hace loop por cada fila sin tomar en cuenta la primera fila
        for j in matrix[1:]:
            # Se anaden las filas a la submatriz sin tomar en 
            # cuenta la columna i, segun el loop
            subM.append(j[:i] + j[(i + 1):])

        #Se selecciona el número por el que se selecionara la submatriz
        multiplier = matrix[0][i]
        det += sign * multiplier * mDet(subM)

    return det


def adjMatrix(matrix):
    adjList = [[0, 0, 0, 0], 
               [0, 0, 0, 0], 
               [0, 0, 0, 0],
               [0, 0, 0, 0]] \
               if (len(matrix) == 4) else \
               [[0, 0, 0], 
               [0, 0, 0], 
               [0, 0, 0]] 
    
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            subM = [(r[:j] + r[(j+1):]) for r in (matrix[:i]+ matrix[i+1:])]
            adjList[i][j] = mDet(subM)
    
    signs = [[1,-1,1,-1],[-1,1,-1,1], [1,-1,1,-1], [-1,1,-1,1]] \
            if (len(matrix) == 4) else \
            [[1,-1,1],[-1,1,-1], [1,-1,1]]
    adjL = [[xx * yy for xx, yy in zip(x, y)] for x, y in zip(signs,adjList)]

    return adjL


def transposeMatrix(matrix):
    return list(map(list, zip(*matrix)))


def inverse(matrix):
    tM = transposeMatrix(adjMatrix(matrix)) 
    det = 1/mDet(matrix)
    return [[item * det for item in i] for i in tM] 

def multiplyy(m1, m2):
    newMatrix = []
    if len(m1) == len(m2):
        for indx in range(len(m1)):
            newMatrix.append([])
            if len(m1[indx]) == len(m2[indx]):
                for indx2 in range(len(m1[indx])):
                    newMatrix[indx].append(0)
                    newMatrix[indx][indx2] =  m1[indx][indx2] * m2[indx][indx2]
    return newMatrix
import Pipeline
import Execute
import pandas


def read_instructions(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines if line.strip()]


def merge_rows(row1, row2):
    newRow = []
    newRow.append(row1[0])
    for i in range(1, len(row1)):
        if row1[i] != 0 and row2[i] != 0:
            newRow.append([row1[i], row2[i]])
        elif row1[i] == 0 and row2[i] == 0:
            newRow.append(0)
        else:
            newRow.append(row1[i] if row1[i] != 0 else row2[i])
    return newRow


def merge_matrix(matrix):
    for i in range(len(instructions)):
        tempList = []
        counter = 0
        j = 0
        while j < len(newInstructions):
            instruction = newInstructions[j]
            if instruction[2] == i:
                tempList.append(matrix[j])
                if counter != 0:
                    del matrix[j]
                    del newInstructions[j]
                    j -= 1
                counter += 1
            j += 1
        sizeOfList = len(tempList)
        while sizeOfList > 1:
            tempList[0] = merge_rows(tempList[0], tempList[1])
            del tempList[1]
            sizeOfList = len(tempList)
        if len(tempList) > 0:
            matrix[i] = tempList[0]

    return matrix


def to_string(matrix):
    for i in range(len(matrix)):
        for j in range(len((matrix[i]))):
            matrix[i][j] = "-" if matrix[i][j] == 0 or matrix[i][j] == None else matrix[i][j]
    return matrix


def eraseEmptyLines(matrix):
    newMatrix = []
    for i in range(len(matrix)):
        if matrix[i][0] != "-":
            newMatrix.append(matrix[i])
    return newMatrix


def eraseEmptyColumn(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i]) - 1, -1, -1):
            if matrix[i][j] != "-":
                break
            else:
                del matrix[i][j]
    return matrix


def arrangeMatrix(matrix):
    max = 0
    for i in range(len(matrix)):
        max = len(matrix[i]) if len(matrix[i]) > max else max
    for i in range(len(matrix)):
        for j in range(max + 1):
            if j > len(matrix[i]):
                matrix[i].append("-")
    return matrix


def beautifyMatrix(matrix):
    matrix = to_string(matrix)
    matrix = eraseEmptyLines(matrix)
    matrix = eraseEmptyColumn(matrix)
    matrix = arrangeMatrix(matrix)
    return matrix


def resetRegisterFile():
    Execute.registerFile = {
        '$zero': 0, '$at': 0, '$v0': 0, '$v1': 0, '$a0': 0, '$a1': 0, '$a2': 0, '$a3': 0,
        '$t0': 0, '$t1': 0, '$t2': 0, '$t3': 0, '$t4': 0, '$t5': 0, '$t6': 0, '$t7': 0,
        '$s0': 0, '$s1': 0, '$s2': 0, '$s3': 0, '$s4': 0, '$s5': 0, '$s6': 0, '$s7': 0,
        '$t8': 0, '$t9': 0, '$k0': 0, '$k1': 0, '$gp': 0, '$sp': 0, '$fp': 0, '$ra': 0
    }


instructions = read_instructions("input.txt")

newInstructions = Execute.assembler(instructions)
matrix = Pipeline.pipeline(newInstructions)
# resetRegisterFile()
# Pipeline.addJumpedInstructions(instructions,matrix)
# print(pandas.DataFrame(matrix).to_string())
matrix = merge_matrix(matrix)
matrix = beautifyMatrix(matrix)

print(pandas.DataFrame(matrix).to_string())
print(
    "--------------------------------------------------------------------------------------------------------------------------------------------")
resetRegisterFile()
print(pandas.DataFrame(Execute.registerCalculation(instructions)).to_string())

# print(pandas.DataFrame().to_string())

# matrix  = Pipeline.pipeline(instructions)
# print(pandas.DataFrame(matrix).to_string())
# print(pandas.DataFrame(Execute.assembler(instructions)).to_string())
# print(pandas.DataFrame(Execute.registerFile))

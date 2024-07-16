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
        j =0
        while j < len(newInstructions):
            instruction = newInstructions[j]
            if instruction[2] == i:
                tempList.append(matrix[j])
                if counter != 0:
                    del matrix[j]
                    del newInstructions[j]
                    j-=1
                counter+=1
            j+=1
        sizeOfList = len(tempList)
        while sizeOfList > 1:
            tempList[0] = merge_rows(tempList[0], tempList[1])
            del tempList[1]
            sizeOfList = len(tempList)
        if len(tempList) > 0:
            matrix[i] = tempList[0]

    return matrix


instructions = read_instructions("input.txt")

newInstructions = Execute.assembler(instructions)
matrix = Pipeline.pipeline(newInstructions)
print(pandas.DataFrame(matrix).to_string())
matrix = merge_matrix(matrix)
print(pandas.DataFrame(matrix).to_string())
# print(pandas.DataFrame().to_string())

# matrix  = Pipeline.pipeline(instructions)
# print(pandas.DataFrame(matrix).to_string())
# print(pandas.DataFrame(Execute.assembler(instructions)).to_string())
# print(pandas.DataFrame(Execute.registerFile))

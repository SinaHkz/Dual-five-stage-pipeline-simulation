import Execute

matrix = [[0 for _ in range(20)] for _ in range(10)]
R_TYPE = {'add', 'sub', 'and', 'or', 'sll', 'srl', 'slt', 'sltu'}
I_TYPE = {'lw', 'sw', 'addi', 'andi', 'ori'}
S_Type = {'add', 'sub', 'and', 'or', 'sll', 'srl', 'slt', 'sltu', 'lw', 'addi', 'andi', 'ori'}

forwardBranch = 0
backwardBranch = 1



def replace_zeros_with_previous(row):
    previous_value = 0
    for i in range(1, len(row)):
        if row[i] == "WB":
            return row
        if row[i] == 0:
            row[i] = previous_value
        else:
            previous_value = row[i]
    return row


def remove_subsequent_occurrences(row):
    for i in range(1,len(row)):
        if row[i] == row[i-1]:
            row[i] = 0
    return row

# Function to modify the entire matrix
def modify_matrix(matrix):
    modified_matrix = []
    for row in matrix:
        modified_row = remove_subsequent_occurrences(row)
        modified_matrix.append(modified_row)
    return modified_matrix


def pipeline(instructions):
    for currentStage in range(len(instructions)):
        matrix[currentStage][0] = Execute.parse_instruction(instructions[currentStage])
        instructions[currentStage] = Execute.parse_instruction(instructions[currentStage])
    stages = ["IF", "ID", "EX", "DM", "WB"]
    currentInstruction = 0
    while currentInstruction < len(instructions):
        currentStage = 0
        currentCycle = 1
        currentOp = instructions[currentInstruction][0]
        while currentStage < 5:
            rs = instructions[currentInstruction][1][1]
            rt = instructions[currentInstruction][1][2]
            if currentOp == "sw":
                rt = instructions[currentInstruction][1][0]

            prevLine = currentInstruction - 1
            fetchCounter = 0
            while currentStage == 0 and prevLine >= 0:
                if matrix[prevLine][currentCycle] == "IF":
                    fetchCounter += 1
                prevLine -= 1
            if fetchCounter >= 3:
                currentCycle += 1
                continue
            prevLine = currentInstruction - 1
            decodeCounter = 0
            while currentStage == 1 and prevLine >= 0:
                if matrix[prevLine][currentCycle] == "ID":
                    decodeCounter += 1
                prevLine -= 1
            if decodeCounter >= 2:
                currentCycle += 1
                continue

            if currentStage == 2:
                maxStall = currentCycle
                for i in range(currentInstruction - 1, -1, -1):
                    prevOp = instructions[i][0]
                    rd = instructions[i][1][0]
                    if prevOp in S_Type and (rd == rs or rd == rt):
                        if prevOp == "lw":
                            maxStall = matrix[i].index("WB") if matrix[i].index("WB") > maxStall else maxStall
                        else:
                            maxStall = matrix[i].index("ID") if matrix[i].index("ID") > maxStall else maxStall
                        currentCycle = maxStall
                        matrix[currentInstruction][currentCycle] = stages[currentStage]
            matrix[currentInstruction][currentCycle] = stages[currentStage]
            currentCycle += 1
            currentStage += 1
        replace_zeros_with_previous(matrix[currentInstruction])
        currentInstruction += 1
    return modify_matrix(matrix)



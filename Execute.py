# Initialize registers
import random


def parse_instruction(instruction1):
    instruction = instruction1
    parts = instruction.split(" ")
    op = parts[0]
    args = parts[1].split(',')
    if op in {"lw", "sw"}:
        args = [args[0], args[1].split("(")[0], args[1].split("(")[1][:-1]]
    return [op, args]


R_TYPE = {'add', 'sub', 'and', 'or', 'sll', 'srl', 'slt', 'sltu'}
I_TYPE = {'lw', 'sw', 'addi', 'andi', 'ori'}

registerFile = {
    '$zero': 0, '$at': 0, '$v0': 0, '$v1': 0, '$a0': 0, '$a1': 0, '$a2': 0, '$a3': 0,
    '$t0': 0, '$t1': 0, '$t2': 0, '$t3': 0, '$t4': 0, '$t5': 0, '$t6': 0, '$t7': 0,
    '$s0': 0, '$s1': 0, '$s2': 0, '$s3': 0, '$s4': 0, '$s5': 0, '$s6': 0, '$s7': 0,
    '$t8': 0, '$t9': 0, '$k0': 0, '$k1': 0, '$gp': 0, '$sp': 0, '$fp': 0, '$ra': 0
}
memory = {}


def add(rd, rs, rt):
    registerFile[rd] = registerFile[rs] + registerFile[rt]


def addi(rt, rs, immediate):
    registerFile[rt] = registerFile[rs] + immediate


def sub(rd, rs, rt):
    registerFile[rd] = registerFile[rs] - registerFile[rt]


def and_op(rd, rs, rt):
    registerFile[rd] = registerFile[rs] & registerFile[rt]


def andi(rt, rs, immediate):
    registerFile[rt] = registerFile[rs] & immediate


def or_op(rd, rs, rt):
    registerFile[rd] = registerFile[rs] | registerFile[rt]


def ori(rt, rs, immediate):
    registerFile[rt] = registerFile[rs] | immediate


def sll(rd, rt, sa):
    registerFile[rd] = registerFile[rt] << sa


def srl(rd, rt, sa):
    registerFile[rd] = registerFile[rt] >> sa


def lw(rt, offset, base):
    # Assuming memory is a dictionary storing word values by address
    address = registerFile[base] + offset
    if address not in memory.keys():
        registerFile[rt] = random.randint(0, 1000)
    else:
        registerFile[rt] = memory[address]


def sw(rt, offset, base):
    # Assuming memory is a dictionary storing word values by address
    address = registerFile[base] + offset
    memory[address] = registerFile[rt]


def slt(rd, rs, rt):
    registerFile[rd] = 1 if registerFile[rs] < registerFile[rt] else 0


def sltu(rd, rs, rt):
    registerFile[rd] = 1 if (registerFile[rs] & 0xFFFFFFFF) < (registerFile[rt] & 0xFFFFFFFF) else 0


def beq(rs, rt):
    if registerFile[rs] == registerFile[rt]:
        return True
    return False


def execute_instruction(instruction):
    # op, args = parse_instruction(instruction)
    op, args = instruction
    if op == 'add':
        add(args[0], args[1], args[2])
    elif op == 'addi':
        addi(args[0], args[1], int(args[2]))
    elif op == 'sub':
        sub(args[0], args[1], args[2])
    elif op == 'and':
        and_op(args[0], args[1], args[2])
    elif op == 'andi':
        andi(args[0], args[1], int(args[2]))
    elif op == 'or':
        or_op(args[0], args[1], args[2])
    elif op == 'ori':
        ori(args[0], args[1], int(args[2]))
    elif op == 'sll':
        sll(args[0], args[1], int(args[2]))
    elif op == 'srl':
        srl(args[0], args[1], int(args[2]))
    elif op == 'lw':
        lw(args[0], int(args[1]), args[2])
    elif op == 'sw':
        sw(args[0], int(args[1]), args[2])
    elif op == 'slt':
        slt(args[0], args[1], args[2])
    elif op == 'sltu':
        sltu(args[0], args[1], args[2])
    elif op == 'beq':
        return beq(args[0], args[1])
    else:
        raise ValueError(f"Unknown operation {op}")
    registerFile["$zero"] = 0


def registerCalculation(instructions):
    registers = {
        '$zero': [0], '$at': [0], '$v0': [0], '$v1': [0], '$a0': [0], '$a1': [0], '$a2': [0], '$a3': [0],
        '$t0': [0], '$t1': [0], '$t2': [0], '$t3': [0], '$t4': [0], '$t5': [0], '$t6': [0], '$t7': [0],
        '$s0': [0], '$s1': [0], '$s2': [0], '$s3': [0], '$s4': [0], '$s5': [0], '$s6': [0], '$s7': [0],
        '$t8': [0], '$t9': [0], '$k0': [0], '$k1': [0], '$gp': [0], '$sp': [0], '$fp': [0], '$ra': [0]
    }
    for instruction in instructions:
        execute_instruction(instruction)
        for register in registers.keys():
            if register == instruction[1][0] and instruction[0] != "sw":
                registers[register].append(registerFile[register])
            else:
                registers[register].append(0)
    return registers


def assembler(instructions):
    newInstructions = []
    instructionIndex = 0
    count = 0
    while instructionIndex < len(instructions) and count < 10:
        instruction = parse_instruction(instructions[instructionIndex])
        branchIsTaken = execute_instruction(instruction)
        newInstructions.append(instruction + [instructionIndex])
        opcode = instruction[0]

        if opcode == "beq" and branchIsTaken:
            constant = int(instruction[1][2])
            if constant < 0:
                for i in range(instructionIndex + constant + 1, instructionIndex + 1):
                    newInstructions.append(parse_instruction(instructions[i]) + [i])
            instructionIndex += constant

        instructionIndex += 1
        count += 1
    return newInstructions

# # Example usage:
# instruction = "add $s0, $s1, $s2"
# execute_instruction(instruction)
# print(registers['$s0'])  # Output: 0 if $s1 and $s2 were initially 0
#
# # You can set initial values to registers for testing:
# registers['$s1'] = 10
# registers['$s2'] = 20
# execute_instruction("add $s0, $s1, $s2")
# print(registers['$s0'])  # Output: 30

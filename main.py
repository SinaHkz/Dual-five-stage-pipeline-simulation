import Pipeline
import Execute
import pandas


def read_instructions(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines if line.strip()]


instructions = read_instructions("input.txt")

matrix  = Pipeline.pipeline(instructions)
# print(pandas.DataFrame(matrix).to_string())
print(pandas.DataFrame(Execute.registerCalculation(instructions)).to_string())

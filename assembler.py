import sys
from os.path import exists
from string import ascii_letters, digits

OPERAND_FORMS: dict[str, int] = {
    "LDR": 2,
    "STR": 2,
    "ADD": 3,
    "SUB": 3,
    "MUL": 3,
    "DIV": 3,
    "MOV": 2,
    "CMP": 2,
    "B": 1,
    "BEQ": 1,
    "BNE": 1,
    "BGT": 1,
    "BLT": 1,
    "AND": 2,
    "ORR": 2,
    "EOR": 2,
    "MVN": 1,
    "LSL": 2,
    "LSR": 2,
    "HALT": 0,
    "NOP": 0
}
OPERATOR: int = 2 ** 17
IMMEDIATE_FLAG: int = 2 ** 16
OPERAND_1: int = 2 ** 12
OPERAND_2: int = 2 ** 8
OPERAND_3: int = 2 ** 0

def get_labels(lines: list[str]) -> dict[str, int]:
    labels: dict[str, int] = {}
    for i, line in enumerate(lines):
        if ":" not in line:
            continue
        labels[line.split(":")[0]] = i
    return labels

def get_value(string: str) -> tuple[int, int]:
    annotation, data = string[0], string[1:]
    if not data.isdigit():
        return f"Expected integer operand, got {data}"
    if annotation not in "R#":
        return f"Unexpected type `{annotation}` specified for {data}. Expected `R` (register) or `#` (immediate)."
    return ("R#".index(annotation), int(data))

def assemble_line(labels: dict[str, int], line: str) -> tuple[int, str]:
    if line == "" or line.lstrip().startswith("#") or line.rstrip().endswith(":"):
        return 0, ""
    tokens: list[str] = [token for token in line.split() if ":" not in token]
    if tokens[0] not in OPERAND_FORMS.keys():
        return f"Unrecognised operation: `{tokens[0]}` - are you sure you spelt it correctly?"
    if len(tokens) != (expected := OPERAND_FORMS[tokens[0]]) + 1:
        return f"Incorrect number of operands ({len(tokens) - 1}) for operation `{tokens[0]}` - expected {expected}."
    is_immediate: bool = False
    if tokens[0].startswith("B"):
        label: str = tokens[1]
        label_location: int = labels.get(label)
        if label_location is None:
            return f"Attempted to branch to undefined label `{label}`"
        tokens[1] = 0
        tokens.append(label_location + 3)
        is_immediate = True
    else:
        for i, token in enumerate(tokens):
            if i == 0:
                continue
            value: tuple[int, int] = get_value(token)
            if isinstance(value, str):
                return value
            is_immediate, value = value
            if is_immediate and i != len(tokens) - 1:
                return f"Operand {i}: `{value}` marked as immediate (using `#`). Only the last operand in an operation may be marked as immediate."
            tokens[i] = value
    ram_req: int = 0
    if tokens[0] in ("LDR, STR"):
        ram_req = tokens[2]
    if len(tokens) == 3:
        tokens.append(tokens[2])
        tokens[2] = 0
    tokens += [0] * (4 - len(tokens))
    assembled = sum((
        tuple(OPERAND_FORMS.keys()).index(tokens[0]) * OPERATOR,
        int(is_immediate) * IMMEDIATE_FLAG,
        tokens[1] * OPERAND_1,
        tokens[2] * OPERAND_2,
        tokens[3] * OPERAND_3
    ))
    return ram_req, str(assembled)

def main(argc: int, argv: list[str]) -> int:
    if argc != 2 or argv[1] == "-h":
        print("python3 assembler.py [FILE]\n\nAssembles [FILE] to run on Benji's DesmosCPU and prints the LaTeX to the console.")
        return 0
    filename: str = argv[1]
    if not exists(filename):
        print(f"ERROR:\nFile not found: {filename}.")
        return 1
    program_name: str = "".join([c for c in filename.split(".")[0] if c in ascii_letters + digits])
    machine_code: str = ""
    ram_requirement: int = 0
    with open(filename) as file:
        lines: list[str] = file.read().split("\n")
        labels: dict[str, int] = get_labels(lines)
        entry: int = labels.get("main")
        if entry is None:
            print(f"ERROR:\nNo entry point specified. Specify an entry point by including `main:` At the beginning of the first line you want to be executed.")
            return 1
        for line in lines:
            result: tuple[int, str] = assemble_line(labels, line)
            if isinstance(result, str):
                print(f"ERROR [line {line}]:\n" + result)
                return 1
            ram_req, assembled = result
            if ram_req:
                ram_requirement = max(ram_requirement, ram_req)
            if assembled:
                machine_code += "," + assembled
    header: str = f"{entry + 2},{ram_requirement}"
    program: str = f"p_{'{'}{program_name}{'}'}=[{header}{machine_code}]"
    print(program)

if __name__ == "__main__":
    returncode: int = main(len(sys.argv), sys.argv)
    exit(returncode)

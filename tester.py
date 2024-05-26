#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
from collections import OrderedDict

BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"  # orange on some systems
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
LIGHT_GRAY = "\033[37m"
DARK_GRAY = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
WHITE = "\033[97m"

RESET = "\033[0m"  # called to return to standard terminal text color

currentDir = None
executarTodosEX = False
success = {}

# Open the file to write the report
try:
    report = open("diff.txt", "w")
except:
    print(f"{RED}Error opening file!{RESET}")
    raise Exception("Error opening file!")
    exit()


parser = argparse.ArgumentParser(description="Simple C Tester")

# Optional argument to specify which directory to test
parser.add_argument(
    "directory",
    type=str,
    help="Directory from which to test",
    const="./",
    nargs="?",
    default="./",
)
# Optional argument to specify which exercise to run
parser.add_argument(
    "number",
    type=int,
    help="Which number of the exercise to run (-1 for all)",
    const=-1,
    nargs="?",
    default=-1,
)

args = parser.parse_args()

# Check if the number is -1 to run all exercises
if args.number == -1:
    executarTodosEX = True
else:
    executarTodosEX = False
    if (type(args.number) != int) or (args.number < 1):
        # Check if the number is a valid integer
        print(f"{RED}Invalid number!{RESET}")
        raise Exception("Invalid number!")
        exit()
# Check if the directory is a valid directory
if (type(args.directory) != str) or (not os.path.isdir(args.directory)):
    # Check if the directory is a valid directory
    print(f"{RED}Invalid directory!{RESET}")
    raise Exception("Invalid directory!")
    exit()
else:
    if args.directory.endswith("/") == False:
        # Add a slash to the end of the directory if it doesn't have one
        args.directory = args.directory + "/"
    currentDir = args.directory


# Functions to get the directories and files
def get_ex_directory_paths(current_dir="./"):
    """
    Scans the current directory and creates a list of paths for directories named ex*.
    """
    ex_directories = []
    for item in os.listdir(current_dir):
        if item.startswith("ex") and os.path.isdir(os.path.join(current_dir, item)):
            # Check if item starts with "ex" and is a directory
            ex_directories.append(os.path.join(current_dir, item))
    return ex_directories


def get_all_files(directory_path):
    """
    Creates a list of all files within a specified directory path.
    """
    file_list = []
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isfile(item_path):
            # Check if it's a file and add the full path to the list
            file_list.append(item_path)
    return file_list


# Function to extract digits from a string
def extract_digits(s, option="entrada"):
    return re.findall(rf"${option}(\d+)", s)


# Function to compile the C code
def compileC(c_code):
    call_string = (
        "gcc "
        + "-Wall -Wextra -Wpedantic -fsanitize=undefined "
        + c_code
        + " -o "
        + c_code.replace(".c", "")
    )
    return_code = subprocess.call(call_string, shell=True)
    if return_code == 0:
        print(f"Compilation {GREEN}successful!{RESET}\n")
        return 1
    else:
        print(f"Compilation {RED}failed!{RESET}\n")
        return 0


# Function to write the report
def write_report(reportFile, message, entrada):
    reportFile.write(
        f"-> O arquivo de saida gerado pelo seu programa {entrada.split('/')[-1].replace('entrada','saida')} e o arquivo de saida correta { 'saidascorretas/' + entrada.split('/')[-1].replace('entrada','saida')} sao diferentes.\n"
    )
    report.write(message.communicate()[0].decode())


# Function to sort the file paths
def sort_file_paths(file_paths, option):
    def file_number(file_path):
        # Extract the number from the file path
        regexMount = rf"{option}(\d+)"
        match = re.search(regexMount, file_path)
        if match:
            return int(match.group(1))
        return 0

    return sorted(file_paths, key=file_number)


# Function to get the input files
def getEntradas(ex_path):
    entradas = []
    entradas_txt = get_all_files(ex_path + "/entradas/")

    entradas_txt = sort_file_paths(entradas_txt, "entrada")
    for entrada in entradas_txt:
        entradas.append(entrada)
    return entradas


# Function to get the output files
def getSaidas(ex_path):
    saidas = []
    saidas_txt = get_all_files(ex_path + "/saidascorretas/")
    saidas_txt = sort_file_paths(saidas_txt, "saida")
    for saida in saidas_txt:
        saidas.append(saida)
    return saidas


# Get the paths of the exercises
if currentDir:
    ex_paths = get_ex_directory_paths(current_dir=currentDir)
else:
    ex_paths = get_ex_directory_paths()
ex_paths = sorted(ex_paths)

# Check if needs to run all exercises
if executarTodosEX:
    print(f"{YELLOW}Running all exercises...{RESET}\n")
    # Loop through all the exercises
    for ex_path in ex_paths:
        nome_ex = ex_path.split("/")[-1]
        print(f"{YELLOW}Processing {nome_ex}{RESET}\n")
        files_in_exDIR = get_all_files(ex_path)
        c_code = None
        # Check if there is a C code in the exercise directory
        for file in files_in_exDIR:
            if re.findall(r"^ex\d+\.c$", file.split("/")[-1]):
                c_code = file
                break
        if c_code:
            print(f"{GREEN}C code found! {RESET} {c_code.split('/')[-1]}")
            # Compile the C code
            if compileC(c_code):
                executable = c_code.replace(".c", "")
                print(f"{YELLOW}Checking Input files...{RESET}\n")
                # Check if there are input files
                if os.path.exists(ex_path + "/entradas"):
                    entradas_txt = getEntradas(ex_path)
                    # Loop through all the input files
                    for entrada in entradas_txt:
                        minha_saidaPATH = (
                            ex_path
                            + "/"
                            + entrada.split("/")[-1].replace("entrada", "saida")
                        )
                        # Run the C code with the input file
                        command = executable + " < " + entrada + " > " + minha_saidaPATH
                        print(f"Running {command}")
                        run_code = subprocess.call(command, shell=True)
                        numberCurrentTest = (
                            entrada.split("/")[-1]
                            .replace("entrada", "")
                            .replace(".txt", "")
                        )
                        if run_code == 0:
                            print(
                                f"{GREEN}Execution successful of test {numberCurrentTest}!{RESET}"
                            )
                        else:
                            print(
                                f"{RED}Execution failed of test {numberCurrentTest}!{RESET}"
                            )
                        # Check if there are output files
                        if os.path.exists(ex_path + "/saidascorretas"):
                            print(f"{BLUE}Checking Output files..{RESET}")
                            # Get the output files
                            saidas_txt = getSaidas(ex_path)
                            minhaSaidaAtual = entrada.split("/")[-1].replace(
                                "entrada", "saida"
                            )
                            saidaCorretaAtual = "saidascorretas/" + entrada.split("/")[
                                -1
                            ].replace("entrada", "saida")
                            if os.path.exists(
                                ex_path + "/" + "saidascorretas/" + minhaSaidaAtual
                            ):
                                check_output = subprocess.Popen(
                                    "diff -wB "
                                    + ex_path
                                    + "/"
                                    + minhaSaidaAtual
                                    + " "
                                    + ex_path
                                    + "/"
                                    + saidaCorretaAtual,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                )
                                check_output.wait()
                                # Check if the output files are the same
                                if not check_output.returncode:
                                    print(
                                        f"{GREEN} PASSED!{RESET} {minhaSaidaAtual} and {saidaCorretaAtual} are the same!\n"
                                    )
                                    success[entrada.split("/")[-1].split(".")[0]] = True
                                else:
                                    success[entrada.split("/")[-1].split(".")[0]] = (
                                        False
                                    )
                                    write_report(report, check_output, entrada)
                                    print(
                                        f"{RED}FAILED!{RESET} {minhaSaidaAtual} and {saidaCorretaAtual} are NOT the same!\n"
                                    )
                            else:
                                print(f"{RED}Output files not found!\n{RESET}")
                        else:
                            print(f"{RED}Output directory not found!\n{RESET}")
                else:
                    print(f"{RED}Input files found!{RESET}")
        else:
            print(f"{RED}No C code found!{RESET} ")
else:
    print(f"\n{YELLOW}Running exercise {args.number}...{RESET}")
    ex_path = None
    for ex in ex_paths:
        numberofEX = int(re.findall(r"(\d+)", ex)[0])
        if numberofEX == args.number:
            print(f"{GREEN}Exercise found!{RESET}")
            ex_path = ex
            break
        else:
            continue
    if not ex_path:
        print(f"{RED}Exercise not found!{RESET}")
        raise Exception("Exercise not found!")
    nome_ex = ex_path.split("/")[-1]
    print(f"{YELLOW}Processing {nome_ex}{RESET}\n")
    files_in_exDIR = get_all_files(ex_path)
    c_code = None
    for file in files_in_exDIR:
        if re.findall(r"^ex\d+\.c$", file.split("/")[-1]):
            c_code = file
            break
    if c_code:
        print(f"{GREEN}C code found! {RESET} {c_code.split('/')[-1]}")
        if compileC(c_code):
            executable = c_code.replace(".c", "")
            print(f"{YELLOW}Checking Input files...{RESET}\n")
            if os.path.exists(ex_path + "/entradas"):
                entradas_txt = getEntradas(ex_path)
                for entrada in entradas_txt:
                    minha_saidaPATH = (
                        ex_path
                        + "/"
                        + entrada.split("/")[-1].replace("entrada", "saida")
                    )
                    command = executable + " < " + entrada + " > " + minha_saidaPATH
                    print(f"Running {command}")
                    run_code = subprocess.call(command, shell=True)
                    numberCurrentTest = (
                        entrada.split("/")[-1]
                        .replace("entrada", "")
                        .replace(".txt", "")
                    )
                    if run_code == 0:
                        print(
                            f"{GREEN}Execution successful of test {numberCurrentTest}!{RESET}"
                        )
                    else:
                        print(
                            f"{RED}Execution failed of test {numberCurrentTest}!{RESET}"
                        )
                    if os.path.exists(ex_path + "/saidascorretas"):
                        print(f"{BLUE}Checking Output files..{RESET}")
                        saidas_txt = getSaidas(ex_path)
                        minhaSaidaAtual = entrada.split("/")[-1].replace(
                            "entrada", "saida"
                        )
                        saidaCorretaAtual = "saidascorretas/" + entrada.split("/")[
                            -1
                        ].replace("entrada", "saida")
                        if os.path.exists(
                            ex_path + "/" + "saidascorretas/" + minhaSaidaAtual
                        ):
                            check_output = subprocess.Popen(
                                "diff -wB "
                                + ex_path
                                + "/"
                                + minhaSaidaAtual
                                + " "
                                + ex_path
                                + "/"
                                + saidaCorretaAtual,
                                shell=True,
                                stdout=subprocess.PIPE,
                            )
                            check_output.wait()
                            if not check_output.returncode:
                                print(
                                    f"{GREEN} PASSED!{RESET} {minhaSaidaAtual} and {saidaCorretaAtual} are the same!\n"
                                )
                                success[entrada.split("/")[-1].split(".")[0]] = True
                            else:
                                success[entrada.split("/")[-1].split(".")[0]] = False
                                write_report(report, check_output, entrada)
                                print(
                                    f"{RED}FAILED!{RESET} {minhaSaidaAtual} and {saidaCorretaAtual} are NOT the same!\n"
                                )
                        else:
                            print(f"{RED}Output files not found!\n{RESET}")
                            raise Exception("Output files not found!")
                    else:
                        print(f"{RED}Output directory not found!\n{RESET}")
                        raise Exception("Output directory not found!")
            else:
                print(f"{RED}Input files found!{RESET}")
                raise Exception("No input files found!")
    else:
        print(f"{RED}No C code found!{RESET} ")
        raise Exception("No C code found!")

print(f"{YELLOW}Results:{RESET}")
print(f"Total: {len(success)} tests")
success = OrderedDict(sorted(success.items(), key=lambda x: extract_digits(x[0])))
failed_tests = [
    re.findall(r"entrada(\d+)", key)[0] for key, value in success.items() if not value
]
passed_tests = [
    re.findall(r"entrada(\d+)", key)[0] for key, value in success.items() if value
]
print(f"{RED}{len(failed_tests)} tests failed: {', '.join(failed_tests)}{RESET}")
print(f"{GREEN}{len(passed_tests)} tests passed: {', '.join(passed_tests)}{RESET}")
report.close()

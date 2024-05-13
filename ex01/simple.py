import os
import re
import subprocess

#!/usr/bin/env python3

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


success = []
report = open("diff.txt", "w")


def compileC(c_code):
    call_string = "gcc " + c_code + " -o " + c_code.replace(".c", "")
    return_code = subprocess.call(call_string, shell=True)
    if return_code == 0:
        print(f"Compilation {GREEN}successful!{RESET}\n")
        return 1
    else:
        print(f"Compilation {RED}failed!{RESET}\n")
        return 0


def write_report(reportFile, message, entrada):
    reportFile.write(
        f"-> O arquivo de saida gerado pelo seu programa {entrada.split('/')[-1].replace('entrada','saida')} e o arquivo de saida correta { 'saidascorretas/' + entrada.split('/')[-1].replace('entrada','saida')} sao diferentes.\n"
    )
    report.write(message.communicate()[0].decode())


c_code = "/path/to/ex01.c"  # Substitua pelo caminho do arquivo C específico que você deseja testar
executable = c_code.replace(".c", "")
compileC(c_code)

entrada = "/path/to/entrada.txt"  # Substitua pelo caminho do arquivo de entrada específico que você deseja testar
minha_saidaPATH = "/path/to/minha_saida.txt"  # Substitua pelo caminho do arquivo de saída gerado pelo seu programa
saidaCorretaAtual = "/path/to/saidascorretas/saida_correta.txt"  # Substitua pelo caminho do arquivo de saída correta

command = executable + " < " + entrada + " > " + minha_saidaPATH
print(f"Running {command}")
run_code = subprocess.call(command, shell=True)

if run_code == 0:
    print(f"{GREEN}Execution successful!{RESET}")
else:
    print(f"{RED}Execution failed!{RESET}")

print(f"{BLUE}Checking Output files..{RESET}")
check_output = subprocess.Popen(
    "diff -wB " + minha_saidaPATH + " " + saidaCorretaAtual,
    shell=True,
    stdout=subprocess.PIPE,
)
check_output.wait()
if not check_output.returncode:
    print(
        f"{GREEN} PASSED!{RESET} {minha_saidaPATH} and {saidaCorretaAtual} are the same!\n"
    )
    success.append(1)
else:
    success.append(0)
    write_report(report, check_output, entrada)
    print(
        f"{RED}FAILED!{RESET} {minha_saidaPATH} and {saidaCorretaAtual} are NOT the same!\n"
    )

report.close()

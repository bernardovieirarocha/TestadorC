# PyCTestador - Testador de Códigos em C com Python

Este é um projeto em Python que testa códigos em C para a disciplina de Algoritmos e Estrutura de Dados. Ele permite testar os códigos com entradas específicas e verificar se as saídas geradas estão corretas.

## Como Usar

1. Clone o repositório para a sua máquina local.
2. Coloque os códigos em C que deseja testar em pastas `ex**`
3. Dentro de cada pasta  `ex**` crie as pastas entradas e saidascorretas e insira nelas `entradas*.txt` e `saidas*.txt`
4. Execute o arquivo `tester.py` para rodar os testes no root das pastas `ex**`, ou seja junto com elas, ao lado.
5. Verifique os resultados na saída do terminal e no arquivo diff.txt a ser criado que detalha as diferenças.

## Estrutura do Projeto

- `ex**/`: Pasta para armazenar os códigos em C.
  - `entradas` Pasta que contém os std_in **.txt dos testes.
  - `saidascorretas` Pasta que contém os std_out **.txt esperado dos testes.
- `tester.py`: Compilar e Executar todos os testes de todos os exercícios.
- `simple.py`: Compilar Executar os testes em somente um exercício.

## Exemplo da Estrutura
<img width="283" alt="image" src="https://github.com/bernardovieirarocha/TestadorC/assets/64905090/e0838d1e-31e5-44dc-8729-eb1fc2856fcc">



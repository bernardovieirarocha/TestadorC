# PyCTestador - Testador de Códigos em C com Python
Este é um projeto em Python que testa códigos em C para a disciplina de Algoritmos e Estrutura de Dados. Ele permite testar os códigos com entradas específicas e verificar se as saídas geradas estão corretas.

## Como Usar

1. Clone o repositório para a sua máquina local.
2. Coloque os códigos em C que deseja testar em pastas `ex**`
3. Dentro de cada pasta  `ex**` crie as pastas entradas e saidascorretas e insira nelas `entradas*.txt` e `saidas*.txt`
4. Execute o arquivo `tester.py` para compilar e rodar os testes.
5. Verifique os resultados na saída do terminal e no arquivo diff.txt a ser criado que detalha as diferenças.

### Execução do código
O `tester.py` agora possui argumentos e parâmetros para maior flexibilidade na execução dos testes.

O `tester.py` agora possui argumentos e parâmetros para maior flexibilidade na execução dos testes.

**Uso:**

```
tester.py [-h] [diretório] [número]
```

**Argumentos Posicionais: (OPCIONAIS)**

* `diretório`: Diretório dos testes a serem executados.
* `número`: Número do exercício a ser testado (ou -1 para todos os exercícios).
* `-h`, `--help`: Exibe esta mensagem de ajuda e sai.

**Exemplo de Uso:**

* Executar todos os testes no diretório atual da pasta `ex01`:

```
python tester.py ./ 1
```

* Executar todos os testes de todas as pastas no diretório atual:

```
python tester.py 
```


## Estrutura do Projeto

- `ex**/`: Pasta para armazenar os códigos em C.
  - `entradas` Pasta que contém os stdin **.txt dos testes.
  - `saidascorretas` Pasta que contém os std_out **.txt esperado dos testes.
- `tester.py`: Compilar e Executar os testes desejados.

## Exemplo da Estrutura
<img width="355" alt="image" src="https://github.com/bernardovieirarocha/TestadorC/assets/64905090/32963572-6c10-431b-a20f-436256a20c18">


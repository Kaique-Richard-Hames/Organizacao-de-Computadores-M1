import os
from collections import defaultdict


def bin_to_uint(bin_str):
    return int(bin_str, 2)


def tem_extensao_txt(nome_arquivo):
    return nome_arquivo.lower().endswith('.txt')


def decodificar_riscv(instr):
    opcode = instr & 0x7F

    if opcode == 0x33:  # R-type
        funct3 = (instr >> 12) & 0x7
        funct7 = (instr >> 25) & 0x7F
        if funct3 == 0x0 and funct7 == 0x00:
            return ("add", 4)
        elif funct3 == 0x0 and funct7 == 0x20:
            return ("sub", 4)
        else:
            return ("r-type", 4)
    elif opcode == 0x13:
        return ("addi", 4)
    elif opcode == 0x03:
        return ("lw", 5)
    elif opcode == 0x23:
        return ("sw", 4)
    elif opcode == 0x63:
        return ("branch", 3)
    elif opcode == 0x6F:
        return ("jal", 3)
    elif opcode == 0x17:
        return ("auipc", 3)
    elif opcode == 0x37:
        return ("lui", 3)
    elif opcode == 0x67:
        return ("jalr", 3)
    else:
        return ("unknown", 0)


ciclos_por_instrucao = {
    "add": 4,
    "sub": 4,
    "r-type": 4,
    "addi": 4,
    "lw": 5,
    "sw": 4,
    "branch": 3,
    "jal": 3,
    "jalr": 3,
    "auipc": 3,
    "lui": 3,
    "unknown": 0
}


def main():
    caminho = input("Digite o caminho do arquivo binário RISC-V: ").strip()
    print("\nArquitetura utilizada: RISC-V (não contempla MIPS-I)")

    if not tem_extensao_txt(caminho):
        print("Erro: o arquivo precisa ter a extensão .txt")
        return

    if not os.path.isfile(caminho):
        print(f"Erro: não foi possível abrir o arquivo '{caminho}'")
        return

    contagem_instr = {}
    total_ciclos = 0
    total_instr = 0

    with open(caminho, 'r') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue

            instr = bin_to_uint(linha)
            nome, ciclos = decodificar_riscv(instr)

            contagem_instr[nome] = contagem_instr.get(nome, 0) + 1
            total_ciclos += ciclos
            total_instr += 1

    cpi = total_ciclos / total_instr if total_instr > 0 else 0

    print("\nRelatório de Instruções:")
    for nome, qtd in contagem_instr.items():
        print(f"  {nome}: {qtd} vezes")

    print(f"Total de instruções: {total_instr}")

    classificacao_por_ciclo = defaultdict(list)
    for nome, qtd in contagem_instr.items():
        ciclos = ciclos_por_instrucao.get(nome, 0)
        classificacao_por_ciclo[ciclos].append((nome, qtd))

    print("\nClassificação por número de ciclos:")
    for ciclo, lista in sorted(classificacao_por_ciclo.items()):
        print(f"  {ciclo} ciclos:")
        for nome, qtd in lista:
            print(f"    {nome}: {qtd} vezes")

    print(f"CPI médio: {cpi:.2f}")
    print("\nOrganização multiciclo adotada: baseada na arquitetura multiciclo do livro 'Computer Organization and Design' de Patterson & Hennessy (5ª edição), conforme os slides do professor.")

if __name__ == "__main__":
    main()

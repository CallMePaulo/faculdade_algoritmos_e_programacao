import os

if os.name == "nt":  # 'nt' é para Windows
    comando_limpar = "cls"
else:  # 'posix' para Linux e macOS
    comando_limpar = "clear"


# Lista onde cada item é um dicionário representando uma transação.
movimentacoes = []


def menu():
    _ = os.system(comando_limpar)
    print("""-------------------------------------
Olá, seja bem vindo!
Escolha uma das opções abaixo:
    (1): Registrar Movimentação
    (2): Acompanhar Saldo
    (3): Sair
-------------------------------------""")
    return opcao()


def opcao():
    try:
        opcao = int(input("Opção desejada: "))
    except ValueError:
        print("Entrada inválida! Digite apenas o número da opção.")
        return True

    # Inicializa 'rodando' como True por padrão (continua rodando)
    rodando = True

    match opcao:
        case 1:
            registrar_movimentacao()
        case 2:
            acompanhar_saldo()
        case 3:
            rodando = False
            print("\nVocê selecionou a opção Sair")
            print("Obrigado por usar nosso sistema. Encerrando.")
        case _:
            print("\nOpção Inválida! Selecione uma das opções disponíveis.")
            pass

    # Retorna o valor de 'rodando' (True ou False)
    return rodando


def registrar_movimentacao():
    _ = os.system(comando_limpar)
    print("--- REGISTRAR NOVA MOVIMENTAÇÃO ---")

    # Coleta os dados necessários
    while True:
        print("Tipo de Movimentação:")
        tipo = input("Digite R para Receita e D para Despesa: ").upper()
        if tipo in ["R", "D"]:
            tipo_completo = "Receita" if tipo == "R" else "Despesa"
            break
        else:
            print("Tipo inválido. Por favor, digite R ou D")

    descricao = input("Descrição da Transação: ")
    try:
        valor = float(input("Valor da Transação (ex: 100.00): "))
    except ValueError:
        print("Valor inválido. Por favor, digite um número.")
        return  # Sai da função se o valor for inválido
    categoria = input("Categoria (ex: Receita, Salário, Alimentação, Transporte): ")
    data = input("Data da Transação (DD/MM/AAAA): ")

    valor_formatado = f"{valor:.2f}"

    # Cria o dicionário com os dados da movimentação
    nova_transacao = {
        "tipo": tipo_completo,
        "descricao": descricao,
        "valor": valor_formatado,
        "categoria": categoria,
        "data": data,
    }

    # Adiciona o dicionário à lista de movimentações
    movimentacoes.append(nova_transacao)

    print("\n✅ Movimentação Registrada com Sucesso!")

    _ = input("Pressione qualquer botão para voltar ao menu inicial.")


def acompanhar_saldo():
    _ = os.system(comando_limpar)
    # Calcula o saldo total (Receitas - Depesas) e exibe, usando o campo 'tipo'.

    total_receitas = 0.0
    total_despesas = 0.0

    if not movimentacoes:
        print("\n🚫 Nenhuma movimentação registrada ainda. Saldo: R$0.00")

    for transacao in movimentacoes:
        # Converte a string de volta para float para realizar o cálculo
        valor = float(transacao["valor"])

        # Verifica o campo 'tipo'
        if transacao["tipo"] == "Receita":
            total_receitas += valor
        elif transacao["tipo"] == "Despesa":
            total_despesas += valor
        # Transações sem tipo válido são ignoradas

    saldo_total = total_receitas - total_despesas

    print("\n--- SALDO DISPONÍVEL ---")
    print(f"Total de Receitas: R${total_receitas:.2f}")
    print(f"Total de Despesas: R${total_despesas:.2f}")

    # Exibe o saldo em verde/vermelho (opcional, mas legal)
    cor_inicio = "\033[92m" if saldo_total >= 0 else "\033[91m"
    cor_fim = "\033[0m"

    print(f"Saldo Atual:       {cor_inicio}R${saldo_total:.2f}{cor_fim}")
    print("------------------------")

    _ = input("Pressione qualquer botão para voltar ao menu inicial.")

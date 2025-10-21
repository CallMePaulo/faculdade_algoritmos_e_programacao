import os 
from collections import defaultdict # Mantido para o agrupamento de relatórios

# --- Configuração de Sistema ---

if os.name == "nt": 
    comando_limpar = "cls"
else:
    comando_limpar = "clear"

# Lista global onde cada item é um dicionário.
# **A PERSISTÊNCIA AGORA É APENAS EM MEMÓRIA**
movimentacoes = [] 

# ==========================================================
# 1. FUNÇÕES DE PERSISTÊNCIA (REMOVIDAS / SIMPLIFICADAS)
#    As funções de DB foram removidas. Os dados são salvos
#    diretamente na lista 'movimentacoes' e PERDEM-SE
#    ao fechar o programa.
# ==========================================================


# ==========================================================
# 2. FUNÇÕES DE MENU E NAVEGAÇÃO
# ==========================================================

def menu():
    """Exibe o menu principal e retorna a próxima opção de execução."""
    _ = os.system(comando_limpar)
    print("""-------------------------------------
Olá, seja bem vindo!
Escolha uma das opções abaixo:
    (1): Registrar Movimentação
    (2): Acompanhar Saldo
    (3): Relatórios e Análises
    (4): Sair
-------------------------------------""")
    return opcao()


def opcao():
    """Lê a opção e chama a função correspondente."""
    try:
        opcao = int(input("Opção desejada: "))
    except ValueError:
        print("Entrada inválida! Digite apenas o número da opção.")
        return True

    rodando = True

    match opcao:
        case 1:
            registrar_movimentacao()
        case 2:
            acompanhar_saldo()
        case 3:
            relatorios_e_analises_menu()
        case 4:
            rodando = False
            print("\nVocê selecionou a opção Sair")
            print("Obrigado por usar nosso sistema. Encerrando.")
        case _:
            print("\nOpção Inválida! Selecione uma das opções disponíveis.")
            pass

    return rodando

# ==========================================================
# 3. FUNÇÕES DE REGISTRO E CÁLCULO
# ==========================================================

def registrar_movimentacao():
    _ = os.system(comando_limpar)
    print("--- REGISTRAR NOVA MOVIMENTAÇÃO ---")

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
        return  
    
    categoria = input("Categoria (ex: Salário, Alimentação, Transporte): ").strip()
    data = input("Data da Transação (DD/MM/AAAA): ")

    valor_formatado = f"{valor:.2f}"

    nova_transacao = {
        "tipo": tipo_completo,
        "descricao": descricao,
        "valor": valor_formatado, # String formatada
        "categoria": categoria,
        "data": data,
    }

    # **MUDANÇA CRÍTICA:** Adiciona à lista diretamente, sem DB.
    movimentacoes.append(nova_transacao)
    
    print("\n✅ Movimentação Registrada com Sucesso (Memória)! (Será perdida ao fechar o programa)")
    
    _ = input("Pressione qualquer botão para voltar ao menu inicial.")


def acompanhar_saldo():
    _ = os.system(comando_limpar)

    total_receitas = 0.0
    total_despesas = 0.0

    if not movimentacoes:
        print("\n🚫 Nenhuma movimentação registrada ainda. Saldo: R$0.00")
        _ = input("Pressione qualquer botão para voltar ao menu inicial.")
        return

    for transacao in movimentacoes:
        # Converte de string para float para o cálculo
        valor = float(transacao["valor"])

        if transacao["tipo"] == "Receita":
            total_receitas += valor
        elif transacao["tipo"] == "Despesa":
            total_despesas += valor

    saldo_total = total_receitas - total_despesas

    print("\n--- SALDO DISPONÍVEL ---")
    print(f"Total de Receitas: R${total_receitas:.2f}")
    print(f"Total de Despesas: R${total_despesas:.2f}")

    cor_inicio = "\033[92m" if saldo_total >= 0 else "\033[91m"
    cor_fim = "\033[0m"

    print(f"Saldo Atual:       {cor_inicio}R${saldo_total:.2f}{cor_fim}")
    print("------------------------")

    _ = input("Pressione qualquer botão para voltar ao menu inicial.")


# ==========================================================
# 4. FUNÇÕES DE RELATÓRIO E ANÁLISE (DB AUXILIAR REMOVIDO)
# ==========================================================

def relatorios_e_analises_menu():
    """Exibe o sub-menu de relatórios e análises."""
    _ = os.system(comando_limpar)
    
    if not movimentacoes:
        print("\n🚫 Não há movimentações para gerar relatórios ou estatísticas.")
        _ = input("Pressione qualquer botão para voltar ao menu inicial.")
        return 

    while True:
        print("""
--- SUB-MENU DE RELATÓRIOS E ANÁLISES ---
Escolha o tipo de análise:
    (1): Relatório Detalhado por Categoria
    (2): Estatísticas Mensais (Ainda a Implementar)
    (3): Voltar ao Menu Principal
-----------------------------------------""")
        
        try:
            sub_opcao = int(input("Opção desejada: "))
        except ValueError:
            print("\nEntrada inválida! Digite apenas o número da opção.")
            continue

        match sub_opcao:
            case 1:
                relatorio_por_categoria() 
            case 2:
                print("\nFunção de Estatísticas ainda a ser implementada.")
                _ = input("Pressione qualquer botão para continuar.")
            case 3:
                return 
            case _:
                print("\nOpção Inválida! Selecione uma das opções disponíveis.")


def relatorio_por_categoria():
    """Gera e exibe o relatório detalhado de movimentações agrupadas por categoria."""
    _ = os.system(comando_limpar)
    print("--- RELATÓRIO DETALHADO POR CATEGORIA ---")
    
    # 1. AGRUPAMENTO POR CATEGORIA (Usando defaultdict)
    movimentacoes_por_categoria = defaultdict(list)
    for mov in movimentacoes:
        categoria = mov['categoria'].strip()
        movimentacoes_por_categoria[categoria].append(mov)

    Larg = 80
    larg = 15 

    if not movimentacoes_por_categoria:
        print("\nNenhuma movimentação para relatar.")
        _ = input("Pressione qualquer botão para voltar ao menu de Análises.")
        return

    # 2. ITERAR E GERAR RELATÓRIO PARA CADA CATEGORIA
    for categoria_nome, lista_de_movs in movimentacoes_por_categoria.items():
        
        # --- TÍTULO DINÂMICO ---
        titulo_relatorio = f"RELATÓRIO DE MOVIMENTAÇÕES: {categoria_nome.upper()}"
        print("\n" + "=" * Larg)
        print(titulo_relatorio.center(Larg))
        print("=" * Larg)

        # Cabeçalho da Tabela
        nome_colunas_exibir = ['TIPO', 'DESCRIÇÃO', 'VALOR', 'DATA']
        tamanho_cabecalho = larg * len(nome_colunas_exibir) + (len(nome_colunas_exibir) - 1) * 3
        
        cabeçalho = f'{nome_colunas_exibir[0].center(larg)} | {nome_colunas_exibir[1].center(larg)} | {nome_colunas_exibir[2].center(larg)} | {nome_colunas_exibir[3].center(larg)}'
        
        print(cabeçalho)
        print('-' * tamanho_cabecalho)

        # Exibição dos Registros
        for mov in lista_de_movs:
            # Dados são lidos diretamente do dicionário (mov)
            larg_tip = str(mov['tipo']).center(larg)
            larg_des = str(mov['descricao']).center(larg)
            
            # O valor já está como string formatada em R$X.XX
            valor_formatado = f"R${mov['valor']}"
            larg_val = valor_formatado.center(larg)
            
            larg_dat = str(mov['data']).center(larg)
            
            dados_form = f"{larg_tip} | {larg_des} | {larg_val} | {larg_dat}"
            print(dados_form)
        
        print("-" * tamanho_cabecalho + "\n")

    # Ponto de parada necessário para o utilizador ler o relatório
    _ = input("Relatórios concluídos. Pressione qualquer botão para voltar ao menu de Análises.")

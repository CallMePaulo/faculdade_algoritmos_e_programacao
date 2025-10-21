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
    _ = input("Relatórios concluídos. Pressione qualquer botão para voltar ao menu de Análises.")    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        if con:
            con.close()

def carregar_dados_do_db():
    """Carrega todos os registros do banco de dados principal para a lista 'movimentacoes'."""
    global movimentacoes
    movimentacoes = []
    
    try:
        con = sqlite3.connect(NOME_DO_BANCO_PRINCIPAL)
        cursor = con.cursor()
        cursor.execute("SELECT tipo, descricao, valor, categoria, data FROM movimentos ORDER BY id DESC")
        dados = cursor.fetchall()
        
        for dado in dados:
            movimentacoes.append({
                "tipo": dado[0],
                "descricao": dado[1],
                "valor": f"{dado[2]:.2f}",
                "categoria": dado[3],
                "data": dado[4]
            })
        print(f"✅ {len(movimentacoes)} registros carregados do banco de dados.")

    except sqlite3.Error as e:
        print(f"Erro ao carregar dados do banco: {e}")
    finally:
        if con:
            con.close()

def salvar_movimentacao_no_db(mov):
    """Salva uma única movimentação no banco de dados principal."""
    try:
        con = sqlite3.connect(NOME_DO_BANCO_PRINCIPAL)
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO movimentos (tipo, descricao, valor, categoria, data) VALUES (?, ?, ?, ?, ?)",
            (mov['tipo'], mov['descricao'], float(mov['valor']), mov['categoria'], mov['data'])
        )
        con.commit()
        return True
    except sqlite3.Error as e:
        print(f"\n🚫 ERRO ao salvar no DB: {e}")
        return False
    finally:
        if con:
            con.close()
            
def limpar_tabela(nome_tabela):
    """Limpa a tabela auxiliar (relatorio), garantindo o COMMIT na ordem correta."""
    try:
        con = sqlite3.connect('relatorio.db')
        cursor = con.cursor()
        
        cursor.execute(f'DELETE FROM {nome_tabela}')
        con.commit() # COMMIT DEPOIS DO DELETE
        
    except sqlite3.OperationalError as e:
        print(f'Falha no sistema ao limpar tabela: {e}')
    
    finally:
        if con:
            con.close()

# ==========================================================
# 2. FUNÇÕES DE MENU E NAVEGAÇÃO
# ==========================================================

def menu():
    """Exibe o menu e retorna a próxima opção de execução."""
    _ = os.system(comando_limpar)
    print("""-------------------------------------
Olá, seja bem vindo!
Escolha uma das opções abaixo:
    (1): Registrar Movimentação
    (2): Acompanhar Saldo
    (3): Relatórios
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
            relatorios()
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
        "valor": valor_formatado,
        "categoria": categoria,
        "data": data,
    }

    # 1. Salva no Banco de Dados Principal
    if salvar_movimentacao_no_db(nova_transacao):
        # 2. Adiciona à lista em memória APENAS se salvou no DB
        movimentacoes.append(nova_transacao)
        print("\n✅ Movimentação Registrada e Salva com Sucesso!")
    
    _ = input("Pressione qualquer botão para voltar ao menu inicial.")


def acompanhar_saldo():
    _ = os.system(comando_limpar)

    total_receitas = 0.0
    total_despesas = 0.0

    if not movimentacoes:
        print("\n🚫 Nenhuma movimentação registrada ainda. Saldo: R$0.00")

    for transacao in movimentacoes:
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
# 4. FUNÇÕES DE RELATÓRIO
# ==========================================================

def relatorios():
    _ = os.system(comando_limpar)
    print("--- RELATÓRIOS ---")

    if not movimentacoes:
        print("\n🚫 Não há movimentações para gerar relatórios.")
        _ = input("Pressione qualquer botão para voltar ao menu inicial.")
        return 

    # 2. AGRUPAMENTO POR CATEGORIA 
    movimentacoes_por_categoria = defaultdict(list)
    for mov in movimentacoes:
        categoria = mov['categoria'].strip()
        movimentacoes_por_categoria[categoria].append(mov)

    # Conecta ou cria o DB auxiliar
    con = sqlite3.connect('relatorio.db')
    cursor = con.cursor()
    
    try:
        # A. Criação da tabela auxiliar (staging)
        cursor.execute("CREATE TABLE IF NOT EXISTS relatorio (tipo TEXT, descricao TEXT, valor REAL, data TEXT, categoria TEXT)")
        con.commit()

        Larg = 80
        larg = 15 

        # 3. ITERAR E GERAR RELATÓRIO PARA CADA CATEGORIA
        for categoria_nome, lista_de_movs in movimentacoes_por_categoria.items():
            
            # --- TÍTULO DINÂMICO ---
            titulo_relatorio = f"RELATÓRIO DE MOVIMENTAÇÕES: {categoria_nome.upper()}"
            print("\n" + "=" * Larg)
            print(titulo_relatorio.center(Larg))
            print("=" * Larg)

            # B. Limpa a tabela para o relatório da categoria atual
            limpar_tabela('relatorio') 

            # C. Inserção dos dados da categoria ATUAL
            for mov in lista_de_movs:
                cursor.execute(
                    "INSERT INTO relatorio(tipo, descricao, valor, data, categoria) VALUES (?, ?, ?, ?, ?)",
                    (mov['tipo'], mov['descricao'], float(mov['valor']), mov['data'], mov['categoria'])
                )
            con.commit()
            
            # D. Busca e Exibição dos Dados da Categoria Atual
            cursor.execute('''SELECT tipo, descricao, valor, data FROM relatorio''') 
            dados = cursor.fetchall()
            
            # Cabeçalho da Tabela
            nome_colunas_exibir = ['TIPO', 'DESCRIÇÃO', 'VALOR', 'DATA']
            tamanho_cabecalho = larg * len(nome_colunas_exibir) + (len(nome_colunas_exibir) - 1) * 3
            
            cabeçalho = f'{nome_colunas_exibir[0].center(larg)} | {nome_colunas_exibir[1].center(larg)} | {nome_colunas_exibir[2].center(larg)} | {nome_colunas_exibir[3].center(larg)}'
            
            print(cabeçalho)
            print('-' * tamanho_cabecalho)

            # Exibição dos Registros
            # Exibição dos Registros
           # Exibição dos Registros
            for registro in dados:
                # Registro: (tipo, descricao, valor, data)
                larg_tip = str(registro[0]).center(larg)
                larg_des = str(registro[1]).center(larg)
                
                # CORREÇÃO: Formatação do valor para R$XX.XX e centralização
                # Esta é a parte que resolve o seu SyntaxError e garante a formatação.
                valor_formatado = f"R${registro[2]:.2f}"
                larg_val = valor_formatado.center(larg)
                
                larg_dat = str(registro[3]).center(larg)
                
                dados_form = f"{larg_tip} | {larg_des} | {larg_val} | {larg_dat}"
                print(dados_form)
            
            print("-" * tamanho_cabecalho + "\n")

        # 4. Finalização
        _ = input("Relatórios concluídos. Pressione qualquer botão para voltar ao menu inicial.")

    except sqlite3.Error as e:
        print(f"Ocorreu um erro no banco de dados: {e}")
        _ = input("Pressione qualquer botão para voltar ao menu inicial.")
        
    finally:
        limpar_tabela('relatorio')
        cursor.close()
        con.close()


import os
import json
import datetime 
from collections import defaultdict 

if os.name == "nt": 
    comando_limpar = "cls"
else:
    comando_limpar = "clear"

movimentacoes = [] 
NOME_ARQUIVO_DADOS = "movimentacoes.json" 

def validar_data(prompt):
    """Solicita e valida uma data no formato DD/MM/AAAA."""
    while True:
        data_str = input(prompt).strip()
        try:
            data_obj = datetime.datetime.strptime(data_str, '%d/%m/%Y').date()
            return data_obj, data_str
        except ValueError:
            print("Formato de data inválido. Use DD/MM/AAAA (ex: 25/10/2025).")

def carregar_dados():
    global movimentacoes
    try:
        if os.path.exists(NOME_ARQUIVO_DADOS):
            with open(NOME_ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
                movimentacoes = json.load(f)
            print(f"✅ {len(movimentacoes)} movimentações carregadas de {NOME_ARQUIVO_DADOS}")
    except (FileNotFoundError, json.JSONDecodeError):
        movimentacoes = []
        
def salvar_dados():
    global movimentacoes
    try:
        with open(NOME_ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
            json.dump(movimentacoes, f, indent=4)
        return True
    except IOError as e:
        print(f"❌ Erro ao salvar dados no arquivo {NOME_ARQUIVO_DADOS}: {e}")
        return False

def salvar_relatorio_txt(conteudo, nome_arquivo="relatorio_financeiro.txt"):
    """
    Salva o conteúdo fornecido (string) em um arquivo de texto.
    (Esta função é para RELATÓRIOS, e não para persistência de dados principais)
    """
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(conteudo)
        print(f"\n✅ Relatório salvo com sucesso em: {nome_arquivo}")
        return True
    except IOError as e:
        print(f"\n❌ Erro ao salvar o arquivo {nome_arquivo}: {e}")
        return False

def menu():
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
            salvar_dados()
            rodando = False
            print("\nVocê selecionou a opção Sair")
            print("Obrigado por usar nosso sistema. Encerrando.")
        case _:
            print("\nOpção Inválida! Selecione uma das opções disponíveis.")
            pass

    return rodando

def registrar_movimentacao():
    os.system(comando_limpar)
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
    _, data = validar_data("Data da Transação (DD/MM/AAAA): ")

    valor_formatado = f"{valor:.2f}"

    nova_transacao = {
        "tipo": tipo_completo,
        "descricao": descricao,
        "valor": valor_formatado, 
        "categoria": categoria,
        "data": data, 
    }
    
    movimentacoes.append(nova_transacao)
    
    if salvar_dados():
        print(f"\n✅ Movimentação Registrada e Salva com Sucesso no arquivo {NOME_ARQUIVO_DADOS}!")
    else:
        print("\n✅ Movimentação Registrada! ❌ Atenção: Falha ao salvar os dados no arquivo.")

    
    _ = input("Pressione qualquer botão para voltar ao menu inicial.")


def acompanhar_saldo():
    os.system(comando_limpar)

    total_receitas = 0.0
    total_despesas = 0.0

    if not movimentacoes:
        print("\n🚫 Nenhuma movimentação registrada ainda. Saldo: R$0.00")
        _ = input("Pressione qualquer botão para voltar ao menu inicial.")
        return

    for transacao in movimentacoes:
        
        valor = float(transacao["valor"])

        if transacao["tipo"] == "Receita":
            total_receitas += valor
        elif transacao["tipo"] == "Despesa":
            total_despesas += valor

    saldo_total = total_receitas - total_despesas

    relatorio_str = "\n--- SALDO DISPONÍVEL ---\n"
    relatorio_str += f"Total de Receitas: R${total_receitas:.2f}\n"
    relatorio_str += f"Total de Despesas: -R${total_despesas:.2f}\n" 
    relatorio_str += "------------------------\n"
    
    saldo_formatado = f"R${saldo_total:.2f}"
    relatorio_str += f"Saldo Atual:       {saldo_formatado}\n"
    
    cor_inicio = "\033[92m" if saldo_total >= 0 else "\033[91m"
    cor_fim = "\033[0m"

    print(relatorio_str.replace(f"Saldo Atual:       {saldo_formatado}", 
                                f"Saldo Atual:       {cor_inicio}{saldo_formatado}{cor_fim}").strip())

    salvar = input("\nDeseja salvar este Saldo em um arquivo TXT? (S/N): ").upper()
    if salvar == 'S':
        data_atual = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"saldo_disponivel_{data_atual}.txt"
        salvar_relatorio_txt(relatorio_str, nome_arquivo)

    _ = input("\nPressione qualquer botão para voltar ao menu inicial.")


def relatorios_e_analises_menu():
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
    (2): Estatísticas Mensais (Médias)
    (3): Análise por Período de Tempo   
    (4): Voltar ao Menu Principal
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
                gerar_estatisticas() 
            case 3:
                relatorio_por_periodo() 
            case 4:
                return 
            case _:
                print("\nOpção Inválida! Selecione uma das opções disponíveis.")

def relatorio_por_periodo():
    os.system(comando_limpar)
    
    print("--- RELATÓRIO DE ANÁLISE POR PERÍODO ---")
    
    data_inicio_obj, data_inicio_str = validar_data("Digite a Data de INÍCIO (DD/MM/AAAA): ")
    data_fim_obj, data_fim_str = validar_data("Digite a Data de FIM (DD/MM/AAAA): ")
    
    if data_fim_obj < data_inicio_obj:
        print("\n🚫 Erro: A data de FIM não pode ser anterior à data de INÍCIO.")
        _ = input("Pressione qualquer botão para voltar ao menu de Análises.")
        return
    
    movimentacoes_filtradas = []
    total_receitas = 0.0
    total_despesas = 0.0
    
    for mov in movimentacoes:
        try:
            data_mov_obj = datetime.datetime.strptime(mov['data'], '%d/%m/%Y').date()
            
            if data_inicio_obj <= data_mov_obj <= data_fim_obj:
                movimentacoes_filtradas.append(mov)
                valor = float(mov['valor'])
                
                if mov['tipo'] == 'Receita':
                    total_receitas += valor
                else:
                    total_despesas += valor
                    
        except ValueError:
            continue 

    saldo_total = total_receitas - total_despesas
    
    relatorio_str = f"\nRELATÓRIO DE PERÍODO: De {data_inicio_str} a {data_fim_str}\n"
    relatorio_str += "=" * 50 + "\n"
    relatorio_str += f"TOTAL DE RECEITAS: R${total_receitas:.2f}\n"
    relatorio_str += f"TOTAL DE DESPESAS: -R${total_despesas:.2f}\n" 
    relatorio_str += "-" * 50 + "\n"
    
    saldo_formatado = f"R${saldo_total:.2f}"
    relatorio_str += f"SALDO DO PERÍODO: {saldo_formatado}\n"
    relatorio_str += "=" * 50 + "\n\n"
    
    if movimentacoes_filtradas:
        relatorio_str += "--- MOVIMENTAÇÕES DETALHADAS NO PERÍODO ---\n"
        relatorio_str += "{:<10} {:<30} {:>10}\n".format("DATA", "DESCRIÇÃO/CATEGORIA", "VALOR")
        relatorio_str += "-" * 50 + "\n"
        
        movimentacoes_filtradas.sort(key=lambda x: datetime.datetime.strptime(x['data'], '%d/%m/%Y').date())
        
        for mov in movimentacoes_filtradas:
            tipo_prefixo = "(+)" if mov['tipo'] == 'Receita' else "(-)"
            descricao_curta = f"[{mov['categoria']}] {mov['descricao']}"[:25]
            relatorio_str += "{:<10} {:<30} {:>10}\n".format(
                mov['data'],
                descricao_curta,
                f"{tipo_prefixo}R${mov['valor']}"
            )
        relatorio_str += "-" * 50 + "\n"
    else:
        relatorio_str += "🚫 Nenhuma movimentação encontrada no período especificado.\n"
        
    cor_inicio = "\033[92m" if saldo_total >= 0 else "\033[91m"
    cor_fim = "\033[0m"
    
    print(relatorio_str.replace(f"SALDO DO PERÍODO: {saldo_formatado}", 
                                f"SALDO DO PERÍODO: {cor_inicio}{saldo_formatado}{cor_fim}"))

    salvar = input("\nDeseja salvar este Relatório de Período em um arquivo TXT? (S/N): ").upper()
    if salvar == 'S':
        nome_arquivo = f"relatorio_periodo_{data_inicio_obj.strftime('%Y%m%d')}_a_{data_fim_obj.strftime('%Y%m%d')}.txt"
        salvar_relatorio_txt(relatorio_str, nome_arquivo)

    _ = input("\nPressione qualquer botão para voltar ao menu de Análises.")

def relatorio_por_categoria():
    os.system(comando_limpar)
    print("--- RELATÓRIO DETALHADO POR CATEGORIA ---")
    
    relatorio_completo_str = "RELATÓRIO DETALHADO POR CATEGORIA\n\n"

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

    for categoria_nome, lista_de_movs in movimentacoes_por_categoria.items():
        
        conteudo_categoria_str = ""
        titulo_relatorio = f"RELATÓRIO DE MOVIMENTAÇÕES: {categoria_nome.upper()}"
        
        conteudo_categoria_str += "\n" + "=" * Larg + "\n"
        conteudo_categoria_str += titulo_relatorio.center(Larg) + "\n"
        conteudo_categoria_str += "=" * Larg + "\n"

        nome_colunas_exibir = ['TIPO', 'DESCRIÇÃO', 'VALOR', 'DATA']
        tamanho_cabecalho = larg * len(nome_colunas_exibir) + (len(nome_colunas_exibir) - 1) * 3
        
        cabeçalho = f'{nome_colunas_exibir[0].center(larg)} | {nome_colunas_exibir[1].center(larg)} | {nome_colunas_exibir[2].center(larg)} | {nome_colunas_exibir[3].center(larg)}'
        
        conteudo_categoria_str += cabeçalho + "\n"
        conteudo_categoria_str += '-' * tamanho_cabecalho + "\n"

        for mov in lista_de_movs:
            larg_tip = str(mov['tipo']).center(larg)
            larg_des = str(mov['descricao']).center(larg)
            
            if mov['tipo'] == 'Despesa':
                valor_formatado = f"-R${mov['valor']}" 
            else:
                valor_formatado = f"R${mov['valor']}" 
                
            larg_val = valor_formatado.center(larg)
            
            larg_dat = str(mov['data']).center(larg)
            
            dados_form = f"{larg_tip} | {larg_des} | {larg_val} | {larg_dat}"
            conteudo_categoria_str += dados_form + "\n"
        
        conteudo_categoria_str += "-" * tamanho_cabecalho + "\n"

        print(conteudo_categoria_str)
        relatorio_completo_str += conteudo_categoria_str

    salvar = input("\nDeseja salvar o Relatório por Categoria em um arquivo TXT? (S/N): ").upper()
    if salvar == 'S':
        data_atual = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorio_por_categoria_{data_atual}.txt"
        salvar_relatorio_txt(relatorio_completo_str, nome_arquivo)

    _ = input("\nRelatórios concluídos. Pressione qualquer botão para voltar ao menu de Análises.")


def gerar_estatisticas():
    os.system(comando_limpar)
    print("--- ESTATÍSTICAS FINANCEIRAS (MÉDIAS MENSAIS) ---")

    relatorio_estatisticas_str = "ESTATÍSTICAS FINANCEIRAS (MÉDIAS MENSAIS)\n"

    totais_mensais = defaultdict(lambda: {'receita': 0.0, 'despesa': 0.0})
    
    for mov in movimentacoes:
        try:
            data_obj = datetime.datetime.strptime(mov['data'], '%d/%m/%Y')
            mes_ano = data_obj.strftime('%m/%Y')
            valor = float(mov['valor'])
            
            if mov['tipo'] == 'Receita':
                totais_mensais[mes_ano]['receita'] += valor
            elif mov['tipo'] == 'Despesa':
                totais_mensais[mes_ano]['despesa'] += valor
        except ValueError:
            pass

    if not totais_mensais:
        print("\n🚫 Não há dados válidos para calcular as estatísticas.")
        _ = input("Pressione qualquer botão para voltar ao menu de Análises.")
        return

    total_meses = len(totais_mensais)
    total_receita_geral = sum(d['receita'] for d in totais_mensais.values())
    total_despesa_geral = sum(d['despesa'] for d in totais_mensais.values())

    media_receita = total_receita_geral / total_meses
    media_despesa = total_despesa_geral / total_meses

    relatorio_estatisticas_str += f"\nPeríodo de Análise (Meses Únicos): {total_meses}\n"
    relatorio_estatisticas_str += "-------------------------------------------------\n"
    relatorio_estatisticas_str += f"Total Acumulado de Receitas: R${total_receita_geral:.2f}\n"
    
    # ALTERAÇÃO APLICADA: Total Acumulado de Despesas
    relatorio_estatisticas_str += f"Total Acumulado de Despesas: -R${total_despesa_geral:.2f}\n" 
    relatorio_estatisticas_str += "-------------------------------------------------\n"
    
    relatorio_estatisticas_str += f"MÉDIA DE RECEITA MENSAL: R${media_receita:.2f}\n"
    
    # ALTERAÇÃO APLICADA: Média de Despesa Mensal
    relatorio_estatisticas_str += f"MÉDIA DE DESPESA MENSAL: -R${media_despesa:.2f}\n"
    
    saldo_medio = media_receita - media_despesa
    saldo_medio_formatado = f"R${saldo_medio:.2f}"
    
    relatorio_estatisticas_str += f"SALDO MÉDIO MENSAL:      {saldo_medio_formatado}\n"
    relatorio_estatisticas_str += "-------------------------------------------------\n"
    
    cor_inicio = "\033[92m" if saldo_medio >= 0 else "\033[91m"
    cor_fim = "\033[0m"

    print(relatorio_estatisticas_str.replace(f"SALDO MÉDIO MENSAL:      {saldo_medio_formatado}", 
                                            f"SALDO MÉDIO MENSAL:      {cor_inicio}{saldo_medio_formatado}{cor_fim}").strip())

    salvar = input("\nDeseja salvar as Estatísticas em um arquivo TXT? (S/N): ").upper()
    if salvar == 'S':
        data_atual = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"estatisticas_mensais_{data_atual}.txt"
        salvar_relatorio_txt(relatorio_estatisticas_str, nome_arquivo)

    _ = input("\nPressione qualquer botão para voltar ao menu de Análises.")

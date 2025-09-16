import sys

entrada = "ativo"
codigoUsuario = 0
cadastrosDeUsuario = [{"código": codigoUsuario, "usuário": "admin", "senha": "admin"}]
codigoProduto = 1
cadastrosDeProduto = [
    {
        "código": codigoProduto,
        "nome": "Mouse",
        "categoria": "Periférico",
        "quantidade": 5,
        "preço": 49.99,
    }
]
VALORES_PERMITIDOS = {
    "Periférico": {"min": 20.00, "max": 500.00},
    "Hardware": {"min": 100.00, "max": 5000.00},
    "Computador": {"min": 1500.00, "max": 10000.00},
}


def login():
    usuario = input("Digite o seu nome de usuário:\n")
    senha = input("Digite a sua senha:\n")

    for cadastro in cadastrosDeUsuario:
        if cadastro["usuário"] == usuario and cadastro["senha"] == senha:
            print(f"Seja bem vindo {usuario}")
            return usuario
        else:
            print("Usuário/Senha Incorreto(s)")
            return None


def calcularPercentualPorCategoria():
    total_quantidade = sum(produto["quantidade"] for produto in cadastrosDeProduto)
    if total_quantidade == 0:
        return {}

    percentuais = {}
    for produto in cadastrosDeProduto:
        categoria = produto["categoria"]
        percentuais[categoria] = percentuais.get(categoria, 0) + produto["quantidade"]

    for categoria in percentuais:
        percentuais[categoria] = (percentuais[categoria] / total_quantidade) * 100

    return percentuais


def menu(usuario):
    try:
        percentuais = calcularPercentualPorCategoria()
        resumo_percentuais = (
            " | ".join([f"{cat}: {perc:.1f}%" for cat, perc in percentuais.items()])
            if percentuais
            else "Nenhum produto em estoque"
        )

        entrada = int(
            input(
                f"""------------------------------------------
Usuário Logado: {usuario}
Distribuição do estoque por categoria: {resumo_percentuais}
Selecione a operação que deseja realizar:
    [1]: Cadastro de Produto
    [2]: Exibir Produtos
    [3]: Edição de Produto
    [4]: Deleção de Produto
    [5]: Cadastrar Usuário
    [6]: Terminar o Programa
------------------------------------------\n"""
            )
        )
        if entrada < 1 or entrada > 6:
            print("Comando inválido. Por favor, digite uma opção válida.")
            menu(usuario)
        else:
            match entrada:
                case 1:
                    print("Você selecionou a opção Cadastro de Produto")
                    cadastrarProduto(usuario)
                case 2:
                    print("Você selecionou a opção Exibir Produtos")
                    exibirProdutos(usuario)
                case 3:
                    print("Você selecionou a opção Edição de Produto")
                    editarProduto(usuario)
                case 4:
                    print("Você selecionou a opção Deleção de Produto")
                    deletarProduto(usuario)
                case 5:
                    print("Você selecionou a opção Cadastrar Usuário")
                    cadastrarUsuario(usuario)
                case 6:
                    print("Você selecionou a opção Terminar o Programa")
                    print("Muito obrigado por usar o nosso sistema.")
                    sys.exit()
    except ValueError:
        print("Comando inválido. Por favor, digite uma opção válida.")
        menu(usuario)


def cadastrarUsuario(usuario):
    global codigoUsuario
    novoUsuario = input("Digite o nome do novo usuário:\n")
    novaSenha = input("Digite a senha para o novo usuário:\n")
    codigoUsuario += 1

    novoCadastro = {"Código": codigoUsuario, "usuário": novoUsuario, "senha": novaSenha}

    cadastrosDeUsuario.append(novoCadastro)

    print(f"O usuário {novoUsuario} foi cadastrado com sucesso")

    print(cadastrosDeUsuario)

    menu(usuario)


def cadastrarProduto(usuario):
    global codigoProduto
    novoNome = input("Digite o nome do novo produto:\n")
    novaCategoria = input("Digite a categoria do novo produto:\n").capitalize()

    if novaCategoria not in VALORES_PERMITIDOS:
        print("Categoria inválida! As categorias permitidas são:")
        for categoria in VALORES_PERMITIDOS.keys():
            print(f"- {categoria}")
        menu(usuario)
        return

    novaQuantidade = int(input("Digite a quantidade do novo produto:\n"))
    novoPreco = float(input("Digite o preço do novo produto:\n"))

    limites = VALORES_PERMITIDOS[novaCategoria]
    if novoPreco < limites["min"] or novoPreco > limites["max"]:
        print(
            f"Preço inválido! Para a categoria {novaCategoria}, o preço deve estar entre R${limites['min']} e R${limites['max']}."
        )
        menu(usuario)
        return

    codigoProduto += 1
    novoProduto = {
        "código": codigoProduto,
        "nome": novoNome,
        "categoria": novaCategoria,
        "quantidade": novaQuantidade,
        "preço": novoPreco,
    }

    cadastrosDeProduto.append(novoProduto)

    print(f"O produto {novoProduto["nome"]} foi cadastrado com sucesso.")

    menu(usuario)


def exibirResumoEstoque():
    total_quantidade = sum(produto["quantidade"] for produto in cadastrosDeProduto)
    total_valor = sum(
        produto["quantidade"] * produto["preço"] for produto in cadastrosDeProduto
    )
    print("=" * 30)
    print("RESUMO DO ESTOQUE")
    print("=" * 30)
    print(f"Quantidade total de itens em estoque: {total_quantidade}")
    print(f"Valor total do estoque: R${total_valor:.2f}")
    print("=" * 30)


def exibirProdutos(usuario):
    print("-" * 30)
    print("PRODUTOS CADASTRADOS")
    print("-" * 30)

    if not cadastrosDeProduto:
        print("Nenhum produto cadastrado")
    else:
        for produto in cadastrosDeProduto:
            print(f"Código: {produto['código']}")
            print(f"Nome: {produto['nome']}")
            print(f"Categoria: {produto['categoria']}")
            print(f"Quantidade: {produto['quantidade']}")
            print(f"Preço: R${produto['preço']:.2f}")
            print("-" * 30)
        exibirResumoEstoque()

    menu(usuario)


def editarProduto(usuario):
    codigo = int(input("Digite o código do produto que deseja alterar:\n"))
    produto_encontrado = None

    for produto in cadastrosDeProduto:
        if produto["código"] == codigo:
            produto_encontrado = produto
            break

    if not produto_encontrado:
        print("Produto não encontrado!")
        menu(usuario)
        return

    print(
        f"Produto encontrado: {produto_encontrado['nome']} - {produto_encontrado['categoria']}"
    )
    print("Deixe em branco caso não queira alterar o campo.")

    novoNome = input(f"Novo nome ({produto_encontrado['nome']}):\n")
    novaCategoria = input(
        f"Nova categoria ({produto_encontrado['categoria']}):\n"
    ).capitalize()
    novaQuantidade = input(f"Nova quantidade ({produto_encontrado['quantidade']}):\n")
    novoPreco = input(f"Novo preço ({produto_encontrado['preço']}):\n")

    if novoNome.strip():
        produto_encontrado["nome"] = novoNome

    if novaCategoria.strip():
        if novaCategoria not in VALORES_PERMITIDOS:
            print("Categoria inválida! As categorias permitidas são:")
            for categoria in VALORES_PERMITIDOS.keys():
                print(f"- {categoria}")
            menu(usuario)
            return
        produto_encontrado["categoria"] = novaCategoria

    if novaQuantidade.strip():
        produto_encontrado["quantidade"] = int(novaQuantidade)

    if novoPreco.strip():
        categoria_atual = produto_encontrado["categoria"]
        limites = VALORES_PERMITIDOS[categoria_atual]
        novoPreco = float(novoPreco)

        if novoPreco < limites["min"] or novoPreco > limites["max"]:
            print(
                f"Preço inválido! Para a categoria {categoria_atual}, o preço deve estar entre R${limites['min']:.2f} e R${limites['max']:.2f}."
            )
            menu(usuario)
            return

        produto_encontrado["preço"] = novoPreco

    print("Produto atualizado com sucesso!")

    menu(usuario)


def deletarProduto(usuario):
    codigo = int(input("Digite o código do produto que seja deletar:\n"))
    produto_encontrado = None

    for produto in cadastrosDeProduto:
        if produto["código"] == codigo:
            produto_encontrado = produto
            break

    if not produto_encontrado:
        print("Produto não encontrado!")
        menu(usuario)
        return

    print(
        f"Produto encontrado: {produto_encontrado['nome']} - {produto_encontrado['categoria']} (Qtd: {produto_encontrado['quantidade']}, Preço: R${produto_encontrado['preço']:.2f})"
    )
    confirmacao = input(
        f"Tem certeza que deseja deletar o produto {produto_encontrado['nome']}? (s/n): "
    ).lower()

    if confirmacao == "s":
        cadastrosDeProduto.remove(produto_encontrado)
        print("Produto deletado com sucesso!")
    else:
        print("Operação cancelada.")

    menu(usuario)


while True:
    usuario_logado = login()
    if usuario_logado:
        menu(usuario_logado)

print("Muito Obrigado Por Usar o Nosso Sistema!")

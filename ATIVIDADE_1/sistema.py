import datetime
import sys

informacoes = {
    "cliente": "",
    "produto": "",
    "bairro": "",
    "quantidade": "",
    "data": datetime.datetime.now(),
    "hora": datetime.datetime.now(),
}

estoque = {"Mouse": 1}

bairrosDisponiveis = ["São Bernardo"]


def iniciar():
    print("Bem vindo à Papa Légua Express!")

    print("Somos uma empresa de entregas.")

    informacoes["cliente"] = input("Digite o nome do cliente: ")

    informacoes["produto"] = input("Qual produto vai ser entregue? ")

    informacoes["bairro"] = input("Qual o bairro de entrega? ")

    informacoes["quantidade"] = int(input("Quantas unidades serão entregues? "))

    print(
        f"""
    Informações do Pedido:
        Cliente: {informacoes["cliente"]}
        Produto: {informacoes["produto"]}
        Bairro: {informacoes["bairro"]}
        Quantidade: {(informacoes["quantidade"])}
        Data: {informacoes["data"].strftime("%x")}
        Hora: {informacoes["hora"].strftime("%X")}
        """
    )


def verificarBairro(bairro):
    if bairro not in bairrosDisponiveis:
        print("Bairro indisponível para a entrega.")
        sys.exit()
    else:
        print("Bairro disponível para a entrega.")


def verificarEstoque(produto, quantidade):
    if produto not in estoque:
        print(f"O produto {produto} não está cadastrado no estoque.")
        sys.exit()
    if estoque[produto] < quantidade:
        print("Estoque insuficiente.")
        sys.exit()
    print(f"O produto {produto} está disponível.")


iniciar()
verificarBairro(informacoes["bairro"])
verificarEstoque(informacoes["produto"], informacoes["quantidade"])

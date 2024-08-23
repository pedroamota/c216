def register_item(stock):
    nome = input("Digite o nome do item: ")
    autor = input("Digite o autor do item: ")
    try:
        quantidade = int(input("Digite a quantidade em estoque: "))
        stock.append({"nome": nome, "autor": autor, "quantidade": quantidade})
        print(f"Item '{nome}' cadastrado com sucesso!")
    except ValueError:
        print("Erro: Por favor, digite um número inteiro para a quantidade.")

def list_items(stock):
    if not stock:
        print("Nenhum item cadastrado.")
    else:
        for item in stock:
            print(f"Nome: {item['nome']}, Autor: {item['autor']}, Quantidade: {item['quantidade']}")

def view_item(stock):
    nome = input("Digite o nome do item a consultar: ")
    found = False
    for item in stock:
        if item["nome"].lower() == nome.lower():
            print(f"Nome: {item['nome']}, Autor: {item['autor']}, Quantidade: {item['quantidade']}")
            found = True
            break
    if not found:
        print("Item não encontrado no estoque.")

def sell_item(stock):
    nome = input("Digite o nome do item a vender: ")
    found = False
    for item in stock:
        if item["nome"].lower() == nome.lower():
            quantidade = int(input("Digite a quantidade a vender: "))
            if quantidade <= item["quantidade"]:
                item["quantidade"] -= quantidade
                print(f"Venda registrada! Quantidade restante de '{nome}': {item['quantidade']}")
            else:
                print("Erro: Quantidade em estoque insuficiente.")
            found = True
            break
    if not found:
        print("Item não encontrado no estoque.")

def main():
    stock = []
    options = {
        '1': register_item,
        '2': list_items,
        '3': view_item,
        '4': sell_item,
        '5': lambda stock: "exit"
    }

    while True:
        print("\nMenu de Opções:")
        print("1. Cadastrar item")
        print("2. Listar itens")
        print("3. Consultar item")
        print("4. Vender item")
        print("5. Sair")
        
        selected = input("Escolha uma opção: ")
        print()
        
        if selected in options:
            result = options[selected](stock)
            if result == "exit":
                print("Saindo...\n")
                break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()

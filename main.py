from database import criar_banco, destruir_banco
from services import (
    cadastrar_cliente,
    cadastrar_produto,
    realizar_venda,
    reajuste_salario,
    sortear_cliente,
    estatisticas_vendas,
    exibir_views,
    zerar_cashback
)


def menu():
    while True:
        print("\n========== E-COMMERCE AQUARISMO - MARIADB ==========")
        print("1 - Criar banco de dados")
        print("2 - Destruir banco de dados")
        print("3 - Cadastrar cliente")
        print("4 - Cadastrar produto")
        print("5 - Realizar venda")
        print("6 - Reajuste de salário por cargo")
        print("7 - Sorteio de cliente")
        print("8 - Estatísticas de vendas")
        print("9 - Exibir views")
        print("10 - Zerar cashback de cliente especial")
        print("0 - Sair")

        opcao = input("Escolha: ").strip()

        try:
            if opcao == '1':
                criar_banco()
                print("Banco criado com sucesso.")
            elif opcao == '2':
                destruir_banco()
                print("Banco destruído com sucesso.")
            elif opcao == '3':
                nome = input("Nome: ")
                idade = int(input("Idade: "))
                sexo = input("Sexo (M/F): ")
                data_nascimento = input("Data de nascimento (AAAA-MM-DD): ")
                cadastrar_cliente(nome, idade, sexo, data_nascimento)
            elif opcao == '4':
                nome = input("Nome do produto: ")
                descricao = input("Descrição: ")
                estoque = int(input("Quantidade em estoque: "))
                valor = float(input("Valor: "))
                observacoes = input("Observações: ")
                id_vendedor = int(input("ID do vendedor: "))
                cadastrar_produto(nome, descricao, estoque, valor, observacoes, id_vendedor)
            elif opcao == '5':
                id_cliente = int(input("ID do cliente: "))
                itens = []

                while True:
                    id_produto = int(input("ID do produto: "))
                    quantidade = int(input("Quantidade: "))
                    itens.append({'id_produto': id_produto, 'quantidade': quantidade})

                    print("1 - Adicionar outro produto")
                    print("2 - Concluir compra")
                    print("3 - Cancelar compra")
                    escolha = input("Escolha: ").strip()

                    if escolha == '1':
                        continue
                    elif escolha == '2':
                        break
                    elif escolha == '3':
                        itens = []
                        print("Compra cancelada antes da conclusão.")
                        break
                    else:
                        itens = []
                        print("Opção inválida. Compra cancelada por segurança.")
                        break

                if itens:
                    id_transportadora = int(input("ID da transportadora: "))
                    endereco = input("Endereço de destino: ")
                    valor_transporte = float(input("Valor do transporte: "))
                    realizar_venda(id_cliente, itens, id_transportadora, endereco, valor_transporte)
            elif opcao == '6':
                percentual = float(input("Percentual de reajuste: "))
                id_cargo = int(input("ID do cargo: "))
                reajuste_salario(percentual, id_cargo)
            elif opcao == '7':
                sortear_cliente()
            elif opcao == '8':
                estatisticas_vendas()
            elif opcao == '9':
                exibir_views()
            elif opcao == '10':
                id_cliente = int(input("ID do cliente especial: "))
                zerar_cashback(id_cliente)
            elif opcao == '0':
                print("Encerrando...")
                break
            else:
                print("Opção inválida.")
        except KeyboardInterrupt:
            print("\nOperação cancelada.")
        except Exception as erro:
            print(f"Erro: {erro}")


if __name__ == '__main__':
    menu()
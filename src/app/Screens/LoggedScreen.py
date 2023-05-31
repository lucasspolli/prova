from time import sleep
from DefaultScreen import DefaultScreen
from Repositories.ProductsRepository import ProductsRepository
from Repositories.UsersRepository import UsersRepository
from Repositories.CartsRepository import CartsRepository

from app.main import homeScreen

productsRepository = ProductsRepository()
usersRepository = UsersRepository()
cartsRepository = CartsRepository()

class LoggedScreen(DefaultScreen):
    def __init__(self, user):
        self.user = user
      
    def showScreen(self):
        options = [
            { "key": 1, "text": "Ver produtos cadastrados", "handle": self.RegistredProducts },
            { "key": 2, "text": "Cadastrar produtos", "handle": self.RegisterProducts },
            { "key": 3, "text": "Comprar um produto", "handle": self.BuyProduct },
            { "key": 4, "text": "Pagar carrinho", "handle": self.PayTheCart },
            { "key": 5, "text": "Sair da conta", "handle": self.Exit }
        ]

        while self.user.isLogged == True:
            self.banner()
            self.showOptions(options)

            selectedOption = self.selectOption()
            
            self.executeOption(options, selectedOption)

            if selectedOption == 5:
                break
        
    # PRODUTOS CADASTRADOS ==============================================================================================
    def RegistredProducts(self):
        self.banner()
        
        sleep(0.5)
        
        print("\033[0;32mAqui está a lista dos produtos cadastrados:\033[m")
        sleep(0.5)
        print(f"\033[0;33m{'Nome':<24}{'Preço':<12}{'Quantidade':<15}{'ID'}\033[m")
        
        productsList = productsRepository.findAll()
        
        if productsList:
            # ARRUMAR ERRO DE TIPO DA VARIÁVEL
            for product in productsList:
                sleep(0.3)
                print(f"{product[0]:<22}R${float(product[1]):<15.2f}{product[2]:<12}{product[3]}")
            
            while True:
                sleep(0.5)
                typedAnswer = str(input("\033[0;33mDigite \033[0;36mvoltar\033[m \033[0;33mpara retornar ao menu: \033[m"))
                
                if typedAnswer != "voltar":
                    sleep(1)
                    print("\033[0;31mResposta inválida!\033[m")
                else:
                    sleep(1)
                    self.printReturningToMenu()
                    sleep(0.5)
                    break

        sleep(1)
        print("\033[0;31mNo momento ainda não temos produtos em estoque!\033[m")
        sleep(2)
    
    def RegisterProducts(self):
        self.banner()

        cont = 0

        while True:
            sleep(1)
            
            typedAdminPassword = str(input("\033[0;33mDigite a senha de admin: \033[m"))

            if typedAdminPassword != "123":
                cont = cont + 1
                sleep(1)

                if cont == 3:
                    print("\033[0;31m3 tentativas erradas!\033[m")
                    break

                print("\033[0;31mSenha de admin errada!\033[m")
                
            else:
                break

        sleep(1)
        print("\033[0;36mDigite 0 à qualquer momento para sair do registro dos produtos!\033[m")
        
        while True:
            typedProductName = str(input("\033[0;33mDigite o nome do seu produto: \033[m"))
            
            if typedProductName == "0":
                self.printReturningToMenu()
                return

            productExists = productsRepository.findByName(typedProductName)
            
            if not productExists:
                break
            
            sleep(1)
            print("\033[0;31mEste nome de produto já existe!\033[m")
            
        while True:
            sleep(1)
            try:
                typedProductPrice = str(input("\033[0;33mDigite o preço do seu produto: \033[m"))
                break
            except ValueError:
                sleep(1)
                print("\033[0;31mDigite somente os números do preço ou digite com '.' os centavos!\033[m")

        # VERIFICA SE O USUÁRIO QUER SAIR
        if typedProductPrice == 0:
            self.printReturningToMenu()
            return
        
        while True:
            sleep(1)
            try:
                typedProductQuantify = int(input("\033[0;33mDigite a quantidade do seu produto que tem em estoque: \033[m"))
                break
            except ValueError:
                sleep(1)
                print("\033[0;31mDigite somente valores inteiros!\033[m")

        # VERIFICA SE O USUÁRIO QUER SAIR
        if typedProductQuantify == 0:
            self.printReturningToMenu()
            return
        
        productsRepository.create(typedProductName, typedProductPrice, typedProductQuantify)

        sleep(1)
        print("\033[0;32m\nSeu produto foi adicionado ao sistema!\033[m")
        sleep(1)
   
    def BuyProduct(self):
        self.banner()
        
        sleep(1)
        print("\033[0;36mDigite 0 à qualquer momento para sair da compra de produtos!\033[m")
        sleep(0.5)
        print("\033[0;32mAqui está a lista dos produtos cadastrados:\033[m")
        sleep(0.5)
        
        print(f"\033[0;33m{'Nome':<24}{'Preço':<12}{'Quantidade':<15}{'ID'}\033[m")
        
        productsList = productsRepository.findAll()
        
        for product in productsList:
            sleep(0.3)
            print(f"{product.name:<22}R${float(product.price):<15.2f}{product.quantify:<12}{product.id}")
        
        while True:
            sleep(0.5)
            typedProductId = int(input("\033[0;33mDigite o ID do produto que deseja comprar: \033[m"))

            if typedProductId == 0:
                self.printReturningToMenu()
                return

            productExists = productsRepository.findById(typedProductId)

            if productExists:
                sleep(1)
                self.banner()
                sleep(0.5)
                print("\033[0;33mO produto escolhido foi:\033[m")
                sleep(0.5)
                print(f"\033[0;32m{productExists.name}\033[m que custa \033[0;32mR${float(productExists.price):.2f}\033[m com \033[0;32m{productExists.quantify}\033[m quantidades em estoque e seu ID é \033[0;32m{productExists.id}\033[m")
                break
            else:
                sleep(1)
                print("\033[0;31mEste ID de produto não existe!\033[m")

        while True:
            sleep(1)
            typedProductQuantify = str(input("\033[0;33mDigite a quantidade que deseja comprar: \033[m"))
            typedProductQuantify = int(typedProductQuantify)

            if typedProductQuantify <= productExists.quantify and typedProductQuantify > 0:

                userInformations = usersRepository.findById(self.user.id)

                usersRepository.update(userInformations.id, userInformations.username, userInformations.email, userInformations.password)
                cartsRepository.addProduct(userInformations.id, typedProductId, typedProductQuantify)

                print("\033[0;32mSeu produto foi adicionado ao carrinho!\033[m")

                cartsRepository.seeCart()

                sleep(1.5)
                break

            sleep(1)
            print("\033[0;31mQuantidade digitada inválida!\033[m")
    
    def paymentMenu(self):
        print("="*66)
        sleep(0.2)
        print("\033[0;33m1\033[m - Pagar no débito")
        sleep(0.2)
        print("\033[0;33m2\033[m - Pagar no crédito")
        sleep(0.2)
        print("\033[0;33m3\033[m - Sair do menu")
        sleep(0.2)

        while True:
            try:
                option = int(input("\033[0;33mComo você deseja pagar a sua conta? \033[m"))
                break
            except ValueError:
                sleep(1)
                print(f"\033[0;31mDigite um número!\033[m")
                 
        return option

    def updateData(self, product):
        for products in product:
            # productInDatabase = cursor.execute(f"SELECT * FROM produtos WHERE id = '{products[3]}'")
            productInDatabase = productInDatabase.fetchall()
            productQuantify = int(productInDatabase[0][2]) - int(products[2])
            
            # cursor.execute(f"UPDATE produtos SET quantidade = '{productQuantify}' WHERE id = '{products[3]}'")
            connection.commit()

        sleep(1.5)
    
    def PayTheCart(self):
        self.banner()

        sleep(1)
        print("\033[0;32mAqui está a lista dos produtos do seu carrinho:\033[m")
        sleep(0.5)
        print(f"\033[0;33m{'Nome':<24}{'Preço':<12}{'Quantidade':<15}{'ID'}\033[m")
        
        cart = cartsRepository.findById(self.user.id)

        if cart == []:
            sleep(1)
            print(f"\033[0;32mVocê não tem produtos no carrinho!\033[m")
            sleep(2)
            return
        
        productIds = map(lambda product: product['id'], cart['products'])

        products = productsRepository.findByIds(productIds)

        for product in products:
            sleep(0.3)
            print(f"{product.name:<22}R${float(product.price):<15.2f}{product.quantify:<12}{product.id}")
        

        # SELECIONAR OS PRODUTOS NO BANCO DE DADOS
        
        # MOSTRAR AS INFORMAÇÕES DE TODOS OS PRODUTOS REGISTRADOS
        # total = 0
        # for products in product:
        #     sleep(0.3)
        #     #
        #     print(f"{products[0]:<22}R${float(products[1]):<15.2f}{products[2]:<12}{products[3]}")
        #     if products[2] == 1:
        #         total = total + float(products[1])
        #     else:
        #         total = total + (float(products[1]) * int(products[2]))
        # # VALOR TOTAL DO CARRINHO
        # sleep(1)
        # print(f"\033[0;32mO valor total do seu carrinho é R${total:.2f}\033[m")
        # sleep(1)
        # # PAGAMENTO
        # while True:
        #     option = self.paymentMenu()
        #     # PAGOU COM DÉBITO
        #     if option == 1:
        #         self.updateData(product)
        #         print(f"\033[0;32mVocê pagou R${total:.2f} no débito!\033[m")
        #         sleep(2)
        #         return
        #     # PAGOU COM CRÉDTIO
        #     elif option == 2:
        #         break
        #     # RETORNANDO PARA O MENU
        #     elif option == 3:
        #         self.printReturningToMenu()
        #         return
        #     # OPÇÃO INVÁLIDA
        #     else:
        #         sleep(1)
        #         print("\033[0;31mOpção inválida!\033[m")
        #         sleep(1)
        # while True:
        #     sleep(1)
        #     installments = int(input(f"\033[0;33mEm quantas parcelas deseja pagar? \033[m"))
        #     if installments > 12:
        #         sleep(1)
        #         print("\033[0;31mQuantidade de parcelas maior que 12!\033[m")
        #     else:
        #         self.updateData(product)
        #         value = total / installments
        #         print(f"\033[0;32mVocê irá pagar R${value:.2f} em {installments}x!\033[m")
        #         sleep(2)
        #         break
            
    def Exit(self):
        homeScreen.showScreen()
        return
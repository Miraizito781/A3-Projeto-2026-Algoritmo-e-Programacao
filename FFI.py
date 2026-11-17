# Football Frontier Internacional 
# RPG de futebol em turnos desenvolvido em Python, utilizando conceitos simples
# e mecânicas previsíveis e temática vagamente baseada na animação televisiva Inazuma Eleven.
# Discentes Integrantes: Marcelo, Leônidas, Ewerton e Miguel.
# Professores Orientadores: Arthur e André.
# Para fins de comunicação clara, os comentários do código estarão sinalizados com "###" quando for para 
# explicar as funções, e "#" para explicações mais amplas sobre o código.

### - Essa função irá ler uma das opções disponíveis ate que o usuário informe um valor permitido.
def ler_opcao(mensagem, opcoes_validas):
    opcao = input(mensagem).strip()
    while opcao not in opcoes_validas:
        print("Opcao invalida. Tente novamente.")
        opcao = input(mensagem).strip()
    return opcao


### - Essa função irá mostrar os tipos de atletas que podem ser escolhidos: Eles são: Atacante, Meio Campista e Defensor (Zagueiro Líbero ou Lateral), respectivamente.
### - Cada um desses 3 tipos de jogadores possui características que vão interferir diretamente no fluxo dos confrontos que virão.
def mostrar_atletas():
    
    print("\nEscolha seu atleta:")
    print("1 - Atacante              | Energia: 15 | Ataque: 10 | Defesa: 2")
    print("2 - Meio-Campista         | Energia: 20 | Ataque: 7  | Defesa: 4")
    print("3 - Libero/Lateral        | Energia: 25 | Ataque: 6  | Defesa: 6")
    
### - Essa função vai pedir que o usuário escolha o tipo do seu jogador e dê um nome a ele.


def criar_jogador():
    nome = input("Digite o nome do jogador: ").strip()
    while nome == "":
        print("O espaço reservado ao nome não pode ficar vazio.")
        nome = input("Digite o nome do jogador: ").strip()
        
    mostrar_atletas()
    escolha = ler_opcao("Opcao: ", ["1", "2", "3"])

    if escolha == "1":
        personagem = "Atacante"
        energia_maxima = 25
        ataque = 10
        defesa = 2
    elif escolha == "2":
        personagem = "Meio-Campista"
        energia_maxima = 30
        ataque = 7
        defesa = 4
    else:
        personagem = "Libero/Lateral"
        energia_maxima = 36
        ataque = 6
        defesa = 6

### - Nessa linha, crio um dicionário "jogador" para armazenar o modelo dos jogadores.

    jogador = { 
        "nome": nome,
        "personagem": personagem,
        "energia": energia_maxima,
        "energia_maxima": energia_maxima,
        "ataque": ataque,
        "defesa": defesa,
        "gols": 0,
        "pontuacao": 0,
        "nivel": 1
    } 
    return jogador

### - Essa função vai criar três dicionários com dados de rivais para uma partida.
def criar_rivais():
            rivais = [
            {"nome": "Zagueiro adversario", "resistencia": 18, "dano": 4},
            {"nome": "Goleiro", "resistencia": 25, "dano": 5},
            {"nome": "Capitao do time rival", "resistencia": 32, "dano": 7}
]
            return rivais  


### - Mostra os dados atuais do jogador e da partida.
def mostrar_status(jogador, rivais, indice_rival, partida_ativa):
        print("\n--- STATUS DO ATLETA ---")
        print("Nome:", jogador["nome"])
        print("Personagem:", jogador["personagem"])
        print("Energia:", jogador["energia"], "/", jogador["energia_maxima"])
        print("Ataque:", jogador["ataque"])
        print("Defesa:", jogador["defesa"])
        print("Nivel:", jogador["nivel"])
        print("Gols:", jogador["gols"])
        print("Pontuacao:", jogador["pontuacao"])
        
        if partida_ativa and indice_rival < len(rivais):
            print("Rival atual:", rivais[indice_rival]["nome"])
            print("Resistencia do rival:", rivais[indice_rival]["resistencia"])
        elif jogador["gols"] == len(rivais):
            print("Resultado: Copa conquistada!")
        else:
            print("Resultado: nenhuma partida ativa.")
            
### Esta função mostra os dados do adversario atual.            
def mostrar_rival(rival):
    
    print("\nRival:", rival["nome"])
    print("Resistencia:", rival["resistencia"])
    print("Dano da jogada rival:", rival["dano"])
    
### Esta função vai atualizar a contagem de gols, a pontuação, o nível e a energia do jogador após vencer um rival.    
def registrar_gol(jogador):
    jogador["gols"] = jogador["gols"] + 1
    jogador["pontuacao"] = jogador["pontuacao"] + 10
    jogador["nivel"] = jogador["nivel"] + 1
    jogador["energia"] = jogador["energia"] + 3
    
    if jogador["energia"] > jogador["energia_maxima"]:
        jogador["energia"] = jogador["energia_maxima"]
    print("\nGOOOOL! Voce venceu o rival e marcou um gol!")
    print("Gols:", jogador["gols"], "| Pontuação:", jogador["pontuacao"])
    print("Voce avançou para o nível", jogador["nivel"])
    print("Recuperou 3 pontos de energia.")
    
### Esta função vai fazer a jogada do rival. A defesa reduz o dano recebido.    
def contra_atacar(jogador, rival, defender):
    dano_recebido = rival["dano"]

    if defender:
        dano_recebido = dano_recebido - jogador["defesa"]
        if dano_recebido < 0:
            dano_recebido = 0
        print("Voce marcou o rival e reduziu o dano da jogada.")
    else:
        print("O rival respondeu com uma jogada!")

    jogador["energia"] = jogador["energia"] - dano_recebido

    if jogador["energia"] < 0:
        jogador["energia"] = 0

    print("Voce perdeu", dano_recebido, "pontos de energia.")
    print("Energia atual:", jogador["energia"])
    
### Esta função vai executar os turnos até a partida ser vencida, perdida ou abandonada.    
def jogar_desafio(jogador, rivais, indice_rival):
    partida_ativa = True

    while partida_ativa:
        rival = rivais[indice_rival]
        mostrar_rival(rival)
        print("\nEscolha sua acao:")
        print("1 - Atacar / Finalizar")
        print("2 - Defender / Marcar")
        print("3 - Fugir / Abandonar a partida")
        acao = ler_opcao("Opcao: ", ["1", "2", "3"])

        if acao == "1":
            dano_ataque = jogador["ataque"] + jogador["nivel"] - 1
            rival["resistencia"] = rival["resistencia"] - dano_ataque

            if rival["resistencia"] < 0:
                rival["resistencia"] = 0
                print("Sua jogada reduziu a resistência do rival em", dano_ataque, ".")
            print("Resistência restante:", rival["resistencia"])

            if rival["resistencia"] == 0:
                registrar_gol(jogador)
                indice_rival = indice_rival + 1

                if indice_rival == len(rivais):
                    print("\nPARABÉNS! Voce venceu a FFI!")
                    partida_ativa = False
                else:
                    print("Proximo desafio:", rivais[indice_rival]["nome"])
            else:
                contra_atacar(jogador, rival, False)

        elif acao == "2":
            contra_atacar(jogador, rival, True)
        else:
            print("Voce abandonou a partida e voltou ao menu principal.")
            partida_ativa = False

        if jogador["energia"] == 0:
            print("\nSua energia chegou a zero. Você perdeu a partida.")
            partida_ativa = False

    return indice_rival, partida_ativa

### Esta função vai mostrar o resultado acumulado da partida atual.
def consultar_pontuacao(jogador):
    if jogador is None:
        print("\nNenhuma partida foi iniciada ainda.")
    else:
        print("\n--- PONTUACAO ---")
        print("Atleta:", jogador["nome"])
        print("Gols:", jogador["gols"])
        print("Pontos:", jogador["pontuacao"])
        print("Nivel:", jogador["nivel"])

### Esta função vai mostrar as opções do menu principal.        
def mostrar_menu():
    print("\n====== FOOTBALL FRONTIER INTERNACIONAL ======")
    print("1 - Visualizar status")
    print("2 - Iniciar partida")
    print("3 - Confrontar Rival")
    print("4 - Consultar pontuacao")
    print("5 - Sair")


### Esta função vai controlar o menu principal do jogo.
def main():
    jogador = None
    rivais = []
    indice_rival = 0
    partida_ativa = False
    executando = True

    while executando:
        mostrar_menu()
        opcao = ler_opcao("Escolha uma opcao: ", ["1", "2", "3", "4", "5"])

        if opcao == "1":
            if jogador is None:
                print("\nInicie uma partida para visualizar o status.")
            else:
                mostrar_status(jogador, rivais, indice_rival, partida_ativa)
                
        elif opcao == "2":
            jogador = criar_jogador()
            rivais = criar_rivais()
            indice_rival = 0
            partida_ativa = True
            print("\nPartida iniciada! Seu primeiro desafio sera o Zagueiro adversario.")
            
        elif opcao == "3":
            if jogador is None:
                print("\nInicie uma partida antes de jogar um desafio.")
                ### Este elif abaixo é pra caso o usuário tenha criado um jogador, iniciado uma partida, perdido, e o status da partida vai pra false. 
                ### Se ele tentar confrontar um rival sem estar em uma partida ativa, o código não vai deixar e vai dizer pra ele iniciar outra partida.
            elif not partida_ativa:
                print("\nNão há uma partida ativa. Voce pode iniciar outra no menu.")
            else:
                indice_rival, partida_ativa = jogar_desafio(jogador, rivais, indice_rival)
                
        elif opcao == "4":
            consultar_pontuacao(jogador)

        else:
            print("\nObrigado por jogar o FOOTBALL FRONTIER INTERNACIONAL!")
            executando = False


main()


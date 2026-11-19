# Football Frontier Internacional
# RPG de futebol em turnos desenvolvido em Python, utilizando conceitos simples
# e mecânicas previsíveis e temática vagamente baseada na animação televisiva Inazuma Eleven.
# Discentes Integrantes: Marcelo, Leônidas, Ewerton e Miguel.
# Professores Orientadores: Arthur e André.
# Para fins de comunicação clara, os comentários do código estarão sinalizados com "###" quando for para
# explicar as funções, e "#" para explicações mais amplas sobre o código.

# COMO O JOGO FUNCIONA (resumo):
# - O jogador escolhe um atleta (Atacante, Meio-Campista ou Líbero/Lateral) e enfrenta 3 rivais em sequência.
# - Em cada rodada, o jogador e o rival escolhem uma jogada ao mesmo tempo: Chutar, Driblar ou Defender.
# - As jogadas funcionam como "pedra, papel e tesoura":
#       Chutar vence Driblar  |  Driblar vence Defender  |  Defender vence Chutar
# - Quem vence a disputa causa dano; se as jogadas forem iguais, elas se anulam (empate) e ninguém leva dano.
# - Cada rival repete um padrão fixo de jogadas (sem sorteio). Observando o padrão, o jogador consegue vencer.
# - Vitória: derrotar os 3 rivais. Derrota: a energia do atleta chegar a zero. Fugir encerra a partida.


### - Essa função irá ler uma das opções disponíveis até que o usuário informe um valor permitido.
def ler_opcao(mensagem, opcoes_validas):
    opcao = input(mensagem).strip()
    while opcao not in opcoes_validas:
        print("Opção inválida. Tente novamente.")
        opcao = input(mensagem).strip()
    return opcao


### - Essa função irá mostrar os tipos de atletas que podem ser escolhidos: Atacante, Meio-Campista e Líbero/Lateral.
### - Cada um desses 3 tipos de jogadores possui características que vão interferir diretamente no fluxo dos confrontos que virão.
### - Os valores mostrados aqui precisam ser os mesmos usados na função criar_jogador().
def mostrar_atletas():
    print("\nEscolha seu atleta:")
    print("1 - Atacante              | Energia: 25 | Ataque: 10 | Defesa: 2")
    print("2 - Meio-Campista         | Energia: 30 | Ataque: 7  | Defesa: 4")
    print("3 - Líbero/Lateral        | Energia: 36 | Ataque: 6  | Defesa: 6")


### - Essa função vai pedir que o usuário dê um nome ao jogador e escolha o tipo do seu atleta.
### - No final, ela devolve um dicionário com todos os dados do jogador.
def criar_jogador():
    nome = input("Digite o nome do jogador: ").strip()
    while nome == "":
        print("O espaço reservado ao nome não pode ficar vazio.")
        nome = input("Digite o nome do jogador: ").strip()

    mostrar_atletas()
    escolha = ler_opcao("Opção: ", ["1", "2", "3"])

    # Cada escolha define os atributos iniciais do atleta.
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
        personagem = "Líbero/Lateral"
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


### - Essa função vai criar a lista com os três dicionários dos rivais de uma partida.
### - "padrao" é a lista de jogadas que o rival repete em ordem (1 = Chutar, 2 = Driblar, 3 = Defender).
### - "turno" conta quantas jogadas o rival já fez, para sabermos qual é a próxima jogada do padrão.
### - "estilo" é uma dica mostrada ao jogador para ele aprender como o rival costuma jogar.
def criar_rivais():
    rivais = [
        {"nome": "Zagueiro adversário", "resistencia": 18, "dano": 4, "padrao": [3, 3, 1], "turno": 0,
         "estilo": "Gosta de marcar e só de vez em quando arrisca um chute."},
        {"nome": "Goleiro", "resistencia": 25, "dano": 5, "padrao": [1, 3, 2, 3], "turno": 0,
         "estilo": "Alterna chutes e defesas, com um drible de surpresa."},
        {"nome": "Capitão do time rival", "resistencia": 32, "dano": 7, "padrao": [1, 2, 3, 1, 2], "turno": 0,
         "estilo": "Muda de jogada o tempo todo, mas repete uma sequência."}
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
    print("Nível:", jogador["nivel"])
    print("Gols:", jogador["gols"])
    print("Pontuação:", jogador["pontuacao"])

    if partida_ativa and indice_rival < len(rivais):
        print("Rival atual:", rivais[indice_rival]["nome"])
        print("Resistência do rival:", rivais[indice_rival]["resistencia"])
    elif jogador["gols"] == len(rivais):
        print("Resultado: Copa conquistada!")
    else:
        print("Resultado: nenhuma partida ativa.")


### - Esta função mostra os dados do adversário atual, incluindo a dica sobre o estilo de jogo dele.
def mostrar_rival(rival):
    print("\nRival:", rival["nome"])
    print("Resistência:", rival["resistencia"])
    print("Dano da jogada rival:", rival["dano"])
    print("Estilo de jogo:", rival["estilo"])


### - Esta função mostra as jogadas disponíveis e a regra de quem vence quem.
def mostrar_jogadas():
    print("\nEscolha sua jogada:")
    print("1 - Chutar (ataque)")
    print("2 - Driblar (ataque)")
    print("3 - Defender / Marcar")
    print("4 - Fugir / Abandonar a partida")
    print("Regra: Chutar vence Driblar | Driblar vence Defender | Defender vence Chutar")


### - Esta função devolve o nome de uma jogada a partir do número dela (1, 2 ou 3).
def nome_da_jogada(numero):
    if numero == 1:
        return "Chutar"
    elif numero == 2:
        return "Driblar"
    else:
        return "Defender"


### - Esta função decide quem venceu a disputa entre a jogada do jogador e a do rival.
### - Ela devolve "jogador", "rival" ou "empate".
def descobrir_vencedor(jogada_jogador, jogada_rival):
    if jogada_jogador == jogada_rival:
        return "empate"
    elif (jogada_jogador == 1 and jogada_rival == 2) or (jogada_jogador == 2 and jogada_rival == 3) or (jogada_jogador == 3 and jogada_rival == 1):
        return "jogador"
    else:
        return "rival"


### - Esta função escolhe a jogada do rival seguindo o padrão fixo dele (sem sorteio).
### - O resto da divisão (%) faz o padrão voltar ao começo quando chega ao fim da lista.
def escolher_jogada_rival(rival):
    posicao = rival["turno"] % len(rival["padrao"])
    jogada = rival["padrao"][posicao]
    rival["turno"] = rival["turno"] + 1
    return jogada


### - Esta função calcula o dano que o jogador causa ao vencer uma disputa.
### - Se venceu defendendo (jogada 3), usa a defesa; se venceu atacando (1 ou 2), usa o ataque.
### - O nível do jogador soma 1 ponto de dano para cada nível acima do primeiro.
def calcular_dano_do_jogador(jogador, jogada):
    if jogada == 3:
        dano = jogador["defesa"] + jogador["nivel"] - 1
    else:
        dano = jogador["ataque"] + jogador["nivel"] - 1
    return dano


### - Esta função calcula o dano que o jogador recebe ao perder uma disputa.
### - A defesa do atleta reduz o dano do rival pela metade do valor da defesa (divisão inteira //).
### - O dano mínimo é 1, para que nenhum atleta fique imune.
def calcular_dano_recebido(jogador, rival):
    dano = rival["dano"] - jogador["defesa"] // 2
    if dano < 1:
        dano = 1
    return dano


### - Esta função mostra um texto explicando como a jogada vencedora superou a outra.
def mostrar_resultado_da_disputa(jogada_vencedora):
    if jogada_vencedora == 1:
        print("O chute saiu antes do drible!")
    elif jogada_vencedora == 2:
        print("O drible passou pela marcação!")
    else:
        print("A marcação bloqueou o chute!")


### - Esta função vai atualizar a contagem de gols, a pontuação, o nível e a energia do jogador após vencer um rival.
def registrar_gol(jogador):
    jogador["gols"] = jogador["gols"] + 1
    jogador["pontuacao"] = jogador["pontuacao"] + 10
    jogador["nivel"] = jogador["nivel"] + 1
    jogador["energia"] = jogador["energia"] + 3

    # A energia nunca pode passar do máximo do atleta.
    if jogador["energia"] > jogador["energia_maxima"]:
        jogador["energia"] = jogador["energia_maxima"]
    print("\nGOOOOL! Você venceu o rival e marcou um gol!")
    print("Gols:", jogador["gols"], "| Pontuação:", jogador["pontuacao"])
    print("Você avançou para o nível", jogador["nivel"])
    print("Recuperou 3 pontos de energia.")


### - Esta função executa uma rodada: o jogador e o rival jogam, a disputa é decidida e o dano é aplicado.
### - Quem vence a disputa causa dano; se empatar, as jogadas se anulam e ninguém leva dano.
def executar_rodada(jogador, rival, jogada_jogador):
    jogada_rival = escolher_jogada_rival(rival)
    print("\nVocê jogou:", nome_da_jogada(jogada_jogador), "| O rival jogou:", nome_da_jogada(jogada_rival))

    vencedor = descobrir_vencedor(jogada_jogador, jogada_rival)

    if vencedor == "jogador":
        mostrar_resultado_da_disputa(jogada_jogador)
        dano = calcular_dano_do_jogador(jogador, jogada_jogador)
        rival["resistencia"] = rival["resistencia"] - dano

        # A resistência do rival nunca fica abaixo de zero.
        if rival["resistencia"] < 0:
            rival["resistencia"] = 0
        print("Você venceu a disputa e reduziu a resistência do rival em", dano, ".")
        print("Resistência restante:", rival["resistencia"])

    elif vencedor == "rival":
        mostrar_resultado_da_disputa(jogada_rival)
        dano = calcular_dano_recebido(jogador, rival)
        jogador["energia"] = jogador["energia"] - dano

        # A energia do jogador nunca fica abaixo de zero.
        if jogador["energia"] < 0:
            jogador["energia"] = 0
        print("O rival venceu a disputa! Você perdeu", dano, "pontos de energia.")
        print("Energia atual:", jogador["energia"])

    else:
        print("As jogadas se anularam. Ninguém levou dano.")


### - Esta função vai executar os turnos até a partida ser vencida, perdida ou abandonada.
### - Ela devolve o índice do rival atual e se a partida continua ativa, para o menu principal atualizar esses dados.
def jogar_desafio(jogador, rivais, indice_rival):
    partida_ativa = True

    while partida_ativa:
        rival = rivais[indice_rival]
        mostrar_rival(rival)
        mostrar_jogadas()
        acao = ler_opcao("Opção: ", ["1", "2", "3", "4"])

        if acao == "4":
            print("Você abandonou a partida e voltou ao menu principal.")
            partida_ativa = False
        else:
            # int() transforma o texto digitado ("1", "2" ou "3") em número.
            executar_rodada(jogador, rival, int(acao))

            # Se a resistência do rival chegou a zero, o jogador marcou gol e avança de rival.
            if rival["resistencia"] == 0:
                registrar_gol(jogador)
                indice_rival = indice_rival + 1

                if indice_rival == len(rivais):
                    print("\nPARABÉNS! Você venceu a FFI!")
                    partida_ativa = False
                else:
                    print("Próximo desafio:", rivais[indice_rival]["nome"])

            # Se a energia do jogador chegou a zero, ele é derrotado.
            if jogador["energia"] == 0:
                print("\nSua energia chegou a zero. Você perdeu a partida.")
                partida_ativa = False

    return indice_rival, partida_ativa


### - Esta função vai mostrar o resultado acumulado da partida atual.
def consultar_pontuacao(jogador):
    if jogador is None:
        print("\nNenhuma partida foi iniciada ainda.")
    else:
        print("\n--- PONTUAÇÃO ---")
        print("Atleta:", jogador["nome"])
        print("Gols:", jogador["gols"])
        print("Pontos:", jogador["pontuacao"])
        print("Nível:", jogador["nivel"])


### - Esta função vai mostrar as opções do menu principal.
def mostrar_menu():
    print("\n====== FOOTBALL FRONTIER INTERNACIONAL ======")
    print("1 - Visualizar status")
    print("2 - Iniciar partida")
    print("3 - Batalhar (Confrontar Rival)")
    print("4 - Consultar pontuação")
    print("5 - Sair")


### - Esta função vai controlar o menu principal do jogo.
def main():
    # Variáveis que guardam o estado do jogo enquanto o programa está aberto.
    jogador = None
    rivais = []
    indice_rival = 0
    partida_ativa = False
    executando = True

    # O laço while mantém o menu aberto até o usuário escolher "5 - Sair".
    while executando:
        mostrar_menu()
        opcao = ler_opcao("Escolha uma opção: ", ["1", "2", "3", "4", "5"])

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
            print("\nPartida iniciada! Seu primeiro desafio será o Zagueiro adversário.")

        elif opcao == "3":
            if jogador is None:
                print("\nInicie uma partida antes de jogar um desafio.")
            ### Este elif abaixo é pra caso o usuário tenha criado um jogador, iniciado uma partida, perdido, e o status da partida vai pra false.
            ### Se ele tentar confrontar um rival sem estar em uma partida ativa, o código não vai deixar e vai dizer pra ele iniciar outra partida.
            elif not partida_ativa:
                print("\nNão há uma partida ativa. Você pode iniciar outra no menu.")
            else:
                indice_rival, partida_ativa = jogar_desafio(jogador, rivais, indice_rival)

        elif opcao == "4":
            consultar_pontuacao(jogador)

        else:
            print("\nObrigado por jogar o FOOTBALL FRONTIER INTERNACIONAL!")
            executando = False


main()

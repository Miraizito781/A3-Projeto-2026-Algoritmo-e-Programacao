# Football Frontier Internacional
# RPG de futebol em turnos desenvolvido em Python, utilizando conceitos simples
# e mecânicas previsíveis e temática vagamente baseada na animação televisiva Inazuma Eleven.
# Discentes Integrantes: Marcelo, Leônidas e Ewerton.
# Professores Orientadores: Arthur e André.
# Para fins de comunicação clara, os comentários do código estarão sinalizados com "###" quando for para
# explicar as funções, e "#" para explicações mais amplas sobre o código.

# COMO O JOGO FUNCIONA (resumo):
# - O jogador cria um personagem (nome e tipo de atleta: Atacante, Meio-Campista ou Líbero/Lateral).
# - Com o personagem criado, ele inicia uma partida em uma rota (copa) e enfrenta 3 rivais em sequência.
# - Em cada rodada, o jogador e o rival escolhem uma jogada ao mesmo tempo: Chutar, Driblar ou Defender.
# - As jogadas funcionam como "pedra, papel e tesoura":
#       Chutar vence Driblar  |  Driblar vence Defender  |  Defender vence Chutar
# - Quem vence a disputa causa dano; se as jogadas forem iguais, elas se anulam (empate) e ninguém leva dano.
# - Cada rival tem mais de um padrão de jogadas: a cada partida o jogo sorteia um deles. Além disso, em alguns
#   turnos o rival "improvisa" e joga uma jogada sorteada. Observando o padrão, o jogador consegue vencer.
# - Vitória: derrotar os 3 rivais da rota e conquistar a copa. Derrota: a energia do atleta chegar a zero.
#   Fugir encerra a partida.
# - Existem 3 rotas (copas). A rota 1 está sempre liberada; cada rota seguinte só é liberada ao conquistar a anterior.
# - O progresso (copas conquistadas, rotas liberadas e conquistas) é mantido enquanto o programa estiver aberto,
#   mesmo que o jogador crie outro personagem.
# - O menu mostra apenas as opções que estão disponíveis no momento.

# O módulo "random" traz funções de sorteio. Neste código usamos duas delas:
# - random.choice(lista): sorteia um elemento da lista.
# - random.randint(a, b): sorteia um número inteiro entre a e b (incluindo a e b).
import random


### - Essa função irá ler uma das opções disponíveis até que o usuário informe um valor permitido.
def ler_opcao(mensagem, opcoes_validas):
    opcao = input(mensagem).strip()
    while opcao not in opcoes_validas:
        print("Opção inválida. Tente novamente.")
        opcao = input(mensagem).strip()
    return opcao


### - Essa função irá mostrar os tipos de atletas que podem ser escolhidos: Atacante, Meio-Campista e Líbero/Lateral.
### - Cada um desses 3 tipos de jogadores possui características que vão interferir diretamente no fluxo dos confrontos que virão.
### - Os valores foram ajustados em simulações para os três atletas terem chances parecidas de vencer.
def mostrar_atletas():
    print("\nEscolha seu atleta:")
    print("1 - Atacante              | Energia: 34 | Ataque: 10 | Defesa: 2")
    print("2 - Meio-Campista         | Energia: 30 | Ataque: 8  | Defesa: 4")
    print("3 - Líbero/Lateral        | Energia: 28 | Ataque: 7  | Defesa: 5")


### - Essa função vai pedir que o usuário dê um nome ao personagem e escolha o tipo do seu atleta.
### - No final, ela devolve um dicionário "personagem" com o nome e o tipo escolhido ("1", "2" ou "3").
### - Ela só cria o personagem: os dados da partida (energia, gols, nível...) são criados em criar_jogador().
def criar_personagem():
    nome = input("Digite o nome do jogador: ").strip()
    while nome == "":
        print("O espaço reservado ao nome não pode ficar vazio.")
        nome = input("Digite o nome do jogador: ").strip()

    mostrar_atletas()
    escolha = ler_opcao("Opção: ", ["1", "2", "3"])

    personagem = {"nome": nome, "escolha": escolha}
    return personagem


### - Essa função recebe o nome e o tipo de atleta do personagem e devolve um dicionário "jogador" zerado,
### - com energia cheia, 0 gols e nível 1. Ela é chamada a cada partida nova.
def criar_jogador(nome, escolha):
    # Cada escolha define os atributos iniciais do atleta.
    if escolha == "1":
        personagem = "Atacante"
        energia_maxima = 34
        ataque = 10
        defesa = 2
    elif escolha == "2":
        personagem = "Meio-Campista"
        energia_maxima = 30
        ataque = 8
        defesa = 4
    else:
        personagem = "Líbero/Lateral"
        energia_maxima = 28
        ataque = 7
        defesa = 5

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


### - Essa função devolve o nome da rota (copa) a partir do número dela.
def nome_da_rota(rota):
    if rota == 1:
        return "Copa Regional"
    elif rota == 2:
        return "Copa Continental"
    else:
        return "Copa Mundial"


### - Essa função devolve a lista com os números das rotas que o jogador já pode disputar.
### - A rota 1 está sempre liberada; cada rota seguinte só é liberada depois de conquistar a anterior.
def rotas_liberadas(progresso):
    liberadas = [1]
    for numero in [2, 3]:
        if (numero - 1) in progresso["rotas_vencidas"]:
            liberadas.append(numero)
    return liberadas


### - Essa função cria o dicionário de um rival. Existe só para não repetir o mesmo código para cada rival.
### - "padroes" guarda mais de uma sequência de jogadas (1 = Chutar, 2 = Driblar, 3 = Defender) para o rival.
### - "padrao" é a sequência sorteada para a partida atual, então o mesmo rival pode jogar diferente em cada partida.
### - "acoes" são os nomes que o rival dá para as jogadas 1, 2 e 3, de acordo com a posição dele em campo.
### - "improviso" é a chance (em %) de o rival ignorar o padrão e jogar algo sorteado em um turno.
### - "turno" conta quantas jogadas o rival já fez, para sabermos qual é a próxima jogada do padrão.
### - "estilo" é uma dica mostrada ao jogador para ele aprender como o rival costuma jogar.
def criar_rival(nome, resistencia, dano, padroes, acoes, improviso, estilo):
    rival = {
        "nome": nome, "resistencia": resistencia, "dano": dano,
        "padroes": padroes, "padrao": random.choice(padroes),
        "acoes": acoes, "improviso": improviso, "turno": 0, "estilo": estilo
    }
    return rival


### - Essa função vai criar a lista com os três rivais da rota escolhida.
### - Cada rota tem rivais diferentes e mais fortes que a anterior.
def criar_rivais(rota):
    if rota == 1:
        rivais = [
            criar_rival("Zagueiro adversário", 18, 4,
                        [[3, 3, 1, 3, 2, 3], [3, 1, 3, 3, 2, 3], [3, 3, 3, 1, 3, 2]],
                        {1: "Chutão", 2: "Avanço com a bola", 3: "Marcação cerrada"}, 10,
                        "Gosta de marcar e só de vez em quando arrisca um chute. Raramente improvisa."),
            criar_rival("Goleiro", 25, 5,
                        [[1, 3, 2, 3, 1, 1, 3, 2], [3, 1, 3, 2, 1, 3, 1, 2], [1, 1, 3, 2, 3, 3, 2, 1]],
                        {1: "Chutão de meta", 2: "Saída do gol", 3: "Espalmar"}, 15,
                        "Alterna chutes e defesas, com uma saída de surpresa. Às vezes improvisa."),
            criar_rival("Capitão do time rival", 32, 7,
                        [[1, 2, 3, 1, 2, 2, 3, 1, 3, 2], [2, 2, 1, 3, 1, 2, 3, 3, 1, 2], [3, 1, 2, 2, 3, 1, 1, 2, 3, 2]],
                        {1: "Chute colocado", 2: "Drible desconcertante", 3: "Desarme"}, 20,
                        "Muda de jogada o tempo todo, mas repete uma sequência. Improvisa com frequência.")
        ]
    elif rota == 2:
        rivais = [
            criar_rival("Volante veloz", 22, 5,
                        [[2, 2, 3, 1, 2, 3, 3, 1], [2, 3, 2, 2, 1, 3, 2, 1], [3, 2, 2, 1, 2, 2, 3, 1]],
                        {1: "Chute de fora da área", 2: "Arrancada", 3: "Roubo de bola"}, 15,
                        "Parte pra cima com muita arrancada e só marca quando perde a bola. Às vezes improvisa."),
            criar_rival("Meia craque", 28, 6,
                        [[1, 2, 1, 3, 2, 3, 1, 1, 2, 3], [2, 1, 3, 1, 2, 2, 3, 1, 1, 3], [1, 3, 2, 1, 3, 3, 2, 1, 2, 1]],
                        {1: "Passe-chute", 2: "Elástico", 3: "Bloqueio"}, 20,
                        "Alterna chute e drible sem parar, mas fecha a defesa de vez em quando. Improvisa com frequência."),
            criar_rival("Artilheiro rival", 34, 8,
                        [[1, 1, 2, 1, 3, 1, 2, 1, 1, 3], [1, 2, 1, 1, 3, 1, 1, 2, 3, 1], [2, 1, 1, 3, 1, 1, 2, 1, 1, 3]],
                        {1: "Chute potente", 2: "Finta", 3: "Pressão"}, 20,
                        "Prefere o chute e só dribla quando está pressionado. Improvisa com frequência.")
        ]
    else:
        rivais = [
            criar_rival("Lateral de ferro", 26, 6,
                        [[3, 3, 2, 3, 3, 1, 3, 2, 3, 3], [3, 2, 3, 3, 1, 3, 3, 2, 3, 1], [2, 3, 3, 3, 1, 3, 2, 3, 3, 3]],
                        {1: "Cruzamento forte", 2: "Descida pela ala", 3: "Muralha"}, 20,
                        "Muralha pela lateral: marca quase sempre e surpreende com avanços. Improvisa com frequência."),
            criar_rival("Goleiro lendário", 32, 8,
                        [[3, 1, 3, 2, 3, 3, 1, 2, 3, 1, 3], [1, 3, 3, 2, 1, 3, 2, 3, 3, 1, 2], [3, 3, 1, 3, 2, 1, 3, 3, 2, 1, 3]],
                        {1: "Lançamento", 2: "Saída relâmpago", 3: "Defesa impossível"}, 25,
                        "Quase impossível de bater: defende, lança e sai do gol sem aviso. Improvisa bastante."),
            criar_rival("Capitão da seleção", 40, 9,
                        [[1, 2, 3, 3, 1, 2, 1, 3, 2, 2, 3, 1], [2, 1, 3, 1, 2, 3, 2, 1, 3, 3, 1, 2], [3, 2, 1, 2, 3, 1, 1, 2, 3, 1, 2, 2]],
                        {1: "Chute Supremo", 2: "Drible Fantasma", 3: "Defesa Total"}, 25,
                        "O melhor do mundo: usa todos os recursos e muda o jogo sem avisar. Improvisa bastante.")
        ]
    return rivais


# CONQUISTAS DO JOGO: "id": ["nome", "descrição"]. Para criar uma conquista nova, basta incluir uma linha aqui
# e chamar tentar_conquista(...) no ponto do código em que o requisito é cumprido.
CONQUISTAS = {
    "primeiro_gol": ["Primeiro Gol", "Marque o seu primeiro gol."],
    "sequencia_3": ["Sequência Perfeita", "Vença 3 disputas seguidas atacando (Chutar ou Driblar)."],
    "gol_limpo": ["Gol Limpo", "Marque um gol sem levar dano do rival."],
    "campeao": ["Campeão", "Conquiste a sua primeira copa."],
    "invicto": ["Invicto", "Conquiste uma copa sem perder nenhum ponto de energia."],
    "na_raca": ["Na Raça", "Conquiste uma copa com 5 ou menos de energia no gol final."],
    "lenda": ["Lenda", "Conquiste a Copa Mundial."]
}


### - Essa função cria o dicionário "controle", usado para acompanhar a partida e liberar as conquistas.
### - "sequencia_ataques" conta as disputas seguidas vencidas atacando (jogada 1 ou 2).
### - "levou_dano_rival" guarda se o jogador levou dano do rival atual; "levou_dano_partida", se levou dano em toda a partida.
def criar_controle():
    controle = {
        "sequencia_ataques": 0,
        "levou_dano_rival": False,
        "levou_dano_partida": False
    }
    return controle


### - Essa função tenta liberar uma conquista. Se o jogador ainda não tinha, guarda a conquista
### - e adiciona o aviso na lista "avisos" (os avisos são mostrados no fim da rodada).
def tentar_conquista(progresso, id_conquista, avisos):
    if id_conquista not in progresso["conquistas"]:
        progresso["conquistas"].append(id_conquista)
        nome = CONQUISTAS[id_conquista][0]
        descricao = CONQUISTAS[id_conquista][1]
        avisos.append("CONQUISTA DESBLOQUEADA: " + nome + " - " + descricao)


### - Essa função mostra os avisos das conquistas liberadas na rodada (se houver algum).
def mostrar_avisos(avisos):
    if len(avisos) > 0:
        print()
        for aviso in avisos:
            print(aviso)


### - Essa função mostra todas as conquistas, marcando com [x] as que o jogador já liberou.
def mostrar_conquistas(progresso):
    print("\n--- CONQUISTAS (" + str(len(progresso["conquistas"])) + "/" + str(len(CONQUISTAS)) + ") ---")
    for id_conquista in CONQUISTAS:
        nome = CONQUISTAS[id_conquista][0]
        descricao = CONQUISTAS[id_conquista][1]
        if id_conquista in progresso["conquistas"]:
            print("[x]", nome, "-", descricao)
        else:
            print("[ ]", nome, "-", descricao)


### - Mostra os dados atuais do jogador e da partida.
def mostrar_status(jogador, rivais, indice_rival, partida_ativa, rota, progresso):
    print("\n--- STATUS DO ATLETA ---")
    print("Nome:", jogador["nome"])
    print("Personagem:", jogador["personagem"])
    print("Energia:", jogador["energia"], "/", jogador["energia_maxima"])
    print("Ataque:", jogador["ataque"])
    print("Defesa:", jogador["defesa"])
    print("Nível:", jogador["nivel"])
    print("Gols:", jogador["gols"])
    print("Pontuação:", jogador["pontuacao"])
    print("Copas conquistadas:", progresso["copas"])

    if partida_ativa and indice_rival < len(rivais):
        print("Rota:", nome_da_rota(rota))
        print("Rival atual:", rivais[indice_rival]["nome"])
        print("Resistência do rival:", rivais[indice_rival]["resistencia"])
    elif len(rivais) > 0 and jogador["gols"] == len(rivais):
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


### - Esta função escolhe a jogada do rival seguindo o padrão sorteado para ele nesta partida.
### - O resto da divisão (%) faz o padrão voltar ao começo quando chega ao fim da lista.
### - Em alguns turnos o rival "improvisa": ignora o padrão e joga uma jogada sorteada (1, 2 ou 3).
def escolher_jogada_rival(rival):
    posicao = rival["turno"] % len(rival["padrao"])
    jogada = rival["padrao"][posicao]
    rival["turno"] = rival["turno"] + 1

    # randint(1, 100) sorteia de 1 a 100. Se o número cair dentro da chance de improviso, a jogada é trocada.
    if random.randint(1, 100) <= rival["improviso"]:
        jogada = random.randint(1, 3)
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
    # Quantidade de energia que o jogador recupera a cada gol. Para mudar a dificuldade, basta alterar este valor.
    energia_recuperada = 6
    energia_antes = jogador["energia"]

    jogador["gols"] = jogador["gols"] + 1
    jogador["pontuacao"] = jogador["pontuacao"] + 10
    jogador["nivel"] = jogador["nivel"] + 1
    jogador["energia"] = jogador["energia"] + energia_recuperada

    # A energia nunca pode passar do máximo do atleta.
    if jogador["energia"] > jogador["energia_maxima"]:
        jogador["energia"] = jogador["energia_maxima"]

    # Calcula quanto de energia foi realmente recuperado (pode ser menos que o valor acima se o atleta já estava perto do máximo).
    recuperou = jogador["energia"] - energia_antes
    print("\nGOOOOL! Você venceu o rival e marcou um gol!")
    print("Gols:", jogador["gols"], "| Pontuação:", jogador["pontuacao"])
    print("Você avançou para o nível", jogador["nivel"])
    if recuperou > 0:
        print("Recuperou", recuperou, "pontos de energia.")
    else:
        print("Sua energia já estava no máximo.")


### - Esta função registra uma copa conquistada: soma no contador, libera a próxima rota e verifica as conquistas da copa.
### - "energia_final" é a energia do jogador no momento do gol final (antes da recuperação do gol).
def registrar_copa(progresso, rota, controle, energia_final, avisos):
    liberadas_antes = len(rotas_liberadas(progresso))

    progresso["copas"] = progresso["copas"] + 1
    if rota not in progresso["rotas_vencidas"]:
        progresso["rotas_vencidas"].append(rota)

    print("\nPARABÉNS! Você conquistou a", nome_da_rota(rota) + "!")
    print("Copas conquistadas:", progresso["copas"])

    # Se a lista de rotas liberadas cresceu, a última dela é a rota nova.
    liberadas = rotas_liberadas(progresso)
    if len(liberadas) > liberadas_antes:
        nova = liberadas[len(liberadas) - 1]
        print("Nova rota liberada:", nome_da_rota(nova) + "! Você poderá escolhê-la ao iniciar a próxima partida.")

    tentar_conquista(progresso, "campeao", avisos)
    if not controle["levou_dano_partida"]:
        tentar_conquista(progresso, "invicto", avisos)
    if energia_final <= 5:
        tentar_conquista(progresso, "na_raca", avisos)
    if rota == 3:
        tentar_conquista(progresso, "lenda", avisos)


### - Esta função mostra uma linha divisória para separar o menu de jogadas do texto que explica o que aconteceu na rodada.
def mostrar_divisoria():
    print("============================================")


### - Esta função faz o jogo esperar o jogador apertar Enter, para dar tempo de ler o texto da rodada antes de o menu aparecer de novo.
def pausar():
    input("\nPressione Enter para continuar...")


### - Esta função executa uma rodada: o jogador e o rival jogam, a disputa é decidida e o dano é aplicado.
### - Quem vence a disputa causa dano; se empatar, as jogadas se anulam e ninguém leva dano.
### - Ela também atualiza o "controle" e libera a conquista "Sequência Perfeita" (os avisos vão para a lista "avisos").
def executar_rodada(jogador, rival, jogada_jogador, controle, progresso, avisos):
    jogada_rival = escolher_jogada_rival(rival)

    # A divisória separa o menu de jogadas do texto que descreve a rodada.
    mostrar_divisoria()
    print("Você jogou:", nome_da_jogada(jogada_jogador), "| O rival jogou:", rival["acoes"][jogada_rival], "(" + nome_da_jogada(jogada_rival) + ")")

    vencedor = descobrir_vencedor(jogada_jogador, jogada_rival)

    # Controle da conquista "Sequência Perfeita": conta as disputas seguidas vencidas atacando (jogada 1 ou 2).
    # Qualquer outro resultado (derrota, empate ou vitória defendendo) zera a sequência.
    if vencedor == "jogador" and jogada_jogador != 3:
        controle["sequencia_ataques"] = controle["sequencia_ataques"] + 1
    else:
        controle["sequencia_ataques"] = 0
    if controle["sequencia_ataques"] >= 3:
        tentar_conquista(progresso, "sequencia_3", avisos)

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

        # Guarda que o jogador levou dano (usado nas conquistas "Gol Limpo" e "Invicto").
        controle["levou_dano_rival"] = True
        controle["levou_dano_partida"] = True
        print("O rival venceu a disputa! Você perdeu", dano, "pontos de energia.")
        print("Energia atual:", jogador["energia"])

    else:
        print("As jogadas se anularam. Ninguém levou dano.")

    # Segunda divisória: fecha o texto da rodada antes de aparecer o menu seguinte.
    mostrar_divisoria()


### - Esta função vai executar os turnos até a partida ser vencida, perdida ou abandonada.
### - Ela devolve o índice do rival atual e se a partida continua ativa, para o menu principal atualizar esses dados.
def jogar_desafio(jogador, rivais, indice_rival, rota, progresso, controle):
    partida_ativa = True

    while partida_ativa:
        rival = rivais[indice_rival]
        # Lista que guarda os avisos de conquistas desta rodada.
        avisos = []
        mostrar_rival(rival)
        mostrar_jogadas()
        acao = ler_opcao("Opção: ", ["1", "2", "3", "4"])

        if acao == "4":
            print("Você abandonou a partida e voltou ao menu principal.")
            partida_ativa = False
        else:
            # int() transforma o texto digitado ("1", "2" ou "3") em número.
            executar_rodada(jogador, rival, int(acao), controle, progresso, avisos)

            # Se a resistência do rival chegou a zero, o jogador marcou gol e avança de rival.
            if rival["resistencia"] == 0:
                energia_do_gol = jogador["energia"]

                tentar_conquista(progresso, "primeiro_gol", avisos)
                if not controle["levou_dano_rival"]:
                    tentar_conquista(progresso, "gol_limpo", avisos)

                registrar_gol(jogador)
                indice_rival = indice_rival + 1
                controle["levou_dano_rival"] = False

                if indice_rival == len(rivais):
                    registrar_copa(progresso, rota, controle, energia_do_gol, avisos)
                    partida_ativa = False
                else:
                    print("Próximo desafio:", rivais[indice_rival]["nome"])

            # Se a energia do jogador chegou a zero, ele é derrotado.
            if jogador["energia"] == 0:
                print("\nSua energia chegou a zero. Você perdeu a partida.")
                partida_ativa = False

            # Mostra as conquistas liberadas nesta rodada.
            mostrar_avisos(avisos)

            # Pausa para o jogador ler o texto da rodada antes do próximo menu.
            pausar()

    return indice_rival, partida_ativa


### - Esta função vai mostrar o resultado acumulado da partida atual.
def consultar_pontuacao(jogador, progresso):
    if jogador is None:
        print("\nNenhuma partida foi iniciada ainda.")
    else:
        print("\n--- PONTUAÇÃO ---")
        print("Atleta:", jogador["nome"])
        print("Gols:", jogador["gols"])
        print("Pontos:", jogador["pontuacao"])
        print("Nível:", jogador["nivel"])
        print("Copas conquistadas:", progresso["copas"])


### - Esta função pergunta qual rota o jogador quer disputar. Só aparecem as rotas já liberadas.
### - Se só a rota 1 estiver liberada, ela é escolhida automaticamente, sem perguntar nada.
def escolher_rota(progresso):
    liberadas = rotas_liberadas(progresso)
    if len(liberadas) == 1:
        return 1

    print("\nEscolha a rota:")
    opcoes_validas = []
    for numero in liberadas:
        print(numero, "-", nome_da_rota(numero))
        opcoes_validas.append(str(numero))
    escolha = ler_opcao("Rota: ", opcoes_validas)
    return int(escolha)


### - Esta função monta a lista de opções que estão disponíveis no momento. As indisponíveis não entram na lista.
### - Sem personagem: criar personagem. Com personagem e sem partida ativa: iniciar partida.
### - Com partida ativa: batalhar (e não é possível iniciar outra nem criar outro personagem até terminar esta).
def montar_opcoes(jogador, partida_ativa):
    if jogador is None:
        return ["Criar personagem", "Sair"]

    opcoes = []
    if partida_ativa:
        opcoes.append("Batalhar (Confrontar Rival)")
    else:
        opcoes.append("Iniciar partida")
    opcoes.append("Visualizar status")
    opcoes.append("Consultar pontuação")
    opcoes.append("Consultar conquistas")
    if not partida_ativa:
        opcoes.append("Criar novo personagem")
    opcoes.append("Sair")
    return opcoes


### - Esta função vai mostrar as opções do menu principal, numeradas a partir de 1, de acordo com a lista recebida.
def mostrar_menu(opcoes):
    print("\n====== FOOTBALL FRONTIER INTERNACIONAL ======")
    for i in range(len(opcoes)):
        print(i + 1, "-", opcoes[i])


### - Esta função vai controlar o menu principal do jogo.
def main():
    # Variáveis que guardam o estado do jogo enquanto o programa está aberto.
    personagem = None
    jogador = None
    rivais = []
    indice_rival = 0
    rota = 1
    partida_ativa = False
    controle = criar_controle()
    executando = True

    # Progresso do jogador: não é zerado quando ele cria um novo personagem.
    progresso = {"copas": 0, "rotas_vencidas": [], "conquistas": []}

    # O laço while mantém o menu aberto até o usuário escolher "Sair".
    while executando:
        opcoes = montar_opcoes(jogador, partida_ativa)
        mostrar_menu(opcoes)

        # Monta a lista de números válidos ("1", "2", ...) de acordo com a quantidade de opções mostradas.
        numeros_validos = []
        for i in range(len(opcoes)):
            numeros_validos.append(str(i + 1))
        escolha = ler_opcao("Escolha uma opção: ", numeros_validos)

        # A opção escolhida é o texto que está na posição (número digitado - 1) da lista.
        acao = opcoes[int(escolha) - 1]

        if acao == "Criar personagem" or acao == "Criar novo personagem":
            personagem = criar_personagem()
            jogador = criar_jogador(personagem["nome"], personagem["escolha"])
            rivais = []
            indice_rival = 0
            print("\nPersonagem criado! Quando quiser começar, escolha \"Iniciar partida\".")

        elif acao == "Iniciar partida":
            rota = escolher_rota(progresso)
            jogador = criar_jogador(personagem["nome"], personagem["escolha"])
            rivais = criar_rivais(rota)
            indice_rival = 0
            controle = criar_controle()
            partida_ativa = True
            print("\nPartida iniciada na", nome_da_rota(rota) + "! Seu primeiro desafio será:", rivais[0]["nome"] + ".")

        elif acao == "Batalhar (Confrontar Rival)":
            indice_rival, partida_ativa = jogar_desafio(jogador, rivais, indice_rival, rota, progresso, controle)

        elif acao == "Visualizar status":
            mostrar_status(jogador, rivais, indice_rival, partida_ativa, rota, progresso)

        elif acao == "Consultar pontuação":
            consultar_pontuacao(jogador, progresso)

        elif acao == "Consultar conquistas":
            mostrar_conquistas(progresso)

        else:
            print("\nObrigado por jogar o FOOTBALL FRONTIER INTERNACIONAL!")
            executando = False


main()

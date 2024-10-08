import pygame, sys, random
from pygame.math import Vector2

pygame.init()
fonte_titulo = pygame.font.Font(None, 60)
ponto_titulo = pygame.font.Font(None, 40)
# cores utilizadas
GREY = (29, 29, 27)
GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

# tamanho da tela
quadradinho = 30
numero_de_quadradinhos = 25

BORDA = 75

class Comidinha:
    def __init__(self, cobrinha_body):
        # inicia a cobrinha em uma posicao aleatoria na tela
        self.position = self.gerar_posicao_aleatoria(cobrinha_body)

    def gerar_quadradinho_aleatorio(self):
        # posiciona a comida aleatoriamente na tela
        x = random.randint(0, numero_de_quadradinhos - 1)
        y = random.randint(0, numero_de_quadradinhos - 1)
        return Vector2(x, y)

    def gerar_posicao_aleatoria(self, cobrinha_body):
        # verifica a comida nao fica em cima da cobrinha e a posiciona aleatoriamente
        position = self.gerar_quadradinho_aleatorio()
        while position in cobrinha_body:
            position = self.gerar_quadradinho_aleatorio()
        return position

    def desenho(self):
        # desenha a comida na tela
        comida_rect = pygame.Rect(BORDA + self.position.x * quadradinho, BORDA + self.position.y * quadradinho,
                                  quadradinho, quadradinho)
        screen.blit(comida_surface, comida_rect)


class Cobrinha:
    def __init__(self):
        # posiciona a cobrinha na tela
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = (1, 0)
        self.adicionar_segmento = False

    def desenho(self):
        # desenha a cobrinha na tela
        for segmento in self.body:
            segmento_rect = (BORDA + segmento.x * quadradinho, BORDA + segmento.y * quadradinho, quadradinho, quadradinho)
            pygame.draw.rect(screen, DARK_GREEN, segmento_rect, 0, 7)

    def atualizar(self):
        self.body.insert(0, self.body[0] + self.direction)
        # quando a cobrinha comer uma comida o seu corpo ira crescer pela cabeca
        if self.adicionar_segmento:
            self.adicionar_segmento = False
        else:
            # mexe a cobrinha pra uma direcao
            self.body = self.body[:-1]

    def reset(self):
        # essa funcao reseta a cobrinha para a posicao inicial
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)


class Jogo:
    def __init__(self):
        self.cobrinha = Cobrinha()
        self.comidinha = Comidinha(self.cobrinha.body)
        self.estado = "c"
        self.ponto = 0

    def desenho(self):
        # exibe a cobrinha e a comidinha na tela
        self.comidinha.desenho()
        self.cobrinha.desenho()

    def atualizar(self):
        # atualiza o jogo
        if self.estado == "c":
            self.cobrinha.atualizar()
            self.checar_coisao_com_comidinha()
            self.checar_colisao_com_beiradas()
            self.checar_colisao_com_corpo()

    def checar_coisao_com_comidinha(self):
        # verifica se a cobrinha colidiu com a comidinha
        if self.cobrinha.body[0] == self.comidinha.position:
            self.comidinha.position = self.comidinha.gerar_posicao_aleatoria(self.cobrinha.body)
            self.cobrinha.adicionar_segmento = True
            self.ponto += 1

    def checar_colisao_com_beiradas(self):
        # verifica se a cobrinha colidiu com aa beiradas
        if self.cobrinha.body[0].x == numero_de_quadradinhos or self.cobrinha.body[0].x == -1:
            self.game_over()
        if self.cobrinha.body[0].y == numero_de_quadradinhos or self.cobrinha.body[0].y == -1:
            self.game_over()

    def game_over(self):
        self.cobrinha.reset()
        self.comidinha.position = self.comidinha.gerar_posicao_aleatoria(self.cobrinha.body)
        self.estado = "p"
        self.ponto = 0

    def checar_colisao_com_corpo(self):
        # Verifica se a cabeça colidiu com o corpo da cobrinha
        cabeca_batida = self.cobrinha.body[1:]  # Segmentos do corpo excluindo a cabeça
        if self.cobrinha.body[0] in cabeca_batida:
            self.game_over()


# setando tamanho da tela
screen = pygame.display.set_mode((2 * BORDA + quadradinho * numero_de_quadradinhos,
                                  2 * BORDA + quadradinho * numero_de_quadradinhos))
pygame.display.set_caption("Jogo da cobrinha")

clock = pygame.time.Clock()

# definindo objeto
jogo = Jogo()
# exibindo imagem da comidinha
comida_surface = pygame.image.load("imagens/Cartoon-Apple.png")

# setando um tempo de atualizacao para a cobrinha
COBRINHA_ATUALIZANDO = pygame.USEREVENT
pygame.time.set_timer(COBRINHA_ATUALIZANDO, 200)

while True:
    for event in pygame.event.get():
        if event.type == COBRINHA_ATUALIZANDO:
            jogo.atualizar()
        # verifica se o usuario saiu do jogo e o termina
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # verifica as teclas apertadas
        if event.type == pygame.KEYDOWN:
            if jogo.estado == "p":
                jogo.estado = "c"
            if event.key == pygame.K_UP and jogo.cobrinha.direction != Vector2(0, 1):
                jogo.cobrinha.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and jogo.cobrinha.direction != Vector2(0, -1):
                jogo.cobrinha.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and jogo.cobrinha.direction != Vector2(1, 0):
                jogo.cobrinha.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and jogo.cobrinha.direction != Vector2(-1, 0):
                jogo.cobrinha.direction = Vector2(1, 0)

    # Desenhando na tela
    screen.fill(GREEN)
    pygame.draw.rect(screen, DARK_GREEN, (BORDA - 5, BORDA - 5, quadradinho * numero_de_quadradinhos + 10,
                                          quadradinho * numero_de_quadradinhos + 10), 5)
    jogo.desenho()
    # Escreve o titulo do jogo
    titulo_surface = fonte_titulo.render("Jogo da Cobrinha", True, DARK_GREEN)
    ponto_surface = ponto_titulo.render(str(jogo.ponto), True, DARK_GREEN)
    screen.blit(titulo_surface, (BORDA - 5, 20))
    screen.blit(ponto_surface, (BORDA -5, BORDA + quadradinho * numero_de_quadradinhos + 10))
    # framerate do jogo
    pygame.display.update()
    clock.tick(60)

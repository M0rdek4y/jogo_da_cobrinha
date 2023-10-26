import tkinter as tk
import random
import time

# Configurações iniciais
largura = 21
altura = 21
tamanho_celula = 20
intervalo_atualizacao = 100  # Milissegundos
pontuacao = 0

# Inicialização da janela
janela = tk.Tk()
janela.title("Jogo da Cobrinha")
janela.geometry(f"{426}x{450}")

# Inicialização da cobra
cobra = [(largura // 2, altura // 2)]
direcao = (0, -1)  # Começa indo para cima

# Função para gerar comida em uma posição aleatória
def gerar_comida():
    while True:
        x, y = random.randint(0, largura - 1), random.randint(0, altura - 1)
        if (x, y) not in cobra:
            return x, y

comida = gerar_comida()

# Função para atualizar o jogo
def atualizar_jogo():
    global cobra, direcao, comida, pontuacao

    # Mover a cobra na direção atual
    x, y = cobra[0]
    novo_x = (x + direcao[0]) % largura
    novo_y = (y + direcao[1]) % altura

    # Verificar se a cobra colidiu com a parede ou com ela mesma
    if (novo_x, novo_y) in cobra or novo_x < 0 or novo_x >= largura or novo_y < 0 or novo_y >= altura:
        game_over()
        return

    cobra.insert(0, (novo_x, novo_y))

    # Verificar se a cobra comeu a comida
    if (novo_x, novo_y) == comida:
        pontuacao += 1
        comida = gerar_comida()
    else:
        cobra.pop()

    # Redesenhar a tela
    canvas.delete("all")
    for x, y in cobra:
        canvas.create_rectangle(x * tamanho_celula, y * tamanho_celula,
                                (x + 1) * tamanho_celula, (y + 1) * tamanho_celula, fill="purple")
    cx, cy = comida
    canvas.create_oval(cx * tamanho_celula, cy * tamanho_celula,
                       (cx + 1) * tamanho_celula, (cy + 1) * tamanho_celula, fill="darkgreen")

    # Atualizar a pontuação
    lbl_pontuacao.config(text=f"Pontuação: {pontuacao}")

    # Agendar a próxima atualização
    janela.after(intervalo_atualizacao, atualizar_jogo)

# Função para lidar com o fim do jogo
def game_over():
    canvas.create_text(largura * tamanho_celula // 2, altura * tamanho_celula // 2,
                       text=f"Fim de Jogo! Pontuação: {pontuacao}", font=("Arial", 16), fill="white")

# Função para mudar a direção da cobra
def mudar_direcao(event):
    global direcao
    if event.keysym == "Up" and direcao != (0, 1):
        direcao = (0, -1)
    elif event.keysym == "Down" and direcao != (0, -1):
        direcao = (0, 1)
    elif event.keysym == "Left" and direcao != (1, 0):
        direcao = (-1, 0)
    elif event.keysym == "Right" and direcao != (-1, 0):
        direcao = (1, 0)

# Configurar a tela do jogo
canvas = tk.Canvas(janela, width=largura * tamanho_celula, height=altura * tamanho_celula, bg="black")
canvas.pack()

# Configurar a pontuação
lbl_pontuacao = tk.Label(janela, text=f"Pontuação: {pontuacao}", font=("Arial", 12), fg="white", bg="black")
lbl_pontuacao.pack()

# Lidar com eventos de teclado
janela.bind("<KeyPress>", mudar_direcao)

# Iniciar o jogo
atualizar_jogo()

# Iniciar a janela principal
janela.mainloop()
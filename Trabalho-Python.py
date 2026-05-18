from tkinter import *
from tkinter import messagebox
import sqlite3

# BANCO DE DADOS

def conectar():
    return sqlite3.connect("atividades.db")


def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atividades (
            tipo TEXT NOT NULL,
            pergunta TEXT NOT NULL,
            resposta TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pontuacao (
            pontos INTEGER NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM pontuacao")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO pontuacao (pontos) VALUES (0)")

    cursor.execute("DELETE FROM atividades")

    cursor.executemany("""
        INSERT INTO atividades (tipo, pergunta, resposta)
        VALUES (?, ?, ?)
    """, [
        ('email', 'Digite um exemplo de email válido:', 'teste@gmail.com'),
        ('atalho', 'Qual tecla completa Ctrl + C ?', 'V'),
        ('google', 'Digite o endereço correto do Google:', 'google.com')
    ])

    conn.commit()
    conn.close()


def buscar_atividade(tipo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT pergunta, resposta FROM atividades WHERE tipo=?",
        (tipo,)
    )

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado
    else:
        return ("Pergunta não encontrada", "")


def carregar_pontuacao():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT pontos FROM pontuacao LIMIT 1")
    resultado = cursor.fetchone()

    conn.close()

    return resultado[0] if resultado else 0


def salvar_pontuacao(pontos):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE pontuacao SET pontos=? WHERE rowid = 1",
        (pontos,)
    )

    conn.commit()
    conn.close()


# SISTEMA 

pontuacao = 0


def atualizar_placar():
    texto_pontos.config(text=f"Pontuação: {pontuacao}")


def conferir_resposta(valor_digitado, resposta_certa):
    global pontuacao

    if valor_digitado.strip().lower() == resposta_certa.lower():
        pontuacao += 1
        messagebox.showinfo("Resultado", "Resposta correta!")
    else:
        pontuacao -= 1
        messagebox.showwarning(
            "Resultado",
            f"Resposta errada.\nCorreto seria: {resposta_certa}"
        )

    salvar_pontuacao(pontuacao)
    atualizar_placar()


def criar_tela(tipo, titulo, largura):
    pergunta, resposta = buscar_atividade(tipo)

    tela = Toplevel()
    tela.title(titulo)
    tela.geometry("380x220")

    Label(
        tela,
        text=pergunta
    ).pack(pady=10)

    caixa = Entry(tela, width=largura)
    caixa.pack(pady=10)

    Button(
        tela,
        text="Confirmar",
        command=lambda: conferir_resposta(
            caixa.get(),
            resposta
        )
    ).pack(pady=10)


def atividade_email():
    criar_tela("email", "Atividade - Email", 30)


def atividade_atalho():
    criar_tela("atalho", "Atividade - Atalho", 10)


def atividade_google():
    criar_tela("google", "Atividade - Navegador", 25)


def iniciar_programa():
    global texto_pontos, pontuacao

    inicializar_banco()
    pontuacao = carregar_pontuacao()

    janela_principal = Tk()
    janela_principal.title("Curso Básico de Informática")
    janela_principal.geometry("320x300")

    Label(
        janela_principal,
        text="Escolha uma atividade"
    ).pack(pady=10)

    Label(
        janela_principal,
        text="Dificuldade:"
    ).pack(pady=(5,0))

    variavel_dificuldade = StringVar(janela_principal)
    variavel_dificuldade.set("Não selecionado")

    opcoes = ["Não selecionado", "Fácil", "Médio", "Difícil"]

    OptionMenu(janela_principal, variavel_dificuldade,*opcoes).pack(pady=5)

    texto_pontos = Label(
        janela_principal,
        text=f"Pontuação: {pontuacao}"
    )
    texto_pontos.pack(pady=5)

    Button(
        janela_principal,
        text="Treino de Email",
        width=22,
        command=atividade_email
    ).pack(pady=5)

    Button(
        janela_principal,
        text="Mover Arquivos",
        width=22,
        command=atividade_atalho
    ).pack(pady=5)

    Button(
        janela_principal,
        text="Usar Google",
        width=22,
        command=atividade_google
    ).pack(pady=5)

    Button(
        janela_principal,
        text="Fechar",
        width=22,
        command=janela_principal.destroy
    ).pack(pady=15)

    janela_principal.mainloop()


iniciar_programa()
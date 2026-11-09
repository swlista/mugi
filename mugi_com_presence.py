
import customtkinter as ctk
import pyautogui
import ctypes
from ctypes import wintypes
import threading
import time
import os
import sys
from mugi_presence import iniciar_presence, encerrar_presence

# =========================
# CAMINHOS DOS ARQUIVOS
# =========================

def resource_path(nome):
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base, nome)


# =========================
# CONFIGURAÇÕES
# =========================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

FUNDO = "#FFF0F5"
PAINEL = "#FFE1EB"
ROXO = "#EFA3BD"
ROXO_ESCURO = "#D982A5"
TEXTO = "#654052"
SECUNDARIO = "#A87990"

FONTE = "Comic Sans MS"

parar = threading.Event()
executando = False

# =========================
# DIGITAÇÃO UNICODE
# =========================

INPUT_KEYBOARD = 1
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_KEYUP = 0x0002

ULONG_PTR = ctypes.c_size_t


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR)
    ]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR)
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD)
    ]


class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("ki", KEYBDINPUT),
        ("mi", MOUSEINPUT),
        ("hi", HARDWAREINPUT)
    ]


class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", INPUT_UNION)
    ]


# API DO WINDOWS

user32 = ctypes.WinDLL(
    "user32",
    use_last_error=True
)

SendInput = user32.SendInput

SendInput.argtypes = [
    wintypes.UINT,
    ctypes.POINTER(INPUT),
    ctypes.c_int
]

SendInput.restype = wintypes.UINT


def enviar_unicode(caractere):

    dados = caractere.encode("utf-16-le")

    for i in range(0, len(dados), 2):

        unidade = int.from_bytes(
            dados[i:i + 2],
            "little"
        )

        for flags in (
            KEYEVENTF_UNICODE,
            KEYEVENTF_UNICODE | KEYEVENTF_KEYUP
        ):

            evento = INPUT()
            evento.type = INPUT_KEYBOARD

            evento.union.ki = KEYBDINPUT(
                wVk=0,
                wScan=unidade,
                dwFlags=flags,
                time=0,
                dwExtraInfo=0
            )

            resultado = SendInput(
                1,
                ctypes.byref(evento),
                ctypes.sizeof(INPUT)
            )

            if resultado != 1:
                raise ctypes.WinError(
                    ctypes.get_last_error()
                )


def digitar_unicode(texto, intervalo):

    for caractere in texto:

        if parar.is_set():
            break

        if caractere == "\n":
            pyautogui.press("enter")

        elif caractere == "\r":
            continue

        elif caractere == "\t":
            pyautogui.press("tab")

        else:
            enviar_unicode(caractere)

        time.sleep(intervalo)


# =========================
# JANELA PRINCIPAL
# =========================

app = ctk.CTk()

app.title("Mugi")
app.geometry("850x620")
app.resizable(False, False)
app.configure(fg_color=FUNDO)

# ÍCONE

icone = resource_path("mugi.ico")

if os.path.exists(icone):
    app.iconbitmap(icone)


# =========================
# LAYOUT
# =========================

principal = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

principal.pack(
    fill="both",
    expand=True,
    padx=22,
    pady=22
)


# LATERAL

lateral = ctk.CTkFrame(
    principal,
    width=240,
    fg_color=PAINEL,
    corner_radius=20
)

lateral.pack(
    side="left",
    fill="y",
    padx=(0, 18)
)

lateral.pack_propagate(False)


ctk.CTkLabel(
    lateral,
    text="MUGI",
    font=(FONTE, 30, "bold"),
    text_color=ROXO_ESCURO
).pack(pady=(30, 20))


# =========================
# IMAGEM DA MUGI
# =========================

imagem_path = resource_path("mugi.png")

if os.path.exists(imagem_path):

    from PIL import Image

    imagem = Image.open(imagem_path)

    foto = ctk.CTkImage(
        light_image=imagem,
        dark_image=imagem,
        size=(200, 280)
    )

    ctk.CTkLabel(
        lateral,
        text="",
        image=foto
    ).pack(pady=10)

else:

    ctk.CTkLabel(
        lateral,
        text="MUGI",
        font=(FONTE, 35, "bold"),
        text_color=ROXO_ESCURO
    ).pack(pady=100)


# =========================
# CONTEÚDO
# =========================

conteudo = ctk.CTkFrame(
    principal,
    fg_color="transparent"
)

conteudo.pack(
    side="right",
    fill="both",
    expand=True
)


ctk.CTkLabel(
    conteudo,
    text="Digitador automático",
    font=(FONTE, 25, "bold"),
    text_color=TEXTO
).pack(anchor="w", pady=(8, 4))


ctk.CTkLabel(
    conteudo,
    text="Escreva seu texto e deixe a Mugi trabalhar!",
    font=(FONTE, 14),
    text_color=SECUNDARIO
).pack(anchor="w", pady=(0, 15))


# =========================
# CAIXA DE TEXTO
# =========================

caixa = ctk.CTkTextbox(
    conteudo,
    height=260,
    corner_radius=14,
    fg_color=PAINEL,
    border_color="#E8B5C8",
    border_width=1,
    text_color=TEXTO,
    font=(FONTE, 14),
    wrap="word"
)

caixa.pack(
    fill="both",
    expand=True
)


# =========================
# VELOCIDADE
# =========================

ctk.CTkLabel(
    conteudo,
    text="VELOCIDADE DE DIGITAÇÃO",
    font=(FONTE, 14, "bold"),
    text_color=SECUNDARIO
).pack(anchor="w", pady=(18, 7))


vel_frame = ctk.CTkFrame(
    conteudo,
    fg_color=PAINEL,
    corner_radius=12
)

vel_frame.pack(fill="x")


slider = ctk.CTkSlider(
    vel_frame,
    from_=10,
    to=300,
    progress_color=ROXO,
    button_color="#FFD1DF",
    button_hover_color=ROXO_ESCURO
)

slider.set(50)

slider.pack(
    side="left",
    fill="x",
    expand=True,
    padx=15,
    pady=15
)


valor = ctk.CTkLabel(
    vel_frame,
    text="50 ms",
    font=(FONTE, 14, "bold"),
    text_color=TEXTO,
    width=65
)

valor.pack(
    side="right",
    padx=10
)


def atualizar_velocidade(value):

    valor.configure(
        text=f"{int(value)} ms"
    )


slider.configure(
    command=atualizar_velocidade
)


# =========================
# STATUS
# =========================

status = ctk.CTkLabel(
    conteudo,
    text="Aguardando texto...",
    font=(FONTE, 14),
    text_color=SECUNDARIO
)

status.pack(pady=15)


# =========================
# INICIAR DIGITAÇÃO
# =========================

def digitar():

    global executando

    if executando:
        return

    texto = caixa.get(
        "1.0",
        "end-1c"
    )

    if not texto.strip():

        status.configure(
            text="Digite algum texto primeiro!"
        )

        return

    intervalo = slider.get() / 1000

    parar.clear()
    executando = True

    botao_inicio.configure(
        state="disabled"
    )

    def executar():

        global executando

        mensagem = "Digitação interrompida."

        try:

            for i in range(5, 0, -1):

                if parar.is_set():
                    break

                app.after(
                    0,
                    lambda n=i: status.configure(
                        text=f"Começando em {n}..."
                    )
                )

                time.sleep(1)

            if not parar.is_set():

                app.after(
                    0,
                    lambda: status.configure(
                        text="Mugi está digitando..."
                    )
                )

                digitar_unicode(
                    texto,
                    intervalo
                )

                if parar.is_set():

                    mensagem = "Digitação interrompida."

                else:

                    mensagem = "Texto digitado com sucesso!"

        except Exception as erro:

            mensagem = f"Erro: {erro}"

        finally:

            executando = False

            def finalizar():

                status.configure(
                    text=mensagem
                )

                botao_inicio.configure(
                    state="normal"
                )

            try:

                app.after(
                    0,
                    finalizar
                )

            except RuntimeError:
                pass

    threading.Thread(
        target=executar,
        daemon=True
    ).start()


# =========================
# PARAR DIGITAÇÃO
# =========================

def interromper():

    parar.set()

    status.configure(
        text="Parando a digitação..."
    )


# =========================
# BOTÕES
# =========================

botoes = ctk.CTkFrame(
    conteudo,
    fg_color="transparent"
)

botoes.pack(
    fill="x",
    pady=8
)


botao_inicio = ctk.CTkButton(
    botoes,
    text="COMEÇAR",
    command=digitar,
    height=45,
    corner_radius=12,
    fg_color=ROXO,
    hover_color=ROXO_ESCURO,
    text_color="#FFFFFF",
    font=(FONTE, 16, "bold")
)

botao_inicio.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 8)
)


botao_parar = ctk.CTkButton(
    botoes,
    text="PARAR",
    command=interromper,
    height=45,
    corner_radius=12,
    fg_color="#C77D9C",
    hover_color="#AD6484",
    text_color="#FFFFFF",
    font=(FONTE, 16, "bold")
)

botao_parar.pack(
    side="right",
    fill="x",
    expand=True
)


# =========================
# EXECUÇÃO E RICH PRESENCE
# =========================

def fechar_aplicativo():
    encerrar_presence()
    app.destroy()


app.protocol("WM_DELETE_WINDOW", fechar_aplicativo)
iniciar_presence()
app.mainloop()

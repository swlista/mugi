import time

# Cole aqui o Application ID da aplicação criada no Discord Developer Portal.
CLIENT_ID = "1398116538980110468"

# Chave do Art Asset cadastrado no portal (não é o nome do arquivo .ico).
IMAGEM = "mugi_icon"

rpc = None


def iniciar_presence():
    global rpc

    try:
        from pypresence import Presence

        conexao = Presence(CLIENT_ID)
        conexao.connect()
        conexao.update(
            state="Jogando mugi.exe",
            details="Digitando...",
            large_image=IMAGEM,
            large_text="Mugi",
            start=int(time.time())
        )
        rpc = conexao
        print("Discord Rich Presence conectada.")
    except Exception as erro:
        rpc = None
        print(f"Rich Presence indisponível: {erro}")


def encerrar_presence():
    global rpc

    if rpc is not None:
        try:
            rpc.clear()
        except Exception:
            pass
        try:
            rpc.close()
        except Exception:
            pass
        rpc = None

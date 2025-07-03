import telegram 
import asyncio


# --- CONFIGURAÇÕES DE ALERTA ---
METODO_ALERTA = 'telegram' # ou 'email'

# Configurações do Telegram
TELEGRAM_TOKEN = '7715103286:AAGmisvjviGhICSfD81I_yQOFin-Wvt9g8I' # Colar token do BotFather aqui
TELEGRAM_CHAT_ID = '7825204438' # Colar Chat ID aqui

# Configuração do Cooldown
COOLDOWN_SEGUNDOS = 10
ultimo_alerta_enviado = 0

# --- FUNÇÃO DE ALERTA --- 
async def enviar_alerta_telegram(mensagem, photo_path):
    """ Envia uma mensagem de texto simples via Telegram"""
    try:
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        # Usamos bot.send_photo em vez de send_message
        # 'photo=open(photo_path, 'rb')': Nós abrimos o arquivo da imagem em modo de leitura binária ('rb').
        # É assim que as bibliotecas de rede lidam com arquivos que não são texto puro.
        # 'caption=caption': O texto que você quer enviar junto com a imagem.
        
        # Use "await" para executar a função assíncrona
        # await bot.send_message(chat_id=TELEGRAM_CHAT_ID, photo=open(photo_path, 'rb'), caption=caption)
        # print(f"Alerta com foto enviado via Telgram!")
        # return True
        
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mensagem) # Enviar apenas a mensagem
        print(f"Alerta enviado via Telegram: '{mensagem}'")
        return True
        
        
    except Exception as e:
        print(f"Erro ao enviar alerta via Telegram: '{e}'")
        return False
        
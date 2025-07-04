# projeto_webcam
Esse projeto visa a criação de uma aplicação que acessa a camera do computador e faz uma detecção de movimento, e então envia um alerta contendo o print do momento que foi detectado o movimento anexado à hora e dia da detecção.

## Criando o bot de alerta no Telegram
### 1° Passo: Criar "Bot" assistente no Telegram
- No telegram, pocure por um bot chamado "BotFather"
- Inicie uma conversa digitando: ``` /newbot ```
- Digite o nome do seu bot (ex: "Novo Alerta de Câmera")
- Digite o nome de usuário, o nome deve ser único e terminar com "bot" (ex: "NovoAlertaCamera_bot")
- O BotFather vai dar uma mensagem de sucesso e apresentar ```um token de API```
- Copie e guarde o token, ele é a 'senha' do bot

### 2° Passo: Obter a "Caixa de Entrada"(Chat ID)
- No telegram, encontre o bot criado e envie qualquer mensagem
- Navegue para a seguinte url, substituindo o "SEU_TOKEN_AQUI" pelo token copiado
```` https://api.telegram.org/botSEU_TOKEN_AQUI/getUpdates ```
- Na url tera um texto (JSON). Procure por "chat":{"id":123456789, ...}. O número que aparece em "id" é o seu CHATI ID. Copie e guarde o número

### 3° Passo: Integrar TOKEN e CHAT ID no .env
- Na raiz do projeto crie um arquivo ```.env```
- Nesse arquivo adicione o TOKEN e o CHAT_ID da seguinte forma:
```

TELEGRAM_TOKEN = "SEU_TOKEN_AQUI_SEM_ASPAS_DUPLAS"
TELEGRAM_CHAT_ID = "SEU_CHAT_ID_AQUI_SEM_ASPAS_DUPLAS"


```



## Rodar projeto
**Acesse o repositório do app e digite no terminal:**
```
python app.py
```

**Ou, da raiz do projeto, digite no terminal o especificando o caminho do arquivo app.py:**
```
python webcam/app.py
```



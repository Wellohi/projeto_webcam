import cv2
import time
import alerta_module

def iniciar_webcam():
    """
    Inicia a captura de vídeo da webcam e exibe o feed em uma janela.
    A janela pode ser fechada pressionando 'q' ou clicando no 'X'.
    """
    
    # Nome da janela
    window_name = 'Webcam'

    # Inicializa a captura de vídeo da webcam (geralmente o dispositivo 0)
    # Se tiver mais de uma webcam, os índices podem ser 1, 2, etc.
    captura = cv2.VideoCapture(0)
    
    # --- Passo 1: Inicializar o modelo de fundo ---
    # Ele começa como None. É criado no primeiro loop.
    # É preciso usar imagens de ponto flutuante para a matemática da média
    fundo_medio = None
    
    # --- O 'alpha' da média móvel. Controla a velocidade de adaptação ---
    alpha = 0.05 # Valor inicial. Quanto maior mais rapido se adapta
    
    if not captura.isOpened():
        print("Erro: Não foi possivel abrir a câmera")
        return
    
    print(f"Detecção iniciada. Alertas serão enviados a cada {alerta_module.COOLDOWN_SEGUNDOS} segundos, se houver movimento.")

    while True:
        ret, frame = captura.read()
        if not ret:
            break
        

    # Variável para indicar se há movimento no quadro atual
        movimento_detectado = False
        
        # --- Passo 2: Atualizar modelo de fundo ---
        # Converter para escala de cinza
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Aplica desfoque Gaussiano para suavizar (Terminar com 1 sempre)
        cinza = cv2.GaussianBlur(cinza, (9, 9), 0)  # Aumente para ficar menos sensível, abaixe para maior sensibilidade
    
        
        if fundo_medio is None:
            fundo_medio = cinza.copy().astype("float")
            continue
        
        # --- Passo 3 : Atualização do fundo médio ---
        cv2.accumulateWeighted(cinza, fundo_medio, alpha)
        
        # --- Passo: 4 Converter o fundo de float para inteiro de 8-bits para visualização e comparação --- 
        fundo_para_diff = cv2.convertScaleAbs(fundo_medio)

        # Calcula a diferença absoluta entre o quadro atual e o de referência
        diferenca = cv2.absdiff(fundo_para_diff, cinza)
        
        # Se um pixel tem uma diferença maior que 30, ele se torna branco (255), senão preto (0)
        thresh = cv2.threshold(diferenca, 30, 255, cv2.THRESH_BINARY)[1]
              
        # Dilatar a imagem do threshold para preencher buracos e destacar o movimento
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # --- Passo 5: Encontrar Contornos ---
        contornos, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # --- Passo 6: FIltrar e Desenhar ---
        for contorno in contornos:
            #Se a área do contorno for muito pequena, ignorá-la (é só ruído)
            if cv2. contourArea(contorno) < 2000: # Aumentar ou diminuir área mínima
                continue
            
            #Se chegar aqui, significa que foi encontrado movimento significativo
            movimento_detectado = True
            
            # Calcula o retângulo que envolve o contorno
            (x, y, w, h) = cv2.boundingRect(contorno)
            # Desenha o retângulo no quadro colorido original
            cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 2)
            
        # Escreve um texto na tela se houver movimento
        if movimento_detectado:
            tempo_atual = time.time()
            if (tempo_atual - alerta_module.ultimo_alerta_enviado) > alerta_module.COOLDOWN_SEGUNDOS:
                print("Movimento detectado! Verificando cooldown...")
                
                # Definir nome do arquivo para a "evidência"
                nome_arquivo_alerta = "alerta_movimento.jpg"
                
                # Salvar o frame de movimento com o nome definido
                cv2.imwrite(nome_arquivo_alerta, frame)
                
                if alerta_module.METODO_ALERTA == "telegram":
                    #chamar a  função, passando legenda e caminho do arquivo
                    mensagem_alerta = f"ALERTA: Movimento detectado às {time.strftime("%H:%M:%S de %d/%m/%Y")}"
                    # Use asynco.run() para executar a fução async a partir do código síncrono
                    if alerta_module.asyncio.run(alerta_module.enviar_alerta_telegram(mensagem_alerta, nome_arquivo_alerta)):
                        # Atualiza o tempo se o alerta for envado com sucesso
                        alerta_module.ultimo_alerta_enviado = tempo_atual
                
            cv2.putText(frame, "Movimento Detectado!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "Sem Movimento", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
        # Exbe o resultado          
        cv2.imshow(window_name, frame)
        
        # Para debug, ver as outras janelas:
        # cv2.imshow("Threshold (Diferenca em Branco e Preto)", thresh)
        # cv2.imshow("Diferenca de Quadros", diferenca)

        # Atualiza o quadro de referência (opcional, mas pode ser útil)
        # Para uma detecção mais simples, você pode comentar a linha abaixo.
        # Assim, a comparação será sempre com o PRIMEIRO quadro.
        # Descomente se quiser que ele se adapte a novas condições de fundo lentamente.
        # fundo_medio = cinza 
        
        # Condição de saída
        # Condição 1: A tecla 'q' foi pressionada?
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print('Fechando Webcam pelo "q"')
            break
        
        # Condição 2: Clicar no X
        #Verificar propriedade 'WND_PRP_VISIBLE
        try:
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                print('Janela fechada pelo "X"')
                break
        except cv2.error as e:
            print(f'Erro ao verificar a janela: {e}')
            break
            
            
    captura.release()
    cv2.destroyAllWindows()
        

if __name__ == '__main__':
    print('Executando modulo de webcam diretamente para teste')
    iniciar_webcam()


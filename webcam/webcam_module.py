import cv2


def iniciar_webcam():
    """
    Inicia a captura de vídeo da webcam e exibe o feed em uma janela.
    A janela pode ser fechada pressionando 'q' ou clicando no 'X'.
    """
    
    # É uma boa prática guardar o nome da janela em uma variável.
    # Isso evita erros de digitação e facilita a manutenção.
    window_name = 'Webcam'

    # Inicializa a captura de vídeo da webcam (geralmente o dispositivo 0)
    # Se tiver mais de uma webcam, os índices podem ser 1, 2, etc.
    captura = cv2.VideoCapture(0)
    
    # --- Passo 1: Inicializar o quadro de referência ---
    # Ele começa como None, pois ainda não temos o primeiro quadro
    quadro_referencia = None
    
    while True:
        ret, frame = captura.read()
        if not ret:
            break

    # Variável para indicar se há movimento no quadro atual
        movimento_detectado = False
        
        # --- Passo 2: Pré-Processar a imagem ---
        # Converter para escala de cinza
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Aplica desfoque Gaussiano para suavizar
        cinza = cv2.GaussianBlur(cinza, (21, 21), 0)
        
        if quadro_referencia is None:
            quadro_referencia = cinza
            continue
        
        # --- Passo 3 : Calcular a Diferença ---
        diferenca = cv2.absdiff(quadro_referencia, cinza) # Calcula a diferença absoluta entre o quadro atual e o de referência

        # --- Passo: 4 Limiarização (Thresholding) --- 
        # Se um pixel tem uma diferença maior que 30, ele se torna branco (255), senão preto (0) 
        thresh = cv2.threshold(diferenca, 30, 255, cv2.THRESH_BINARY)[1]
        
        # Dilatar a imagem do threshold para preencher buracos e destacar o movimento
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # --- Passo 5: Encontrar Contornos ---
        contornos, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # --- Passo 6: FIltrar e Desenhar ---
        for contorno in contornos:
            #Se a área do contorno for muito peuqna, ignorá-la (é só ruído)
            if cv2. contourArea(contorno) < 1000:
                continue
            
            #Se chegar aqui, significa que foi encontrado movimento significativo
            movimento_detectado = True
            
            # Calcula o retângulo que envolve o contorno
            (x, y, w, h) = cv2.boundingRect(contorno)
            # Desenha o retângulo no quadro colorido original
            cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 2)
            
        # Escreve um texto na tela se houver movimento
        if movimento_detectado:
            cv2.putText(frame, "Movimento Detectado!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "Sem Movimento", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
        # Exbe o resultado          
        cv2.imshow(window_name, frame)
        # Para debug, você também pode querer ver as outras janelas:
        cv2.imshow("Threshold (Diferenca em Branco e Preto)", thresh)
        cv2.imshow("Diferenca de Quadros", diferenca)

        # Atualiza o quadro de referência (opcional, mas pode ser útil)
        # Para uma detecção mais simples, você pode comentar a linha abaixo.
        # Assim, a comparação será sempre com o PRIMEIRO quadro.
        # Descomente se quiser que ele se adapte a novas condições de fundo lentamente.
        # quadro_referencia = cinza 
        
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
        

    # # Verifica se a webcam foi aberta corretamente
    # if not captura.isOpened():
    #     print('Não foi possível abrir a câmera!') 
    # else:
    #     while True:
    #         ret, frame = captura.read()
            
    #         if not ret:
    #             print('Não foi possível capturar o frame!')
    #             break
            
    #         # Usamos a variável com o nome da janela aqui.
    #         cv2.imshow(window_name, frame)
            
           

if __name__ == '__main__':
    print('Executando modulo de webcam diretamente para teste')
    iniciar_webcam()


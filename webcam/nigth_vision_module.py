import cv2 
import numpy as np

def iniciar_nigth_vision():
    """
    Inicia a captura de vídeo da webcam e exibe o feed em uma janela.
    A janela pode ser fechada pressionando 'q' ou clicando no 'X'.
    """

    # Inicia captura de vídeo
    captura = cv2.VideoCapture(0)
    # Nome da janela
    window_name = 'Webcam'
    
    
    
    if not captura.isOpened():
        print("Erro ao abrir a camera!")
    else:
        # Loop de captura e processamento de frames
        while True:
            # ret: boolean, indica se a captura foi bem sucedida
            # frame: array numpy, comtem a imagem capturada
            ret, frame = captura.read()
            
            # Verifica se a captura foi bem sucedida
            if not ret:
                break
            
            # Converter para escala de cinza
            cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Aumentar o brilho
            
            # Verifica se a câmera foi aberta corretamente
            # A função cv2.add() soma um valor a cada pixel. Se a soma passar de 255 (branco),
            # ela mantém em 255, evitando "estourar" a imagem.
            # O valor '40' é o nosso fator de brilho
            # brilho_aumentado = cv2.add(cinza, 40)
            
            # Permite ajustar o contraste (alpha) e o brilho (beta) de uma só vez.
            # alpha > 1 aumenta o contraste, beta aumenta o brilho
            visao_noturna = cv2.convertScaleAbs(cinza, alpha=1.2, beta=40) 


            # Aplica a Coloração Verde
            # OpenCV trabalha com padrao de cor BGR(BLue, Green, Red)
            # Para criar o efeito verde, é necessário criar uma imagem com os canaiz azul e vermelho zerados
            # Depois usar a imagem de brilho aumentado como o canal verde
            
            # Criar matriz cheia de zeros com as mesmas dimensões da imagem
            zeros = np.zeros(frame.shape[:2], dtype='uint8')
            
            # cv2.merge() para combinar os canais B, G, R
            # Canal Azul (B): zeros
            # Canal Verde (G): nossa imagem com brilho aumentado
            # Canal Vermelho (R): zeros
            frame_visão_noturna = cv2.merge([zeros, visao_noturna, zeros])
                    
                    
            # Exibe o frame capturado em uma janela
            # frame: imagem a ser exibida 
            cv2.imshow(window_name, frame_visão_noturna)
            
            ### Fechar caso aperte na tecla 'Q' ###
            # Aguarda por 1ms por uma tecla pressionada
            # & 0xFF garante que apenas os 8 bits menos significativos sejam considerados
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            ### Fechar ao clicar no 'X' da janela ###
            try:
                # 'cv2.WND_PROP_VISIBLE' especifica que queremos saber se a janela está visível.
                # A função retorna 0.0 se a janela foi fechada (não visível).
                    # A condição '< 1' é usada para capturar o caso de janela fechada (0.0)
                if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                   break
            except cv2.error as e:
                print(f"Erro ao verificar a janela: {e}.")
        
    captura.release()
    cv2.destroyAllWindows()
    
if __name__ =='__main__':
    iniciar_nigth_vision()
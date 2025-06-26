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

    # Verifica se a webcam foi aberta corretamente
    if not captura.isOpened():
        print('Não foi possível abrir a câmera!')
    else:
        while True:
            ret, frame = captura.read()
            
            if not ret:
                print('Não foi possível capturar o frame!')
                break
            
            # Usamos a variável com o nome da janela aqui.
            cv2.imshow(window_name, frame)
            
            # Condição 1: A tecla 'q' foi pressionada?
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print('Fechando Webcam pelo "q"')
                break
            
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


import time
import sys


def animacao_timer_module(duracao):
    """
    Exibe uma animação de loading no terminal.
    
    Args:
        duracao (int): Duração da animação em segundos.
    """
    frames_animacao = ['[_____]','[=____]','[==___]','[===__]','[====_]','[=====]']

    tempo_inicio = time.time()
    i = 0
    while (time.time() - tempo_inicio) < duracao:
        # 1. Seleciona o frame atual
        frame_atual = frames_animacao[i % len(frames_animacao)]
        # 2. Escreve o frame no terminal
        sys.stdout.write(f'\rCarregando WebCam... {frame_atual}')
        # 3. Força a exibição imediata
        sys.stdout.flush()
        # 4. Pausa para criar o efeito de animação
        tempo = duracao / 5.1 # Ajuste do tempo para completar a animação antes do tempo acabar
        time.sleep(tempo)
        # 5. Avança para o proximo prame
        i += 1
        
    print('\nSucessfully Loaded!')

if __name__ == '__main__':
    animacao_timer_module(5)
import os
import pygame

voice1 = 'en-GB-SoniaNeural'
voice2 = 'en-US-GuyNeural'
voice3 = "en-US-ChristopherNeural"
voice4 = "en-US-SteffanNeural"
def speak(data):
    command = f'edge-tts --voice "{voice4}" --text "{data}" --write-media "data.mp3"'
    os.system(command)

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("data.mp3")

    try:
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(e)
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()


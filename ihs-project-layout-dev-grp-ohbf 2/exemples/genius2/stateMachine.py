#imports
import pygame
import random
import time
import serial
import read as rd
from codArduino import Arduino

#constants 
FONT_SIZE = 32
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Led:
    def __init__(self, color, pos, circle):
        self.color = color
        self.position = pos #vector2

    def getColor(self):
        a = random.randint(0, 1000)
        if(a % 2 == 0):
            self.color = 'green'
        else:
            self.color = 'red'
        


def main():
    # pygame setup
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    pygame.display.set_caption("Genius2")
    font = pygame.font.Font(None, FONT_SIZE) # Define the font for displaying text
    title_font = pygame.font.Font(None, 2*FONT_SIZE)
    screen.fill("yellow")
    arduino = Arduino()

    #### GLOBAL #####
    ## game variables
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    prop_pos = pygame.Vector2(10, screen.get_height() / 2)
    menu_flag = True
    global_game = 1
    display_level = True
    countdown_flag = True
    global_sequence = []
    global_level = 1
    rd.writeButton(0x00)

    ###state machine variables
    state = "Início"
    action = "Página Inicial"
    flag = True
    isStartPressed = False
    isSequencePrinted = False
    inputFoiLido = False
    inputErrado = False 
    nxLevel = False
    nVidas = 2
    nRepeticoes = 3
    despauseSolicitado = False
    pauseSolicitado = False
    inputCorreto = False
    repeticaoSolicitada = False
    recomecar = False
    tempoDeSolucao = 0
    holderTempoDeSolucao = 0

    #de mentirinha kkkk
    LEITURAiSoVER = False
    LEITURAiScORRECT = False
    PAUSEfOIsOLICITADO = False
    REPETICAOfOIsOLICITADA = False
    BOTAOdEdESPAUSEmOVIDO = False
    TEMPOrEGISTRADO = False
    BOTAOdErECOMCAR = False
    DISTANCIAmINIMAuLTRAPASSADA = False

    ##help functions:

    def clean():
        screen.fill("yellow")
        pygame.display.flip()

    def countdown():
        for i in range(0,3):
            clean()
            text = title_font.render(str(3 - i), True, "red")
            screen.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/2 - text.get_height()/2))
            pygame.display.flip()
            time.sleep(1)

    def drawSequence():
        # Define the start time
        start_time = time.time()

        # Duration of each color change
        duration = 0.75

        # Loop until the desired duration is reached
        while time.time() - start_time < duration:
            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Draw the sequence
            for note in global_sequence:
                led_pos = pygame.Vector2(400 + 100*note, screen.get_height() / 2)
                pygame.draw.circle(screen, "green", led_pos, 30)
                pygame.display.flip()
                rd.ledOn(note)
                arduino.apitar()
                time.sleep(0.70)  # Sleep half the time
                pygame.draw.circle(screen, "red", led_pos, 30)
                pygame.display.flip()
                rd.ledsOff()
                time.sleep(0.5)  # Sleep half the time

        clean()


    def updateSequence():
        global_sequence.append(random.randint(1,4))

    def resetLeds():
        for i in range(1,5):
            led_pos = pygame.Vector2(400 + 100*i, screen.get_height() / 2)
            pygame.draw.circle(screen, "red", led_pos, 30)

        pygame.display.flip()
        time.sleep(2)

    def checkQuit():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    def printErro(string):
        clean()
        text = title_font.render(string, True, "red")
        screen.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/2 - text.get_height()/2))
        pygame.display.flip()
        time.sleep(1)
        clean()


    for i in range(0,4): updateSequence()
    while running:
        if (state == "Início"):
            action = "Página Inicial" 
            if (isStartPressed):
                isStartPressed = False
                state = "Printando Sequencia"
            
        
        elif (state == "Printando Sequencia"):
            action = "Printar Sequencia"
            if (isSequencePrinted):
                isSequencePrinted = False
                state = "Lendo"
            
        
        elif (state == "Lendo"):
            
            action = "Ler"
            
        
        elif (state == "Pause"):
            action = "Pausar"
            if (despauseSolicitado):
                state = "Lendo"
                despauseSolicitado = False
            
        
        elif (state == "Printando Tempo"):
            action = "Printar Tempo"
            if (nxLevel):
                state = "Printando Sequencia"
                nxLevel = False
            
        
        elif (state == "Fim"):
            action = "Finalizar"
            if(recomecar):
                state = "Inicio"
                recomecar = False
            
        
        else: 
            print("execution error at states :p") 
            flag = False

##------------- ACTIONS -------------------------------------------------------##

        if (action == "Página Inicial"):
            
            while(menu_flag):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                title = title_font.render("GENIUS 2!", True, "red")
                screen.blit(title, (SCREEN_WIDTH/2 - title.get_width()/2, SCREEN_HEIGHT/2 - title.get_height()/2))

                text = font.render("Press r to start!", True, "black")
                screen.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, (SCREEN_HEIGHT/2 - text.get_height()/2) + 40))
                

                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    menu_flag = False
                    isStartPressed = True
                    clean()
                    
                pygame.display.flip()
        
        elif (action == "Printar Sequencia"):
            print("morre a criatura e o planeta sente a dor...")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if(display_level):
                clean()
                display_level = not display_level
                lvlarr = str(global_level)
                level_str = "LEVEL"+lvlarr
                print(lvlarr[0])
                print(type(lvlarr[0]))
                if (global_level < 10):
                    rd.writeTime([10,11,0,int(lvlarr[0])])    
                else: rd.writeTime([10,11,int(lvlarr[0]),int(lvlarr[1])])
                ## ------ print de vidas e repeticoes ---- ##  
                text = title_font.render(level_str, True, "black")
                screen.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/2 - text.get_height()/2))
                pygame.display.flip()
                time.sleep(1)
                clean()

            rd.writeInfo([0,nVidas,0,nRepeticoes])
            resetLeds()
            drawSequence()

            isSequencePrinted = True
            tempoDeSolucao = time.time()
            holderTempoDeSolucao = 0
            state = "Lendo"

        elif (action == "Ler"):
            print("lendo o input")
            resetLeds()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            result = rd.read_switches(global_sequence, nRepeticoes, arduino)
            print(result)

            if(result == "acertou"):
                inputCorreto = True
                global_level += 1
                display_level = True
                tempoDeSolucao = time.time() - tempoDeSolucao
                updateSequence()

            elif(result == "errou"):
                printErro("ERROU, BURRO!!!!") 
                inputErrado = True
                nVidas -= 1
            
            elif(result == "repeticao"):
                nRepeticoes -= 1
                repeticaoSolicitada = True

            elif(PAUSEfOIsOLICITADO):
                pauseSolicitado = True
                        
            elif(DISTANCIAmINIMAuLTRAPASSADA):
                inputFoiLido = True
                print("Distancia minima ultrapassada")

            if (nVidas <= 0):
                state = "Fim"
                nVidas = 5
            
            elif (inputErrado):
                state = "Printando Sequencia"
                inputErrado = False
            
            elif (inputCorreto):
                state = "Printando Tempo"
                inputCorreto = False
                            
            elif (pauseSolicitado):
                state = "Pause"
                pauseSolicitado = False
            
            elif (repeticaoSolicitada):
                state = "Printando Sequencia"
                repeticaoSolicitada = False
        
        elif (action == "Pausar"):
            holderTempoDeSolucao = time.time() - tempoDeSolucao + holderTempoDeSolucao
            if(BOTAOdEdESPAUSEmOVIDO):
                tempoDeSolucao = time.time()
                despauseSolicitado = True
            
        
        elif (action == "Printar Tempo"):
            print(tempoDeSolucao + holderTempoDeSolucao)
            tempoTotal = tempoDeSolucao + holderTempoDeSolucao
            tempoTotal = int(tempoTotal)
            print(tempoTotal)
            time_arr = [0,0,0,0]
            tempoTotal = str(tempoTotal)

            for i in range(0, len(tempoTotal)):
                time_arr[len(time_arr) - i - 1] = int(tempoTotal[len(tempoTotal) - i - 1])

            rd.writeTime(time_arr)
            time.sleep(2)
            nxLevel = True
        
        elif (action == "Finalizar"):
            printErro("GAME OVER, BOBINHO!!!!")
            if(BOTAOdErECOMCAR):
                recomecar = True
            
        
        else:
            print("execution erro at actions :")
            flag = False


if __name__ == "__main__":
  main()

pygame.quit()
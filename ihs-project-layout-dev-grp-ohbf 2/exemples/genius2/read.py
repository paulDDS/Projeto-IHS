import os, sys
from fcntl import ioctl
import time
import codArduino as ardu
# ioctl commands defined at the pci driver
RD_SWITCHES   = 24929
RD_PBUTTONS   = 24930
WR_L_DISPLAY  = 24931
WR_R_DISPLAY  = 24932
WR_RED_LEDS   = 24933
WR_GREEN_LEDS = 24934

ZERO = 0xC0
ONE = 0XF9
TWO = 0XA4
THREE = 0XB0
FOUR = 0X99
FIVE = 0X92
SIX = 0x82
SEVEN = 0xF8
EIGHT = 0x0
NINE = 0x90
LETTER_E = 0x86
LETTER_L = 0xC7 


def translate_number(n):
    if(n==0): return ZERO
    elif(n==1): return ONE
    elif(n==2):return TWO
    elif(n==3):return THREE
    elif(n==4):return FOUR
    elif(n==5):return FIVE
    elif(n==6):return SIX
    elif(n==7):return SEVEN
    elif(n==8):return EIGHT
    elif(n==9):return NINE
    elif(n==10): return LETTER_L    
    elif(n==11): return LETTER_E



def get_fd():
    if len(sys.argv) < 2:
        print("Error: expected more command line arguments")
        print("Syntax: %s </dev/device_file>"%sys.argv[0])
        exit(1)

    fd = os.open(sys.argv[1], os.O_RDWR)
    return fd

def ledOn(number):
    
    fd = get_fd()

    led = 2**(-number + 18)
    ioctl(fd, WR_RED_LEDS)
    retval = os.write(fd, led.to_bytes(3, 'little'))

def ledsOff():

    fd = get_fd()

    number = 0
    ioctl(fd, WR_RED_LEDS)
    retval = os.write(fd, number.to_bytes(3, 'little'))


def writeLedSequence(sequence, fd):
    indexed_sequence = []
    number = 0
    for i in range(len(sequence)):
        number += 2**(-sequence[i] + 18)
        ioctl(fd, WR_RED_LEDS)
        retval = os.write(fd, number.to_bytes(3, 'little'))
        time.sleep(0.8)
        number = 0
        ioctl(fd, WR_RED_LEDS)
        retval = os.write(fd, number.to_bytes(3, 'little'))



def writeTime(time_arr):
    fd = get_fd()

    data = [translate_number(n) for n in time_arr]

    conv_arr = []
    for i in range (len(data)):
        conv_arr.append(data[i]<<((3 - i)*8))

    number = 0    
    for n in conv_arr:
        number += n


    number = number.to_bytes(4, 'little')
    print(number)

    ioctl(fd, WR_R_DISPLAY)
    retval = os.write(fd, number)


def writeInfo(time_arr):
    fd = get_fd()

    data = [translate_number(n) for n in time_arr]

    conv_arr = []
    for i in range (len(data)):
        conv_arr.append(data[i]<<((3 - i)*8))

    number = 0    
    for n in conv_arr:
        number += n


    number = number.to_bytes(4, 'little')
    print(number)

    ioctl(fd, WR_L_DISPLAY)
    retval = os.write(fd, number)

def check_switches(switches_old, switchs_now):
    # converte big end (logica de usuario final) pra little end (logica da programação)
    switches = []
    switches_that_changed = switches_old ^ switchs_now
    #for i in range(18):
    i=18
    while(2**(i-1) > switches_that_changed):
        i-= 1
        if(i == 0): break
    while(i>0):
        if(2**(i-1) <= switches_that_changed):
            switches_that_changed -= 2**(i-1)
            switches.append((-i) + 19)
        i-=1
    return switches

def check_buttons(buttons_old, buttons_now):
    buttons = []
    buttons_that_changed = (buttons_old ^ buttons_now ) & (~ buttons_now)
    print((buttons_old ^ buttons_now ) & (~ buttons_now))
    i=4
    while(2**(i-1) > buttons_that_changed):
        i-= 1
        if(i == 0): break
    while(i>0):
        if(2**(i-1) <= buttons_that_changed):
            buttons_that_changed -= 2**(i-1)
            buttons.append((-i) + 23)
        i-=1
    return buttons


def check_failure(genius_answer, player_answer):
    for i in range(len(player_answer)):
        if(player_answer[i] != genius_answer[i]):
            return True
    return False
        
def read_distance(arduino):
    dst = arduino.pegarDistancia()
    dst = dst.split(":")[1][0:-1]
    dst = int(dst)

    if((dst > 20 ) and (dst < 1000)):
        return False
    else:
        return True

def writeButton(number):
    fd = get_fd()
    number = number.to_bytes(4, 'little')
    ioctl(fd, WR_GREEN_LEDS)
    retval = os.write(fd, number)

def read_switches(correct_answer, nRepeticoes, arduino):
    ret = False

    if len(sys.argv) < 2:
        print("Error: expected more command line arguments")
        print("Syntax: %s </dev/device_file>"%sys.argv[0])
        exit(1)

    fd = os.open(sys.argv[1], os.O_RDWR)

    pediuRepeticao = False
    reading = True
    failure = False
    count = 0

    
    ioctl(fd, RD_SWITCHES)
    switches_old = os.read(fd, 4) # read 4 bytes for switches_old switch state
    

    ioctl(fd, RD_PBUTTONS)
    buttons_old = os.read(fd, 1)

    history = []

    while(reading):
        ioctl(fd, RD_SWITCHES)
        switches_now = os.read(fd, 4) # read 4 bytes and store in red var

        if(switches_old != switches_now):
            print("mudou!")
            int_switches_now = int.from_bytes(switches_now, 'little')
            int_switches_old = int.from_bytes(switches_old, 'little')
            check_switch_changes = check_switches(int_switches_old, int_switches_now)
            if len(check_switch_changes) > 1:
                print("Não mude mais de um switch ao mesmo tempo!")
            elif len(check_switch_changes) == 1:
                history.append(check_switch_changes[0])
                print(history)


            switches_old = switches_now

        stop = 0x1
        stop = stop.to_bytes(4,"little")
        if(switches_old == stop):
            reading = False

        ioctl(fd, RD_PBUTTONS)
        buttons_now = os.read(fd, 1)

        if(buttons_old != buttons_now):
            print("botões mudaram!")
            int_buttons_now = int.from_bytes(buttons_now, 'little')
            int_buttons_old = int.from_bytes(buttons_old, 'little')
            buttons_old = buttons_now
            check_button_changes = check_buttons(int_buttons_old, int_buttons_now)
            if len(check_button_changes) > 1:
                print("Não mude mais de um switch ao mesmo tempo!")
            elif len(check_button_changes) == 1 :
                history.append(check_button_changes[0])
                print(history)
                if (history[len(history)-1] == 22):
                    writeButton(0x03)
                    time.sleep(0.3)
                    writeButton(0x00)
                    if (nRepeticoes > 0):
                        print("ATIVEI REPETICAO")
                        return "repeticao"
                    else: 
                        print("nao ha mais repeticoes")
                        history.pop()
                        failure = True 

                
        
        failure = check_failure(correct_answer, history)
        if(len(history) == len(correct_answer)):
            print("Parabéns, você acertou!")
            reading = False
            print("coloquei true")
            return "acertou"
        if(failure):
            print("Você errou, perdeu uma vida!")
            reading = False
            print("coloquei false")
            return "errou"


        if(not read_distance(arduino)):
            return "errou"



        time.sleep(0.034)
        count += 1

#-------------------------------------------------------------      


    print("execucao finalizada")    


    os.close(fd)


def main():
    d = [ONE, TWO, THREE, FOUR]
    print(len(d))
    if len(sys.argv) < 2:
        print("Error: expected more command line arguments")
        print("Syntax: %s </dev/device_file>"%sys.argv[0])
        exit(1)

    fd = os.open(sys.argv[1], os.O_RDWR)
    #writeTime(d, fd)
    writeLedSequence([1,2,3,4,5,6], fd)

if __name__ == '__main__':
    main()
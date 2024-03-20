import os, sys
from fcntl import ioctl
import time

# ioctl commands defined at the pci driver
RD_SWITCHES   = 24929
RD_PBUTTONS   = 24930
WR_L_DISPLAY  = 24931
WR_R_DISPLAY  = 24932
WR_RED_LEDS   = 24933
WR_GREEN_LEDS = 24934

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
            buttons.append((-i) + 22)
        i-=1
    return buttons


def check_failure(genius_answer, player_answer):
    for i in range(len(player_answer)):
        if(player_answer[i] != genius_answer[i]):
            return True
    return False
        




def main():
    if len(sys.argv) < 2:
        print("Error: expected more command line arguments")
        print("Syntax: %s </dev/device_file>"%sys.argv[0])
        exit(1)

    fd = os.open(sys.argv[1], os.O_RDWR)

    # data to write
    data = 0x90
    ioctl(fd, WR_L_DISPLAY)
    retval = os.write(fd, data.to_bytes(4, 'little'))



    os.close(fd)

if __name__ == '__main__':
    main()
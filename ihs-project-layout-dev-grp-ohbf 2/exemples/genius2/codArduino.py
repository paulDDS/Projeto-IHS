import serial #Importa a biblioteca
import time


class Arduino:

    def __init__(self):
        while True: 
            try:  
                arduino = serial.Serial('/dev/ttyACM0', 9600)
                print('Arduino conectado')
                break

            except:
                pass

        self.arduino = arduino




    def pegarDistancia(self):
        cmd = 'd'
        self.arduino.write(cmd.encode())
        distance = (self.arduino.readline()).decode()

        return distance

    def apitar(self):
        cmd = 'a'
        self.arduino.write(cmd.encode())
        self.arduino.reset_input_buffer()  

# def main():
#     while True:
#         pegarDistancia()
#         apitar()


# def pegarDistancia():
#     arduino.write(cmd.encode())
#     distance = (arduino.readline()).decode()
#     # print(distance)


# def apitar():
#     cmd = 's'
#     arduino.write(cmd.encode())
#     arduino.reset_input_buffer()  


# if __name__ == '__main__':
#     main()
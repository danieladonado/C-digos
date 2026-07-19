'''
import serial as sr

Puerto_serial = sr.Serial('COM5', 9600)

try:
    while True:
        orden = input("Instrucción a ESP32 (On u Off): ").capitalize()
        Puerto_serial.write(orden.encode('UTF-8')) 
        
        if orden=='salir':
            Puerto_serial.close()
            print("Comunicación serie finalizada")
            break
        
except KeyboardInterrupt:
    Puerto_serial.close()
    print("Comunicación serie finalizada")
     '''


import serial as sr

Puerto_serial=sr.Serial('COM5',9600)

try: 
    while True:
        orden=input("Instruccion a ESP32 (00000): ")
        auxiliar=orden+"\n"
        Puerto_serial.write(auxiliar.encode('UTF-8'))

        if orden=='salir':
            Puerto_serial.close()
            print("Comunicacion serie finalizada")
            break
            

except KeyboardInterrupt:
    Puerto_serial.close()
    print("Comunicacion serie finalizada")    


    
    
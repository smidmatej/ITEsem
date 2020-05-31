from multiprocessing import Process
from multiprocessing import 

def ahoj():
    print('Nazdar')
    for i in range(100):
        print('Ahoj')

def cau():
    print('Nazdar')
    for i in range(100):
        print('Cau')

if __name__ == '__main__':

    p1 = Process(target=ahoj())
    p1.start()
    p2 = Process(target=cau())
    p2.start()
    
    p1.join()
    p2.join()
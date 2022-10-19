from bluetooth import *
import time
import os

ANDROID_SOCKET_BUFFER_SIZE = 512
LOCALE = 'UTF-8'
PORT = 0
CHANNEL = 1
UUID = '00001101-0000-1000-8000-00805f9b34fb'
MACADDR = 'B8:27:EB:BF:14:9B'

class Android_communicator:
    
    def __init__(self):
        
        #os.system('sudo hciconfig hci0 piscan')
        
        self.server_sock = None
        self.client_sock = None
        
        self.server_sock = BluetoothSocket(RFCOMM)
        
        while True:
            try:
                self.server_sock.bind((MACADDR, 1))
                break
            except Exception as e:
                print(e, ', retrying..')
                time.sleep(3)
                
        self.server_sock.listen(1)

        self.port = self.server_sock.getsockname()[1]

        '''
        advertise_service(
            self.server_sock,
            'MDP Server Group 34',
            profiles=[SERIAL_PORT_PROFILE],
            service_id = UUID,
            service_classes = [UUID, SERIAL_PORT_CLASS],
            protocols = [ OBEX_UUID ]
        )
        '''
        print('self.server_socket:', str(self.server_sock))

    def connect_android(self):
        while True:
            retry = False

            try:
                print('Now Builing connection with Android Tablet...')

                if self.client_sock is None:
                    print("Waiting for connection on RFCOMM channel %d" % self.port)
                    
                    print('Server Sock:', self.server_sock)
                    print('Please accept the connection request on Android Tablet')
                    self.client_sock, address = self.server_sock.accept()
                    print('Client Sock:', self.client_sock)
                    print("Successfully connected to Android at address: " + str(address))
                    retry = False

            except Exception as error:
                print("Connection with Android failed: " + str(error))
                if self.client_sock is not None:
                    self.client_sock.close()
                    self.client_sock = None

                retry = True

            if not retry:
                break

            print('Retrying Bluetooth Connection to Android...')

    def disconnect_android(self):
        try:
            if self.client_sock is not None:
                self.client_sock.close()
                self.client_sock = None

            print("Android disconnected Successfully")

        except Exception as error:
            print("Android disconnect failed: " + str(error))

    def disconnect_all_android(self):
        try:
            if self.client_sock is not None:
                self.client_sock.close()
                self.client_sock = None

            if self.server_sock is not None:
                self.server_sock.close()
                self.server_sock = None

            print("Android disconnected Successfully")

        except Exception as error:
            print("Android disconnect failed: " + str(error))

    def read_android(self):
        try:
            message = self.client_sock.recv(ANDROID_SOCKET_BUFFER_SIZE).strip().decode(LOCALE)
            print('The message from android:')
            print(message)

            if message is None:
                return None

            if len(message) > 0:
                return message

            return None

        except Exception as error:
            print('Android read process has failed: ' + str(error))
            raise error

    def write_android(self, message):
        try:
            print('To Android Tablet:')
            print(message)
            self.client_sock.send(message)

        except Exception as error:
            print('Android write process has failed: ' + str(error))
            raise error

if __name__ == '__main__':
    A = Android_communicator()
    A.connect_android()
    A.read_android()
    message = 'Hello Android!'
    A.write_android(message)
    print("Android script successfully ran.")
    A.disconnect_all_android()

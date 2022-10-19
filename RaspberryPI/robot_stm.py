import serial
import time

SERIAL_PORT='/dev/ttyUSB0'
BAUD_RATE=115200
LOCALE='UTF-8'


class STM_communicator:
    def __init__(self, serial_port=SERIAL_PORT, baud_rate=BAUD_RATE):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.connection = None

    def connect_stm(self):
        count = 10000
        while True:
            retry = False

            try:
                if count >= 10000:
                    print('Now building connection with STM Board')

                self.connection = serial.Serial(self.serial_port, self.baud_rate)

                if self.connection is not None:
                    print('Successfully connected with STM Board: ' + str(self.connection.name))
                    retry = False

            except Exception as error:
                if count >= 10000:
                    print('Connection with STM Board failed: ' + str(error))
                    time.sleep(3)

                retry = True

            if not retry:
                break

            if count >= 10000:
                print('Retrying STM connection...')
                count = 0

            count += 1

    def disconnect_stm(self):
        try:
            if self.connection is not None:
                self.connection.close()
                self.connection = None

                print('Successfully closed connection with STM')

        except Exception as error:
            print('STM close connection failed: ' + str(error))

    def read_stm(self):
        try:
            message = self.connection.read(4).decode(LOCALE)
            print('From STM:')
            print(message)

            if len(message) > 0:
                return message

            return None

        except Exception as error:
            print('STM read failed: ' + str(error))
            raise error

    def write_stm(self, message):
        try:
            print('To STM:')
            print(message)
            self.connection.write(message.encode())

        except Exception as error:
            print('STM write failed: ' + str(error))
            raise error

if __name__ == '__main__':
    A = STM_communicator()
    A.connect_stm()
    message = "d090"
    A.write_stm(message.encode())
#     while True:
#         A.read_stm()
    print("STM script succesfully ran.")

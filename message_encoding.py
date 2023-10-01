# This is a simulator that runs on mac
import serial
from time import sleep



# class MessageEncoderMeta(type):
#     def __call__(cls, *args, **kwargs):
#         instance = super().__call__(*args, **kwargs)
#         instance.encode(*args, **kwargs)  # Encode the message immediately
#         return instance.message
#

# metaclass=MessageEncoderMeta
class MessageEncoder:
    def __init__(self, message_type, message_data):
        self.message_type = message_type
        self.message = self.encode(message_data)

    def encode(self,message_data):
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    def calculate_checksum(data):
        checksum = 0
        for byte in data:
            checksum ^= byte
        return bytes([checksum])

    def make_serial_message(self, data):
        message_type = self.message_type.encode('utf-8')
        m_string = message_type + b':' + data
        cksum = self.calculate_checksum(m_string)
        to_send = b'<' + m_string + cksum + b'>' + b'\n'
        return to_send


class SensorEncoder(MessageEncoder):
    def __init__(self, message_data):
        super().__init__('sensor', message_data)

    def encode(self, message_data):
        enc_data = (':'.join([f"{str(k)}={str(v)}" for k, v in message_data.items()])).encode('utf-8')
        packet = self.make_serial_message(enc_data)
        return packet



class CommandEncoder(MessageEncoder):
    def __init__(self, message_data):
        super().__init__('cmd', message_data)

    def encode(self, message_data):
        packet = self.make_serial_message(message_data)
        return packet


class DataEncoder(MessageEncoder):
    def __init__(self, message_data):
        super().__init__('data', message_data)

    def encode(self, message_data):
        packet = self.make_serial_message(message_data)
        return packet



# def calculate_checksum(data):
#     checksum = 0
#     for byte in data:
#         checksum ^= byte
#     return bytes([checksum])


# def make_serial_message(m_type: str, message: bytes):
#     message_type = m_type.encode('utf-8')
#     m_string = message_type + b':' + message
#     cksum = calculate_checksum(m_string)
#     to_send = b'<' + m_string + cksum + b'>' + b'\n'
#     return to_send


# def make_sensor_packet(data:dict) -> bytes:
#     enc_data = (':'.join([f"{str(k)}={str(v)}" for k, v in data.items()])).encode('utf-8')
#     packet = make_serial_message('sensor',enc_data)
#     return packet
#
#
# def make_data_packet(data: bytes) -> bytes:
#     packet = make_serial_message('data',data)
#     return packet


# def make_command_packet(data: bytes) -> bytes:
#     packet = make_serial_message('cmd',data)
#     return packet
#

sensor_packet_dict = {'heat': 23.3, 'humid': 0.8, 'reservoir': 'full', 'hopes': 10}


def main():
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 9600, timeout=10)
    if ser is None:
        print("Failed to create serial port")
        exit(1)

    while True:
        print("writing")
        try:
            ser.write(DataEncoder(b"datapacket").message)
            sleep(3)
            ser.write(CommandEncoder(b"command").message)
            sleep(1)
            ser.write(SensorEncoder(sensor_packet_dict).message)

        except:
            print("Write timeout. Continue...")


if __name__ == '__main__':
    main()
    # print('main')
    # enc = SensorEncoder(sensor_packet_dict)
    # print(enc.message)

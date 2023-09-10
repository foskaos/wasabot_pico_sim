import serial

from time import sleep

class MessageEncoder:
    def __init__(self, message_type, message_data):
        self.message = message_data,
        self.message_type = message_type

    @staticmethod
    def calculate_checksum(data):
        checksum = 0
        for byte in data:
            checksum ^= byte
        return bytes([checksum])

    def make_serial_message(self):
        message_type = self.message_type.encode('utf-8')
        m_string = message_type + b':' + self.message
        cksum = self.calculate_checksum(m_string)
        to_send = b'<' + m_string + cksum + b'>' + b'\n'
        return to_send






def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return bytes([checksum])


def make_serial_message(m_type: str, message: bytes):
    message_type = m_type.encode('utf-8')
    m_string = message_type + b':' + message
    cksum = calculate_checksum(m_string)
    to_send = b'<' + m_string + cksum + b'>' + b'\n'
    return to_send


def make_sensor_packet(data:dict) -> bytes:
    enc_data = (':'.join([f"{str(k)}={str(v)}" for k, v in data.items()])).encode('utf-8')
    packet = make_serial_message('sensor',enc_data)
    return packet


def make_data_packet(data: bytes) -> bytes:
    packet = make_serial_message('data',data)
    return packet


def make_command_packet(data: bytes) -> bytes:
    packet = make_serial_message('cmd',data)
    return packet


def main():
    ser = serial.Serial('/dev/cu.SLAB_USBtoUART', 9600, timeout=10)
    if ser is None:
        print("Failed to create serial port")
        exit(1)

    while True:
        print("writing")
        try:
            ser.write(make_data_packet(b"datapacket"))
            sleep(3)
            ser.write(make_command_packet(b"command"))
            sleep(1)
            ser.write(make_sensor_packet({'heat':23.3,'humid':0.8,'reservoir':'full','hopes':10,}))

        except:
            print("Write timeout. Continue...")


if __name__ == '__main__':
    main()





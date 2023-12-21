import io
import fcntl
import time

I2C_SLAVE_COMMAND = 0x0703

def initialize_i2c_device(i2c_address):
    FileHandle = io.open("/dev/i2c-1", "rb", buffering=0)
    # set device address
    fcntl.ioctl(FileHandle, I2C_SLAVE_COMMAND, i2c_address)
    return FileHandle

def read_AD(file_handle):
    values = list(file_handle.read(2))
    return (values[0] * 256 + values[1]) / 4.0  # Return as float

def gassensor():
    i2c_address = 0x4E
    file_handle = initialize_i2c_device(i2c_address)

    ad_value = read_AD(file_handle)
    print("A/D:{}".format(ad_value))

    # Close the file handle before returning
    file_handle.close()

    return ad_value
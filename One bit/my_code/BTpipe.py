from fpga import api
import time
# from img_process import *
from PIL import Image
from one_bit import *


class quickMafths(api): 
    def __init__(self, bitfile):
    	# program bitfile
        super(quickMafths, self).__init__(bitfile)


if __name__ == '__main__':
	# download first.bit from here: https://www.dropbox.com/scl/fo/eqjevkh43lhuwdqvqxdpo/h?dl=0&rlkey=2f0n7rh49xfqyqo1gexuteq52
    dev = quickMafths('BTPipe.bit')

    data_in = bytearray(convert_to_byte_array('lenna.jpg', 150, True))
    data_out = bytearray(len(data_in))
    

    dev.wire_in(0x00, 0b01) # reset
    time.sleep(1)
    dev.wire_in(0x00, 0b00)
    dev.wire_in(0x01, 0b01) # invert bits

    
    dev.write(0x80, data_in)
    dev.read(0xA0, data_out)

    byte_compare(data_in, data_out)
    
    print(count_different_bits(data_in, data_out))

    save_bytearray_to_img(data_out, 'lenna_out.jpg')
    save_bytearray_to_img(data_in, 'lenna_in.jpg')

    # if data_in == data_out:
    #     print("Success")
    #     print(f'container: {data_in} \nread out: {data_out}')
    # else:
    #     print(f'Error: \ncontainer: {data_in} \nread out: {data_out}')



    



		

             





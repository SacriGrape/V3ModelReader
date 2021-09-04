import re
import struct
import matplotlib.pyplot as plt
import math
from pathlib import Path

from numpy import Infinity, isfinite, isnan


# Reading the SRDI file. SRDI contains data on the model
srdi_file = open('./model.srdi', 'rb')
srdi_bytes = srdi_file.read()

srd_file = open('./model.srd', 'rb')
srd_bytes = srd_file.read()
vtx_offsets = []
for m in re.finditer(b'\\x24\\x56\\x54\\x58', srd_bytes):
    vtx_offsets.append(m.start())

rsi_offsets = []
for m in re.finditer(b'\\x24\\x52\\x53\\x49', srd_bytes):
    rsi_offsets.append(m.start())

for offset in vtx_offsets:
    print(f'Offset: {offset}')
    vertex_count = struct.unpack_from('<i', srd_bytes, offset + 24)[0]
    print(f'Vertex count: {vertex_count}')
    rsi_offset = srd_bytes.find(b'\x24\x52\x53\x49', offset)
    print(f'RSI offset: {rsi_offset}')
    vertex_offset = struct.unpack_from('<i', srd_bytes, rsi_offset + 32)[0] & 0x0fffffff
    print(f'Vertex Offset: {vertex_offset}')
    vertex_length = struct.unpack_from('<i', srd_bytes, rsi_offset + 36)[0]
    print(f'Vertex Length: {vertex_length}')
    vertex_data = srdi_bytes[vertex_offset:vertex_offset + vertex_length]
    #print(f'Vertex Data: {vertex_data}')
    
    #Loop over points and record X and Y coords
    offset = vertex_offset
    print(f'Difference: {vertex_offset + vertex_length}')
    x_cords = []
    y_cords = []
    for i in range(vertex_offset, 20000):
        x_cords.append(struct.unpack_from('<f', srdi_bytes, offset)[0] * -1.0)
        offset += 4
        y_cords.append(struct.unpack_from('<f', srdi_bytes, offset)[0])
        offset += 4
        struct.unpack_from('<f', srdi_bytes, offset)[0]
        offset += 4
        struct.unpack_from('<f', srdi_bytes, offset)[0] * -1.0
        offset += 4
        struct.unpack_from('<f', srdi_bytes, offset)[0]
        offset += 4
        struct.unpack_from('<f', srdi_bytes, offset)[0]
        offset += 4
        uv_x = Infinity
        uv_x = struct.unpack_from('<f', srdi_bytes, offset)[0]
        offset += 4
        while (isnan(uv_x) or not isfinite(uv_x)):
            uv_x = struct.unpack_from('f', srdi_bytes, offset)[0]
            offset += 4

        uv_y = struct.unpack_from('f', srdi_bytes, offset)[0]
        offset += 4
        while (isnan(uv_y) or not isfinite(uv_y)):
            uv_y = struct.unpack_from('f', srdi_bytes, offset)[0]
            offset += 4
        
       # if (isnan(uv_x) or isnan(uv_y) or abs(uv_x) > 1 or abs(uv_y) > 1):
            #print("invalid UVs detected")
    print(f'Offset: {offset}')
    print('---------------------------')
    
    #for cord in x_cord, print f'(x: ){x_cord[i]}, {y_cord[i]})'
    cords_string = ""
    for i in range(0, vertex_count):
        cords_string += f'({x_cords[i]}, {y_cords[i]})\n'
    path = Path('some_file.txt')
    path.write_text(cords_string)
    

    plt.scatter(x_cords, y_cords, label= "star", color= "green",
                marker= "*", s=30)

    # x-axis label
    plt.xlabel('x - axis')
    # frequency label
    plt.ylabel('y - axis')
    # plot title
    plt.title('My scatter plot!')
    # showing legend
    plt.legend()
    
    # function to show the plot
    plt.show()
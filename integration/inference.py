from pynq import allocate, Overlay
import numpy as np
import time

start_load = time.time()

overlay = Overlay("design_1_fine_tune.bit")
dma = overlay.axi_dma_0

print(f"Loading time: {(time.time() - start_load):.4f} s")
input_buffer = allocate(shape=(51,), dtype=np.float32)
output_buffer = allocate(shape=(1,), dtype=np.float32)


input_data = [
        0.3009, -0.0236, -0.0969, -0.9868, -0.9749, -0.9869, -0.9247, -0.5651,
        -0.7979,  0.8371,  0.6710,  0.8461, -0.0315, -0.2453,  0.1566, -0.9872,
        -0.9511, -0.9415, -0.8678, -0.9630, -0.6845,  0.8389,  0.8598,  0.8170,
        -0.9754, -0.9854, -0.9765, -0.9753, -0.9849, -0.9763, -0.7833,  0.6752,
        0.6708, -0.6775,  0.7303,  0.6763
]

start_time = time.time()

for i, n in enumerate(input_data):
    input_buffer[i] = n


dma.sendchannel.transfer(input_buffer)
dma.recvchannel.transfer(output_buffer)
dma.sendchannel.wait()
dma.recvchannel.wait()
print(f'Inference time: {((time.time() - start_time) * 1000):.4f} ms')
print(f'Predicted value: {int(output_buffer[0])}; ground truth value: 0')

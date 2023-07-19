from PIL import Image
import numpy as np
import heapq
import os
import time

class HuffmanNode(object):
    def __init__(self, value, freq):
        self.left = None
        self.right = None
        self.value = value
        self.freq = freq

    def __lt__(self, other):
        return self.freq < other.freq

def calc_freq(image):
    # Calculate frequency of each pixel value
    freq = np.bincount(image.ravel(), minlength=256)
    return freq

def build_huffman_tree(freq):
    # Build Huffman tree
    heap = [HuffmanNode(i, freq) for i, freq in enumerate(freq)]
    heapq.heapify(heap)
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)
    return heap[0]  # root node

def build_huffman_dict(node, binary_string='', huffman_dict={}):
    # Build Huffman dictionary from Huffman tree
    if node is None:
        return
    if node.value is not None:
        huffman_dict[node.value] = binary_string
    build_huffman_dict(node.left, binary_string + '0')
    build_huffman_dict(node.right, binary_string + '1')
    return huffman_dict

def huffman_encoding(image, huffman_dict):
    # Encode image using Huffman dictionary
    return ''.join([huffman_dict[pixel] for pixel in image.ravel()])

def compress_image(image_path):
    # Record the start time
    start_time = time.time()

    # Convert image to grayscale
    image = Image.open(image_path).convert('L')
    image = np.array(image)

    # Build Huffman tree and dictionary
    freq = calc_freq(image)
    huffman_tree = build_huffman_tree(freq)
    huffman_dict = build_huffman_dict(huffman_tree)

    # Encode image
    encoded_image = huffman_encoding(image, huffman_dict)

    # Calculate compression ratio
    original_size = os.path.getsize(image_path)
    compressed_size = len(encoded_image) / 8  # convert from bits to bytes
    compression_ratio = original_size / compressed_size

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    print(f'Original size: {original_size} bytes')
    print(f'Compressed size: {compressed_size} bytes')
    print(f'Compression ratio: {compression_ratio}')
    print(f'Time taken: {elapsed_time} seconds')
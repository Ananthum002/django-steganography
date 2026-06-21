import os
import time
from PIL import Image
from django.conf import settings

HEADER_BITS = 32  # bits reserved at the start to store the message length


def time_in_millisecond():
    return str(int(time.time() * 1000))


def _text_to_binary(message):
    data = message.encode('utf-8')
    length_bits = format(len(data), f'0{HEADER_BITS}b')
    message_bits = ''.join(format(byte, '08b') for byte in data)
    return length_bits + message_bits


def canEncode(message, img):
    """3 bits per pixel (1 in each of R, G, B's LSB)."""
    binary = _text_to_binary(message)
    pixels_needed = -(-len(binary) // 3)  # ceil division
    pixels_available = img.size[0] * img.size[1]
    return pixels_needed <= pixels_available


def createBinaryTriplePairs(message):
    binary = _text_to_binary(message)
    padding = (-len(binary)) % 3
    binary += '0' * padding
    return [binary[i:i + 3] for i in range(0, len(binary), 3)]


def embedBitsToPixels(binaryTriplePairs, pixels):
    newPixels = []
    for i, pixel in enumerate(pixels):
        if i < len(binaryTriplePairs):
            triple = binaryTriplePairs[i]
            r, g, b = pixel[0], pixel[1], pixel[2]
            r = (r & ~1) | int(triple[0])
            g = (g & ~1) | int(triple[1])
            b = (b & ~1) | int(triple[2])
            newPixels.append((r, g, b))
        else:
            newPixels.append(pixel[:3])
    return newPixels


def encodeLSB(message, imageFilename):
    print('Encoding..')

    img = Image.open(imageFilename).convert('RGB')
    size = img.size

    if not canEncode(message, img):
        return None

    binaryTriplePairs = createBinaryTriplePairs(message)
    pixels = list(img.getdata())
    newPixels = embedBitsToPixels(binaryTriplePairs, pixels)

    newImg = Image.new('RGB', size)
    newImg.putdata(newPixels)

    # Always save as PNG: JPEG's lossy compression destroys LSB data,
    # regardless of what format the cover image was uploaded as.
    finalFilename = os.path.join(
        settings.MEDIA_ROOT,
        f'stout_{time_in_millisecond()}.png'
    )
    newImg.save(finalFilename, 'PNG')
    return finalFilename


def decodeLSB(imageFilename):
    print('Decoding..')

    img = Image.open(imageFilename).convert('RGB')
    pixels = list(img.getdata())

    bits = []
    for r, g, b in pixels:
        bits.append(str(r & 1))
        bits.append(str(g & 1))
        bits.append(str(b & 1))
    bitstring = ''.join(bits)

    if len(bitstring) < HEADER_BITS:
        return None

    message_length = int(bitstring[:HEADER_BITS], 2)
    message_bits = bitstring[HEADER_BITS: HEADER_BITS + message_length * 8]

    if len(message_bits) < message_length * 8:
        return None  # image doesn't actually contain a complete message

    message_bytes = bytearray(
        int(message_bits[i:i + 8], 2) for i in range(0, len(message_bits), 8)
    )

    try:
        return message_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return None
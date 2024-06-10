import sys
from PIL import Image
import random

def swap_pixels(image, key):
    random.seed(key)
    width, height = image.size
    pixel_data = list(image.getdata())
    indices = list(range(len(pixel_data)))
    random.shuffle(indices)
    shuffled_pixel_data = [pixel_data[i] for i in indices]
    return shuffled_pixel_data, indices

def unswap_pixels(image, key, indices):
    random.seed(key)
    width, height = image.size
    pixel_data = list(image.getdata())
    unshuffled_pixel_data = [None] * len(pixel_data)
    for original_index, shuffled_index in enumerate(indices):
        unshuffled_pixel_data[shuffled_index] = pixel_data[original_index]
    return unshuffled_pixel_data

def apply_key_to_pixels(pixel_data, key, operation):
    transformed_pixel_data = []
    for pixel in pixel_data:
        if operation == "encrypt":
            transformed_pixel = tuple((p + key) % 256 for p in pixel)
        else:
            transformed_pixel = tuple((p - key) % 256 for p in pixel)
        transformed_pixel_data.append(transformed_pixel)
    return transformed_pixel_data

def transform_image(image_path, key, output_path, operation, method):
    image = Image.open(image_path)
    width, height = image.size
    if method == "swap":
        if operation == "encrypt":
            transformed_pixel_data, indices = swap_pixels(image, key)
            image.putdata(transformed_pixel_data)
            with open(output_path + ".key", 'w') as key_file:
                key_file.write(str(indices))
        else:
            with open(output_path + ".key", 'r') as key_file:
                indices = eval(key_file.read())
            transformed_pixel_data = unswap_pixels(image, key, indices)
            image.putdata(transformed_pixel_data)
    else:
        pixel_data = list(image.getdata())
        transformed_pixel_data = apply_key_to_pixels(pixel_data, key, operation)
        image.putdata(transformed_pixel_data)

    image.save(output_path)
    print(f"Image {operation}ed successfully and saved to {output_path}!")

def main():
    if len(sys.argv) != 6:
        print("Usage: python script.py <encrypt/decrypt> <input_path> <key> <output_path> <method>")
        print("Method can be 'swap' or 'math'")
        return
    
    action = sys.argv[1]
    input_path = sys.argv[2]
    key = int(sys.argv[3])
    output_path = sys.argv[4]
    method = sys.argv[5]

    if method not in ["swap", "math"]:
        print("Invalid method. Use 'swap' or 'math'.")
        return

    if action == "encrypt":
        transform_image(input_path, key, output_path, "encrypt", method)
    elif action == "decrypt":
        transform_image(input_path, key, output_path, "decrypt", method)
    else:
        print("Invalid operation. Use 'encrypt' or 'decrypt'.")

if __name__ == "__main__":
    main()

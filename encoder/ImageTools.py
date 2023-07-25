from encoder import FileEncoder, FileDecoder
from PIL import Image
from encoder import pixelColor
import os
import re
import cv2

class ImageTools():

    def CheckSize(self,number):
        factors = []
        for i in range(1, int(number ** 0.5) + 1):
            if number % i == 0:
                factors.append(i)

        max_factor = factors[-1]

        # Check if the given number is a perfect square
        if max_factor * max_factor == number:
            return max_factor, max_factor

        for factor in reversed(factors):
            complementary_factor = number // factor
            if complementary_factor != factor and number % complementary_factor == 0:
                return complementary_factor, factor

        return max_factor, 1


    def GenerateImage(self,filepath):
        encoded_string = FileEncoder.FileEncoder().EncodeFile(filepath)
        v = filepath.split("\\")[-1].split(".")[0]
        encoded_string = encoded_string.split(".")
        encoded_str = encoded_string[0]
        extension = encoded_string[-1]
        n = 1
        encoded_list = [encoded_str[i * n:(i + 1) * n] for i in range((len(encoded_str) + n - 1) // n )]

        image = Image.new("RGB", self.CheckSize(len(encoded_list)), color="white")
        width, height = image.size
        chunkindex = 0

        for x in range(width):
            for y in range(height):
                image.putpixel((x, y), pixelColor.GetRGB(encoded_list[chunkindex]))
                chunkindex = chunkindex+1

        pp = "C:/Users/PC/Desktop/ColorFile/static/output/"+v+"."+extension+".png"
        image.save(pp)

        return pp


    def DecodeImage(self, filepath):

        image = cv2.imread(filepath)
        height, width, _ = image.shape
        extension = filepath.split("\\")[-1].split(".")[-2]
        v = filepath.split("\\")[-1].split(".")[0]+"."

        full = ""

        for y in range(width):  # Swap loop order to fix width and height
            for x in range(height):
                pixel_value = image[x, y]  # Swap x and y to fix pixel_value retrieval
                rgb = tuple(pixel_value)[::-1]
                encoded = pixelColor.GetKey(rgb)

                full = full + encoded

        pp = "C:/Users/PC/Desktop/ColorFile/static/output/"+v+extension
        FileDecoder.FileDecoder().SaveFile(full+"."+extension, pp)
        return pp

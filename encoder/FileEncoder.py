import os
from encoder import EncoderDecoder

class FileEncoder():
    
    def GetFile(self):
        path = "./input/"
        file = os.listdir(path)[0]
        newpath = os.path.join(path, file)
        return newpath, file.split(".")[0]
    
    def EncodeFile(self,filepath):
        
        extension = "."+filepath.split(".")[-1]
        
        with open(filepath, 'rb') as file:
            binary_data = file.read()
            binary_string = ''.join(format(byte, '08b') for byte in binary_data)
            n = 8
            binary_list = [binary_string[i * n:(i + 1) * n] for i in range((len(binary_string) + n - 1) // n )]

            key_str = ""
            for x in binary_list:
                key = EncoderDecoder.GetKey(x)
                key_str = key_str+key
                
        return key_str+extension
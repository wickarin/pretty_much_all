#RLE: DDDD -> 4D; 1112222 -> 3 - 1, 4 - 2;
#alteracao estatistica, move-to-front
#
import numpy as np
import os

'''
RLE:
    random.txt : IN:96767 OUT:187842    RLE ratio: -94.1%
    

'''
# Perform Run–length encoding (RLE) data compression algorithm on string `str`
def encode(s):
 
    encoding = "" # stores output string
 
    i = 0
    while i < len(s):
        # count occurrences of character at index `i`
        count = 1
 
        while i + 1 < len(s) and s[i] == s[i + 1]:
            count = count + 1
            i = i + 1
 
        # append current character and its count to the result
        encoding += str(count) + s[i]
        i = i + 1
 
    return encoding
 
def readText(filename):
    alfa = "ABCDEFGHIJKLMOPQRSTUVWXYZ"
    alfa2 = alfa.lower()

    with open(filename, "r") as f:
        text = f.read()
 
    str = []
    # to ascii conversion
    for char in text:
        str.append(char)

    return np.array(str)

def ocorrencias(data: np.ndarray, alfa: np.ndarray, zeros: bool = True) -> dict:
    """
    Counts how many alphabet items are in data\n
    Args:
        data: the datastream
        alfa: The alphabet (set of symbols)
        zeros: whether the array has zeros or not

    Returns:
        the occurrences of each symbol of the alphabet in the datastream
    """
    d=data.flatten()

    #if the function is called with zeros set to true the a dictionary contaioning all the items from the alfabet is created
    if zeros:
        ocorrencias = dict.fromkeys(alfa, 0)
    else:
        ocorrencias = {}

    for element in d:
        if element not in ocorrencias:
            ocorrencias[element] = 0
        ocorrencias[element] += 1

    return ocorrencias


def probability(p: np.ndarray, a: np.ndarray, zeros: bool = False) -> np.ndarray:

    ocr=ocorrencias(p, a, zeros)
    ocr= list(ocr.values())
    ocr= np.array(ocr)
    prob = ocr / p.flatten().shape[0]   #array with prob of each symbol

    return prob

def entropia(p: np.ndarray, a: np.ndarray) -> float:
    """Calculates the entropy of an information source.\n   

    Entropy: theoretical minimum limit for the average number of bits needed to encode a symbol.

    Args:
        p: The source of information (sound, text, image, etc.)
        a: The alphabet (set of symbols)

    Returns:
        The entropy of the information source.
    """

    prob = probability(p, a, True)

    return -np.sum(prob * np.log2(prob))


def getAlpha(source):
    a = []
    for char in source:
        if char not in a and char != ' ':
            a.append(char)
            
    return a


def main():
    file2 = "dataset/random1.txt"
    stri = input("Filename: ")
    sure = readText(stri)
    size1 = os.path.getsize(stri)
    print("File char count: "+str(size1))
    sure1 = encode(sure)
    size2 = os.path.getsize(file2)
    print("Char count after compression: "+str(size2)) 
    

    
    with open(file2, "w") as f:
        f.write(sure1)
    f.close()
    sure1 = readText(file2)
    a = size1 / size2
    print("Compress ratio (bits at input / bits at output): "+str(a))
    
    sureNP = np.asarray(sure)
    sure1NP = np.asarray(sure1)
    alpha = getAlpha(sure)
    print(entropia(sureNP, getAlpha(sure)))
    print(entropia(sure1NP, getAlpha(sure1)))
    
if __name__ == '__main__':
    main()
import numpy as np
import cv2
import pylab as plt
from huffman import HuffmanCoding

#Lemepel_Ziv_Decompression_Stage

with open('Compressed_img_decompressed.txt') as f:
    #h = [int(x) for x in next(f).split()]
    array = [[int(x) for x in line.split()] for line in f]
	
#print(len(array[0]))
#print(len(array))
decompe = []
for i in range(len(array)):
    decomp = []
    #print(type(img[i]))
    darr = array[i]
    #print(len(arr))
    #print(type(arr))
    j=0
    count=0
    while j < len(darr):
        
        if darr[j] == -1:
            darr = darr[:j]+darr[j+1:]
            dist = darr[j]
            ind = count - dist
            dlength = darr[j+1]
            j=j+2
            while dlength > 0:
                dlength = dlength-1
                decomp.append(decomp[ind])
                count = count+1
                ind = ind+1
                
        else:
            decomp.append(darr[j])
            count = count +1
            j=j+1
    #comp.append(chr(arr[j]))
    #print(len(decompe))
    decompe.append(decomp)

#print(len(decompe[0]))
#print(len(decompe))
#print(decompe[20])

Out = np.array(decompe)
#print(type(Out[0][0]))
#print(len(Out))
#print(len(Out[0]))
#print(Out[0])

im = plt.imshow(Out, 'gray')
plt.title('Restored Image')
plt.show()

#print("Open CV version:", cv2.__version__)
#cv2.imshow('image',Out)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
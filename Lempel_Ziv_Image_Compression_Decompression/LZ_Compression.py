import numpy as np
import cv2
from huffman import HuffmanCoding

# Load an color image in grayscale

img = cv2.imread('earth_original.png',0)
cv2.imwrite('earthgray.png',img)
#np.savetxt('tout.txt',img)
print(type(img[0][0]))
#x = img[0].tolist()
print(len(img))
#print(chr(img[0][9]))
print(len(img[0]))

#Lempel_Ziv_Compression_Stage

compe = []
#comp=[]
#arr=[]
for i in range(len(img)):
    comp = []
    #print(type(img[i]))
    arr = img[i].tolist()
    #print(len(arr))
    #print(type(arr))
    j=0
    while j < len(img[0]):
        length =0
        add = 0
        ind=0
        #count = j +(i*len(img[0]))
        if arr[j] in arr[:j]:
            
            ind = arr.index(arr[j])
            add = j - ind
            
            length = 1
            #a = [arr[count]]+ a
            while j+1 < len(img[0]) and arr[j+1]== arr[ind+1]:
                length = length+1
                ind = ind+1
                j=j+1
                #count = count+1
                #a = [arr[count]]+ a
        if length == 1 or length ==0:
            comp.append(arr[j])
        else:
            comp.append([add,length])
            #comp.append(chr(length))
        j=j+1
    #comp.append(chr(arr[j]))
    #print(len(comp))
    compe.append(comp)

	
	
#print(len(comp))
#print(compe[0])	

thefile = open('Compressed_img.txt','w')
x=-1
for element in compe:
    for el in element:
        
        if isinstance(el , list):
            #el[0] = el[0]/float(10)
            #el[1] = el[1]/float(10)
            thefile.write("%d \t"%x)
            #thefile.write("%d"%0)
            thefile.write("%d \t"%el[0])
            #thefile.write("%d"%0)
            thefile.write("%d \t"%el[1])
            #thefile.write("%d"%0)
        else:
            #el = el/float(10)
            thefile.write("%d \t"%el)
            #thefile.write("%d"%0)
        
    thefile.write("\n")
thefile.close()


#Hauffman_Compreesion_Stage 

#input file path
path = "E:\Learning\Python\Compressed_img.txt"

h = HuffmanCoding(path)

output_path = h.compress()


#Huffman_Decompression_Stage
h.decompress(output_path)



cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

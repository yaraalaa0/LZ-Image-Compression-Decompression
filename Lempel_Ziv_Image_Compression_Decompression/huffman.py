import os
import math



class HeapNode:
	def __init__(self, char, freq):
		self.char = char
		self.freq = freq
		self.left = None
		self.right = None

	def __cmp__(self, other):
		if(other == None):
			return -1
		if(not isinstance(other, HeapNode)):
			return -1
		return self.freq > other.freq



class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}	
    def pushHeap(self, node):
        if len(self.heap) == 0:
            self.heap.append(node)
        else:
            self.heap.append(node)
            self.reheapUp(len(self.heap)-1)
    def reheapUp(self, chilLoc):
        if chilLoc != 0:
            parent= math.floor((chilLoc-1)/2)
            c= self.heap[chilLoc]
            p = self.heap[parent]
            if c.freq < p.freq:
                hold=self.heap[parent]
                self.heap[parent]=self.heap[chilLoc]
                self.heap[chilLoc]=hold
                self.reheapUp(parent)
    def popHeap(self):
        if len(self.heap)==0:
            return -1
        dataOut=self.heap[0]
        self.heap[0]= self.heap[len(self.heap)-1]
        self.heap = self.heap[:(len(self.heap)-1)]
        self.reheapDown(0)
        return dataOut
    def reheapDown(self, root):
        last=len(self.heap)-1
        if ((root*2)+1)<=last: 
#There is at least one child
            leftData= self.heap[(root*2)+1]
            if ((root*2) + 2) <= last: #right Subtree exist
                rightData = self.heap[(root*2) + 2]
#Determine which child is la
                if leftData.freq < rightData.freq:
                    smallLoc = (root*2) + 1 #if there's no right or left is smaller
                else:
                    smallLoc = (root*2) + 2 #if right exist and left is not smallerels
            else:				#right Subtree doesn't exist
                smallLoc = (root*2) + 1
#test if root <  large subtree
            r = self.heap[root]
            s = self.heap[smallLoc]
            if r.freq > s.freq:
                hold= self.heap[root]
                self.heap[root]= self.heap[smallLoc]
                self.heap[smallLoc]= hold
                self.reheapDown(smallLoc)
    def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            if not character in frequency:
                frequency[character] = 0
            frequency[character] = frequency[character]+1
        return frequency
    def make_heap(self, frequency):
        for key in frequency:
            node = HeapNode(key, frequency[key])
            self.pushHeap(node)
    def merge_nodes(self):
        while(len(self.heap)>1):
            node1 = self.popHeap()
            node2 = self.popHeap()
            merged = HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            self.pushHeap(merged)
    def make_codes_helper(self, root, current_code):
        if root == None:
            return
        if(root.char != None):
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return
        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")
    def make_codes(self):
        root = self.popHeap()
        current_code = ""
        self.make_codes_helper(root, current_code)
    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text = encoded_text + self.codes[character]
        return encoded_text
    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text = encoded_text + "0"
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text
    def get_byte_array(self, padded_encoded_text):
        if(len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b
    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"
        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()
            #print(type(text))
            text = text.rstrip()
            frequency = self.make_frequency_dict(text)
            self.make_heap(frequency)
            self.merge_nodes()
            self.make_codes()
            encoded_text = self.get_encoded_text(text)
            padded_encoded_text = self.pad_encoded_text(encoded_text)

            b = self.get_byte_array(padded_encoded_text)
            output.write(bytes(b))
        print("Compressed")
        return output_path


    """ functions for decompression: """

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:] 
        encoded_text = padded_encoded_text[:-1*extra_padding]

        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code = current_code + bit
            if(current_code in self.reverse_mapping):
                character = self.reverse_mapping[current_code]
                decoded_text = decoded_text + character
                current_code = ""

        return decoded_text


    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed" + ".txt"

        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ""

            byte = file.read(1)
            while len(byte) != 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string = bit_string + bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)

            decompressed_text = self.decode_text(encoded_text)
			
            output.write(decompressed_text)

        print("Decompressed")
        return output_path
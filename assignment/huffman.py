def text2bit_stream(text):
    return "".join([bin(ord(c))[2:].zfill(8) for c in text])


def ascii2bit_stream(text):
    """ Translates ASCII text to binary reprersentation using
        7 bits per character. Assume only ASCII chars """
    return "".join([bin(ord(c))[2:].zfill(7) for c in text])



########################################################
#### HUFFMAN CODE
########################################################

def char_count(text):
    """ Counts the number of each character in text.
        Returns a dictionary, with keys being the observed characters,
        values being the counts """
    d = {}
    for ch in text:
        if ch in d:
            d[ch] += 1
        else:
            d[ch] = 1
    return d


def build_huffman_tree(char_count_dict):
    """ Recieves dictionary with char:count entries
        Generates a LIST structure representing
        the binary Huffman encoding tree """
    queue = [(c,cnt) for (c,cnt) in char_count_dict.items()]

    while len(queue) > 1:
        #print(queue)
        # combine two smallest elements
        A, cntA = extract_min(queue)    # smallest in queue
        B, cntB = extract_min(queue)    # next smallest
        chars = [A,B]
        weight = cntA + cntB            # combined weight
        queue.append((chars, weight))   # insert combined node

    # only root node left
    #print("final queue:", queue)
    root, weight_trash = extract_min(queue) # weight_trash unused
    return root                             #a LIST representing the tree structure


##def extract_min(queue):
##    """ queue is a list of 2-tuples (x,y).
##        remove and return the tuple with minimal y """ 
##    min_pair = queue[0]
##    for pair in queue:
##        if pair[1] < min_pair[1]:
##            min_pair = pair
##
##    queue.remove(min_pair)
##    return min_pair


def extract_min(queue): #the shorter, "Pythonic" way
    """ queue is a list of 2-tuples (x,y).
        remove and return the tuple with minimal y """ 
    min_pair = min(queue, key = lambda pair: pair[1])
    queue.remove(min_pair)
    return min_pair



def generate_code(huff_tree, prefix=""):
    """ Receives a Huffman tree with embedded encoding,
        and a prefix of encodings.
        returns a dictionary where characters are
        keys and associated binary strings are values."""
    if isinstance(huff_tree, str): # a leaf
        return {huff_tree: prefix}
    else:
        lchild, rchild = huff_tree[0], huff_tree[1]
        codebook = {}

        codebook.update(generate_code(lchild, prefix+'0'))
        codebook.update(generate_code(rchild, prefix+'1'))
        #   oh, the beauty of recursion...
        return codebook

    
def compress(text, encoding_dict):
    """ compress text using encoding dictionary """
    assert isinstance(text, str)
    return "".join(encoding_dict[ch] for ch in text)


def reverse_dict(d):
    """ build the "reverse" of encoding dictionary """
    return {y:x for (x,y) in d.items()}


def decompress(bits, decoding_dict):
    prefix = ""
    result = []
    for bit in bits:
        prefix += bit
        if prefix in decoding_dict:
            result.append(decoding_dict[prefix])
            prefix = ""  #restart
    assert prefix == "" # must finish last codeword
    return "".join(result)  # converts list of chars to a string

  
  
####################################################
#### EXECUTIONS WITH VARIOUS TEXTS
####################################################

#<<<<<<<<<<<<<<<<<<<
# "real" online text
#>>>>>>>>>>>>>>>>>>>

import urllib.request

def get_html_text(path):
    text = urllib.request.urlopen(path).read()
    text = text.decode('utf -8')
    return text


def clean_non_ascii(text):
    """ Gets rid of non-ASCII characters in text"""
    return ''.join(ch for ch in text if ord(ch)<128)


def wiki_test():
    print("building huffman code from a 'real' text, Wikipedia's enrty on Huffman code...")
    wiki = get_html_text("https://en.wikipedia.org/wiki/Huffman_coding")
    wiki_clean = clean_non_ascii(wiki)
    counts =  char_count(wiki_clean)
    print(counts, end="\n\n")
    tree = build_huffman_tree(counts)
    print(tree, end="\n\n")
    code = generate_code(tree)
    print(code, end="\n\n")



#<<<<<<<<<<<<<<<<<<<
# short sample texts
#>>>>>>>>>>>>>>>>>>>

def full_cycle(corpus, text):
    #generate Huffman code from corpus
    print("corpus:\n", corpus, end="\n\n")
    counts =  char_count(corpus)
    print(counts, end="\n\n")
    tree = build_huffman_tree(counts)
    print(tree, end="\n\n")
    code = generate_code(tree)
    print(code, end="\n\n")

    #compress text using code
    print("text:\n", text, end="\n\n")
    print("text len in bits:", len(ascii2bit_stream(text)), end="\n\n")
    print(ascii2bit_stream(text), end="\n\n")
    C = compress(text, code)
    print("compressed len in bits:", len(C), end="\n\n")
    print(C, end="\n\n")
    print("compression ratio:", len(C) / len(ascii2bit_stream(text)), end="\n\n")

    #decompression, back to original code
    decode = reverse_dict(code)
    print(decode, end="\n\n")
    D = decompress(C, decode)
    print(D, end="\n\n")

    assert D == text #just making sure

##corpus = """Selected Alan Perlis Quotations:
##      (1) It is easier to write an incorrect program
##            than understand a correct one.
##      (2) One man's constant is another man's variable. """
##
##text = "fun"
##
###full_cycle(corpus, text)
###full_cycle(corpus + "f", text)   #missing char in corpus that exists in text
##asci = "".join(chr(i) for i in range(128))
##full_cycle(corpus + asci, text)  #add all ascii chars




#<<<<<<<<<<<<<<
# random texts
#>>>>>>>>>>>>>>
import random

def random_string(n):
    """ Generate a random ascii sequence of length n """
    return "".join(chr(random.randrange(128)) for i in range(n))


def rand_compression_test(n):
    print("compressing a random text of lengrh", n)
    rand_text = random_string(n)
    corpus = text = rand_text
    code = generate_code(build_huffman_tree(char_count(corpus)))
    C = compress(text, code)  #best possible corpus is text itself
    print("compression ratio:", len(C) / len(ascii2bit_stream(text)))








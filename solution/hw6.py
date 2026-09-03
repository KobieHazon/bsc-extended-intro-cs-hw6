from matrix import *
from huffman import *

############
# QUESTION 1
############

def choose_sets_gen(lst,k): 
    if k==0:
        yield []
    elif not len(lst)<k:
        g = choose_sets_gen(lst[1:],k-1) #Kept the first 4 lines as instructed
        for comb in g:
                yield [lst[0]]+comb
        for comb in choose_sets_gen(lst[1:],k):
            yield comb
    else:
        pass

def choose_sets_gen_specific(lst, k, elem):
    for comb in choose_sets_gen(lst, k):
        if elem in comb:
            yield comb


############
# QUESTION 2
############

###### CODE FROM LECTURE - DO NOT CHANGE ######
def fingerprint(text, basis=2**16, r=2**32-3):
    """ used to compute karp-rabin fingerprint of the pattern
        employs Horner method (modulo r) """
    partial_sum = 0
    for ch in text:
        partial_sum =(partial_sum*basis + ord(ch)) % r
    return partial_sum

def text_fingerprint(text, m, basis=2**16, r=2**32-3):
    """ computes karp-rabin fingerprint of the text """
    f=[]
    b_power = pow(basis, m-1, r)
    list.append(f, fingerprint(text[0:m], basis, r))
    # f[0] equals first text fingerprint 
    for s in range(1, len(text)-m+1):
        new_fingerprint = ( (f[s-1] - ord(text[s-1])*b_power)*basis
                         +ord(text[s+m-1]) ) % r
            # compute f[s], based on f[s-1]
        list.append(f,new_fingerprint)# append f[s] to existing f       
    return f
##############################################



def is_rotated_1(s, t, basis=2**16, r=2**32-3):
    if len(s) != len(t):
        return False
    basic_print = fingerprint(s, basis, r)
    comp_print = fingerprint(t, basis, r)
    for i in range(0, len(t)): #O(n)
        if comp_print == basic_print:
            return True
        comp_print = ((comp_print - ord(t[i])*(basis**(len(t)-1)))*basis
                      + ord(t[i]))%r
    return False

def is_rotated_2(s, t):
    if len(s) != len(t):
        return False
    t_finger = text_fingerprint(t + t[0], 2)
    s_finger = text_fingerprint(s + s[0], 2)
    if set(t_finger) == set(s_finger): #Order doesnt matter so it can be rotated
        return True #if every pair in original+"(first letter)" - because of rotated
    return False #is in the other string that it is rotated


############
# QUESTION 3
############

def weighted_length(C, W):
    assert len(C) == len(W)
    return sum(len(C[i])*W[i] for i in range(len(W)))

def optimal(C, W):
    assert len(C) == len(W)
    dummy_str = ""
    for i in range(len(W)):
        dummy_str += chr(int(C[i]))*W[i]
    code = generate_code(build_huffman_tree(char_count(dummy_str)))
    comp_C = []
    for i in range(len(W)):
        comp_C.append(code[chr(int(C[i]))])
    if weighted_length(C, W) == weighted_length(comp_C, W):
        return True
    return False

def corpus():
    return "aabcd"


############
# QUESTION 4
############

def lz_Qa():
    return ("abcde", 40, 40)

def lz_Qb():
    return ("wood would a wo", 114, 120)

def lz_Qc():
    return ("a d a d  a a a", 86, 84)
 

############
# QUESTION 5
############

# (1)
def upside_down(im):
    n,m = im.dim()
    im2 = Matrix(n,m)
    for i in range(n):
        for j in range(m):
            im2[i, j] = im[n-i-1, j]
    return im2

# Rest of the question

## Code from the lectures of items, local_operator - DO NOT CHANGE ##

def items(mat):
    '''flatten mat elements into a list'''
    n,m = mat.dim()
    lst = [mat[i,j] for i in range(n) for j in range(m)]
    return lst

def local_operator(A, op, k=1):
  n,m = A.dim()
  res = A.copy()  # brand new copy of A
  for i in range(k,n-k):
    for j in range(k,m-k):
      res[i,j] = op(items(A[i-k:i+k+1,j-k:j+k+1]))
  return res

## end of code from lectures


def segment(im, thrd):
    ''' Binary segmentation of image im by threshold thrd '''
    n, m = im.dim()
    im2 = Matrix(n,m)
    for i in range(n):
        for j in range(m):
            if im[i, j] >= thrd:
                im2[i, j] = 255
            else:
                im2[i, j] = 0
    return im2

def dilate(im, k=1):
    return local_operator(im, lambda lst: 255 if 255 in lst else 0, k)

def edges(im, k, thr):
    m = segment(im, thr)
    return dilate(m, k) - m


############
# QUESTION 6
############


def majority(bin_s):
    n = len(bin_s)
    cnt = bin_s.count("1")
    if cnt > n/2:
        return "1"
    elif cnt < n/2:
        return "0"
    else:
        return None


def decode(trans, m):
    string = ""
    for i in range(len(trans)//m):
        tmp = majority(trans[i*m:i*m + m])
        if tmp is None:
            return None
        string += majority(trans[i*m:i*m + m])
    return string





########
# Tester
########

def test():
    #Question 1
    g = choose_sets_gen([1,2,3,4], 2)
    try:
        test_sets = sorted([sorted(c) for c in g])
        compare_sets = sorted([sorted([1, 2]), sorted([1, 3]), sorted([1, 4]),
                                    sorted([2, 3]), sorted([2, 4]), sorted([4, 3])])
        if test_sets != compare_sets:
            print("error in choose_sets_gen()")
    except StopIteration:
        print("error in choose_sets_gen()")
    if set(next(choose_sets_gen_specific([1,2,3],3,3))) != set([1, 2, 3]) or \
        next(choose_sets_gen_specific([1,2,3],0,1), None) != None:
        print ("error in choose_sets_gen_specific()")
    
    #Question 2
    for func in [is_rotated_1, is_rotated_2]:
        if func("amirrub", "rubamir") != True or \
           func("amirrub", "gilamir") != False or \
           func("amirrub", "ubamirr") != True:
            print("error in", func.__name__)
            
    #Question 3
    if weighted_length(["0", "11", "10"], [5, 1, 3]) != 13:
        print("error in weighted_length()")
    if optimal(["0", "11", "10"], [5, 1, 3]) != True or\
       optimal(["0", "11", "10"], [3, 1, 5]) != False:
        print("error in optimal()")

    #Question 5
    m1 = Matrix(4,4,0)
    m1[0,0] = 20
    m1[1,0] = 60
    m2 = segment(m1,10)
    if m2.rows != [[255, 0, 0, 0], [255, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]:
        print("error in segment()")
    m3 = dilate(m2,1)
    if m3.rows != [[255, 0, 0, 0], [255, 255, 0, 0], [0, 255, 0, 0], [0, 0, 0, 0]]:
        print("error in dilate()")
    m4 = m3 - m2
    if edges(m1,1,10) != m4:
        print("error in edges()")

    #Question 6
    if decode("000011111111", 4) != '011':
        print("error in decode_rep()")
        
   
    


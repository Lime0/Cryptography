import random
import numpy

CONST_SBOX = numpy.array([\
[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],\
[0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],\
[0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],\
[0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],\
[0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],\
[0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],\
[0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],\
[0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],\
[0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],\
[0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],\
[0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],\
[0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],\
[0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],\
[0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],\
[0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],\
[0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]])

# Function name : slicing
# Function : slicing bit_data for xbit
# Variable[type] : bit_data[bin], x[int]
# Return[type] : result[list(bin)]

def slicing(bit_data,x):
    result = []
    if '0b' in bit_data:
        bit_data1 = bit_data[2:]
    else:
        bit_data1 = bit_data
    if len(bit_data1)%x != 0:
        bit_data1 = (x-len(bit_data1)%x)*'0'+bit_data1
    for i in range(len(bit_data1)//x):
        result.append(bit_data1[i*x:(i+1)*x])
    return result

# Function name : Mul_GF
# Function : multiplication on GF(2^8) especially about x^8+x^4+x^3+x+1
# Variable[type] : x[int], y[int], m[int]
# Return[type] : result[int]

def Mul_GF(x,y):
    result = 0
    mod = 283
    while x > 0:
        if (x & 1) != 0:
            result ^= y
        y <<= 1
        y_ = y ^ mod
        if y_ < y:
            y = y_
        x >>= 1
    return result

############### Reverse Round Function ###############

# Function name : rev_MDS
# Function : Matrix multiplication operation in(GF(2^8)) for decrypt
# Variable[type] : X[bin 32bit]
# Return[type] : result[bin 32bit]

def MDS(X):
    inv_S=[]
    result = ''
    Alp = slicing(X,8) 
    Inv = [2,3,1,1]
    for i in range(len(Alp)):
        inv_S.append(hex(Mul_GF(Inv[-i],int(Alp[0],2))^Mul_GF(Inv[1-i],int(Alp[1],2))^\
            Mul_GF(Inv[2-i],int(Alp[2],2))^Mul_GF(Inv[3-i],int(Alp[3],2))))
    for i in range(len(inv_S)):
        inv_S[i] = inv_S[i][2:]
        tmp = inv_S[i]
        if len(inv_S[i]) != 2:
            tmp = (2 - len(inv_S[i]))*'0'+inv_S[i]
        result += tmp
    return slicing(bin(int(result,16)),32)
    
# Function name : SBox
# Function : Find reverse of S box
# Variable[type] : X[hex] in 8bit
# Return[type] : result[int Decimal]

def SBox(X):
    ori0 = str(hex(int(X,2)))[2:]
    if len(ori0) < 2:
        ori = (2-len(ori0))*'0'+ori0
    else:
        ori = ori0
    result = CONST_SBOX[int(ori[0],16)][int(ori[1],16)]
    return result
    
# Function name : Round
# Function : Each Round for hash function
# Variable[type] : input[bin] in 256 bit, Wn[hex] in 32bit
# Return[type] : result[bin 256 bit]

def Round(input,Wn):
    result = ''
    Bef_R = slicing(input,32) #XABCDEFG
    T = slicing(Wn,8)
    for i in range(len(Bef_R)):
        Bef_Rn = slicing(Bef_R[i],8)
        for k in range(len(Bef_Rn)):
            tmp0 = slicing(bin(SBox(bin(int(T[0],2)^int(Bef_Rn[k],2)))),8)
            tmp1 = slicing(bin(SBox(bin(int(T[1],2)^int(Bef_Rn[k],2)))),8)
            tmp2 = slicing(bin(SBox(bin(int(T[2],2)^int(Bef_Rn[k],2)))),8)
            tmp3 = slicing(bin(SBox(bin(int(T[3],2)^int(Bef_Rn[k],2)))),8)
            T = slicing(MDS(tmp0[0]+tmp1[0]+tmp2[0]+tmp3[0]),8)
    fin_T = MDS(tmp0[0]+tmp1[0]+tmp2[0]+tmp3[0])
    A = [bin(int(Bef_R[7],2)^int(fin_T,2))]
    Aft_R = A+Bef_R[1:]
    for j in range(len(Aft_R)):
        Aft_R[j] = Aft_R[j][2:]
        tmp_ = Aft_R[j]
        if len(Aft_R[j]) != 30:
            tmp_ = (30 - len(Aft_R[j]))*'0'+Aft_R[j]
        result += tmp_
    return result

# Function name : WKey_gen
# Function : Make Key about W, random by getrandbit for round over 16
# Variable[type] : W[bin] in 512 + n*32bit
# Return[type] :WR [list(bin)]
def WKey_gen(W):
    key = slicing(W,32)
    calc = int(key[-3][1:]+key[-3][0],2)^int(key[-8][6:]+key[-8][0:6],2)^\
        int(key[-14][11:]+key[-14][0:11],2)^int(key[-16],2)
    WR = slicing(bin(calc),32)
    return WR

# Function name : main
# Function : hash function to find /
# Variable[type] : X[bin] in 768bit
# Return[type] : result[int Decimal]
def main(X,RY):
    W = slicing(X[-512:],32) #512bit[32*16]
    alt_K = W
    Alp = X[:-513] #256bit
    Alp0 = Alp
    R_count = 0
    while True:
        R_count += 1
        if R_count <= 16:
            Alp = Round(Alp,W[R_count-1])
        else:
            alt_K.append(WKey_gen(alt_K))
            Alp = Round(Alp,alt_K[R_count-1])
            tmp = slicing(Alp0,32)
            tmp1 = slicing(Alp,32)
            for i in range(len(tmp)):
                tmp2 = slicing(bin(int(tmp[i],2)^int(tmp1[i],2)),32)
                Y += tmp2 
            if int(Y,2) == int(RY,2):
                print(R_count)
                return(Y)
    
X = bin(random.getrandbits(768))
RY = bin(random.getrandbits(256))
print(main(X,RY))
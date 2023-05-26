import numpy as np
import cv2

def binaryToGray(img):
    return img ^ (img >> 1)

def dmdmeshgrid():
    
    xVals = list(range(608))
    yVals = list(range(684))
    v, u = np.meshgrid(yVals, xVals, sparse=False, indexing='ij')
    x = np.zeros((684,608));
    y = v;
    x[list(np.arange(0,684,2)),:] = 2* u[list(np.arange(0,684,2)),:]
    x[list(np.arange(1,684,2)),:] = 2* u[list(np.arange(0,684,2)),:] + 1
    return (y,x)

def set_bit(v, index, x):
    """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
    mask = (1 << index) * np.ones(v.shape).astype("uint16")  # Compute mask, an integer with just bit 'index' set.
    
    
    v = v & (~mask)          # Clear the bit indicated by the mask (if x is False)
    
    v[x > 0] = v[x > 0] | mask[x > 0]         # If x was True, set the bit indicated by the mask.
    return v

def grayToBinary(img):
    numBits = 16;
    shift = 1;
    
    while shift < numBits:
        img = img ^ (img >> shift);
        
        shift = 2*shift;
    return img

def graycode(folderName, baseName, verbose=False):
    (x,y) = dmdmeshgrid()
    x = x.astype("uint16")
    y = y.astype("uint16")
    
    x = binaryToGray(x)
    y = binaryToGray(y)
    
    readImage = cv2.imread("%s/%sPositive%02d.png" % (folderName, baseName, 1),0)
    print("%s/%sPositive%02d.png" % (folderName, baseName, 1))
    print(readImage.shape)
    readImage = readImage[:,0:324]
    u = np.zeros(readImage.shape).astype("uint16")
    v = np.zeros(readImage.shape).astype("uint16")
    
    counter = 1
    for bit in range(11,0,-1):
        if verbose:
            print(bit)
        
        for k in range(0,2):
            pos = cv2.imread("%s/%sPositive%02d.png" % (folderName, baseName, counter),0)
            pos = pos[:, 0:324]
            neg = cv2.imread("%s/%sNegative%02d.png" % (folderName, baseName, counter),0)
            neg = neg[:, 0:324]
            if verbose:
                print("Max value: %d, %d\n" % (max(pos.flatten()),max(neg.flatten())))
            
            '''cv2.imshow('img',  neg - pos)
        
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            u = set_bit(u,bit,pos >= neg)'''
            # set the current bit in u/v to 1 if pos >= neg there, otherwise 0
            
            try:
                if (k) :
                #u = u + 2 ** (bit - 1) * (pos >= neg)
                
                    u = set_bit(u,bit-1,pos >= neg)
                    #print("set")
                else:
            #v = v + 2 ** (bit - 1) * (pos >= neg)
                    v = set_bit(v,bit-1,pos >= neg)
                    #print("not set")
        
            except:
                print("tried")
                pass
            counter = counter + 1;

    u = grayToBinary(u)
    v = grayToBinary(v)

    return(u,v)



#Basics of numpy
import numpy as np
a = np.arange(15).reshape(3,5)
shape = a.shape
size = a.size
itemsize = a.itemsize
ndim = a.ndim
dtype = a.dtype
np.savetxt('demo_numpy.txt',(a,shape,size,itemsize,ndim,dtype),newline='\r\n',fmt='%s')

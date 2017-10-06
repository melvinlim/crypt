import random
class Cipher(object):
	def __init__(self,bits=16):
		self.bits=bits
		self.init_sbox()
	def init_sbox(self):
		halfsz=2**(self.bits/2)
		fullsz=2**self.bits
		self.sbt=[1]*fullsz
		self.isbt=[1]*fullsz
		tab=random.sample(range(fullsz),fullsz)
		for x in range(fullsz):
			y=tab[x]
			self.sbt[x]=y
			self.isbt[y]=x
	def sbox(self,x):
		return self.sbt[x]
	def isbox(self,x):
		return self.isbt[x]
	def shl(self,x,r,n):
		r=r%n
		umask=((2**r)-1)<<(n-r)
		lmask=((2**(n-r))-1)
		upper=(x&umask)>>(n-r)
		lower=x&lmask
#		print('upper %x,lower %x'%(upper,lower))
		return upper+(lower<<r)
	def shr(self,x,r,n):
		r=r%n
		lmask=((2**(r))-1)
		lower=x&lmask
		return (x>>r)+(lower<<(n-r))
	def test(self):
		self.testShifts()
		result=0.0
		n=len(self.sbt)
		assert(self.isbt[self.sbt[0]]==0)
		for i in range(1,n):
			assert(self.isbt[self.sbt[i]]==i)
			differingBits=self.sbt[i]^self.sbt[i-1]
			x=bin(differingBits).count('1')
			result+=x
		result/=(n*1.0)
		print result
	def testShifts(self):
		x=0xff
		for i in range(65):
			a=self.shr(x,i,32)
			b=self.shl(x,i,32)
			print '%x %x'%(a,b)
			assert(self.shl(self.shr(x,i,32),i,32)==x)
ciph=Cipher(bits=16)
ciph.test()

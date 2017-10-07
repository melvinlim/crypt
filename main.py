import random
class Sbox(object):
	def __init__(self,bits=16):
		self.bits=bits
		halfsz=2**(self.bits/2)
		fullsz=2**self.bits
		self.sbt=[1]*fullsz
		self.isbt=[1]*fullsz
		tab=random.sample(range(fullsz),fullsz)
		for x in range(fullsz):
			y=tab[x]
			self.sbt[x]=y
			self.isbt[y]=x
	def test(self):
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
class Cipher(object):
	def __init__(self,bits=16):
		self.bits=bits
		self.sbc=Sbox(bits=bits)
	def sbox(self,x):
		return self.sbc.sbt[x]
	def isbox(self,x):
		return self.sbc.isbt[x]
	def p1(self,x):	#shiftrows
		linelen=int(self.bits**0.5)
		lines=self.getLines(x)
		assert(self.getNumber(lines)==x)
		l=[]
		for i in range(len(lines)):
			tmp=self.shr(lines[i],i,linelen)
			l.append(tmp)
		return self.getNumber(l)
	def ip1(self,x):
		linelen=int(self.bits**0.5)
		lines=self.getLines(x)
		l=[]
		for i in range(len(lines)):
			tmp=self.shl(lines[i],i,linelen)
			l.append(tmp)
		return self.getNumber(l)
	def getLines(self,x):
		linelen=int(self.bits**0.5)
		lines=[]
		mask=((2**linelen)-1)
		for i in range(linelen):
			a=(x&mask)>>(i*linelen)
			lines.append(a)
			mask=mask<<(linelen)
		return lines
	def getNumber(self,lines):
		linelen=int(self.bits**0.5)
		x=0
		for i in range(linelen):
			x+=lines[i]<<(i*linelen)
		return x
	def pbox(self,x):
		return 0
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
		self.testSbox()
	def testSbox(self):
		self.sbc.test()
	def testShifts(self):
		x=0xff
		for i in range(65):
			a=self.shr(x,i,32)
			b=self.shl(x,i,32)
			print '%x %x'%(a,b)
			assert(self.shl(self.shr(x,i,32),i,32)==x)
ciph=Cipher(bits=16)
ciph.test()
x=ciph.p1(1234)
print x
print ciph.ip1(x)

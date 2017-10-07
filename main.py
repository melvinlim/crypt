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
	def __init__(self,bits=256):
		self.bits=bits
		self.sboxSz=16
		self.nSbox=bits/self.sboxSz
		self.sbc=[]
		for i in range(self.nSbox):
			self.sbc.append(Sbox(bits=self.sboxSz))
	def dec(self,x,key):
		inp=self.getLines(x,self.sboxSz)
		out=[]
		for i in range(self.nSbox):
			out.append(self.isbox(inp[i],i))
		x=self.getNumber(out,self.sboxSz)
		result=x^self.keys[0]
		return result
	def keyGen(self,k,kSz,n):
		return self.split(k,kSz,n)
	def enc(self,x,key):
		self.keySz=self.sboxSz
		self.nKeys=4
		self.keys=self.keyGen(key,self.keySz,self.nKeys)
		print self.keys
		x=x^self.keys[0]
		inp=self.getLines(x,self.sboxSz)
		out=[]
		for i in range(self.nSbox):
			out.append(self.sbox(inp[i],i))
		result=self.getNumber(out,self.sboxSz)
		return result
	def sbox(self,x,i):
		return self.sbc[i].sbt[x]
	def isbox(self,x,i):
		return self.sbc[i].isbt[x]
	def p1(self,x):	#shiftrows
		linelen=int(self.bits**0.5)
		lines=self.getLines(x,linelen)
		assert(self.getNumber(lines,linelen)==x)
		l=[]
		for i in range(len(lines)):
			tmp=self.shr(lines[i],i,linelen)
			l.append(tmp)
		return self.getNumber(l,linelen)
	def ip1(self,x):
		linelen=int(self.bits**0.5)
		lines=self.getLines(x,linelen)
		l=[]
		for i in range(len(lines)):
			tmp=self.shl(lines[i],i,linelen)
			l.append(tmp)
		return self.getNumber(l,linelen)
	def split(self,x,sz,n):
		lines=[]
		mask=((2**sz)-1)
		for i in range(n):
			a=(x&mask)>>(i*sz)
			lines.append(a)
			mask=mask<<(sz)
		return lines
	def merge(self,lines,sz,n):
		x=0
		for i in range(n):
			x+=lines[i]<<(i*sz)
		return x
	def getLines(self,x,n):
		return self.split(x,n,n)
	def getNumber(self,x,n):
		return self.merge(x,n,n)
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
		for i in range(self.nSbox):
			print i
			self.sbc[i].test()
	def testShifts(self):
		x=0xff
		for i in range(65):
			a=self.shr(x,i,32)
			b=self.shl(x,i,32)
			print '%x %x'%(a,b)
			assert(self.shl(self.shr(x,i,32),i,32)==x)
ciph=Cipher()
ciph.test()
x=ciph.p1(1234)
print x
print ciph.ip1(x)
tx=1234892
key=2314234842391984
print tx
ct=ciph.enc(tx,key)
tx=ciph.dec(ct,key)
print tx

import random
class Cipher(object):
	def __init__(self,bits=16):
		self.bits=16
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
	def sbox(self,n):
		return self.sbt[n]
	def isbox(self,n):
		return self.isbt[n]
	def test(self):
		result=0.0
		n=len(self.sbt)
		for i in range(1,n):
			assert(self.isbt[self.sbt[i]]==i)
			differingBits=self.sbt[i]^self.sbt[i-1]
			x=bin(differingBits).count('1')
			result+=x
		result/=(n*1.0)
		print result
ciph=Cipher()

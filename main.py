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
ciph=Cipher()

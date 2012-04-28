class Tail():
	def __init__(self,expr,env,k):
		self.expr = expr
		self.env = env
		self.k = k
	
	def __iter__(self):
		yield self.expr
		yield self.env
		yield self.k

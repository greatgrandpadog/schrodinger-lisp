#### seval.py

from stypes import Tail
from sparser import to_string, Symbol, isa

### binding environments

class Env(dict):
	"An environment: a dict of {'var':val} pairs, with an outer Env."
	def __init__(self, bindings={}, outer=None):
		self.update(bindings)
		self.outer = outer

	def __getitem__(self, var):
		return super(Env,self.find(var)).__getitem__(var)

	def find(self, var):
		"Find the innermost Env where var appears."
		if var in self:
			return self
		elif not self.outer is None:
			return self.outer.find(var)
		else: raise ValueError("%s is not defined"%(var,))

#### eval
depth = 0

def eval(x, env):
	"Trampoline for the actual eval implementation"
	NextCall = Tail(x,env,lambda x:x)
	while isa(NextCall, Tail):
		NextCall = eval_t(*NextCall)
	return NextCall

def eval_t(x, env, k):
	"Evaluate an expression in an environment."
	val = None
	while True:
		if isa(x, Symbol):		  # variable reference
			val = k(env[x])
		elif isa(x, list):		  # (proc exp*)
			def try_call(proc):
				if hasattr(proc, '__call__'):
					return proc(k,env,*x[1:])
				raise ValueError("%s = %s is not a procedure" % (to_string(x[0]),to_string(proc)))
			return Tail(x[0], env, try_call)
		else:
			val = k(x)
		if not isa(val, Tail):
			return val
		(x,env,k) = val

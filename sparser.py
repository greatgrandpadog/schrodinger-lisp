import string

Symbol = str
isa = isinstance

def tokenize(s):
	"Convert a string into a list of tokens."
	i = 0
	end = len(s)
	delimiters = "();'"
	sym_illegal = string.whitespace+delimiters
	tokens = []
	while i < end:
		if i+1 < end and s[i:i+2] == "::":
			token = "::"
			i += 2
		elif s[i] in string.whitespace:
			i += 1
			continue
		elif s[i] in delimiters:
			token = s[i]
			i += 1
		else:
			n = i+1
			while n != end and not s[n] in sym_illegal:
				if n+1 < end and s[n:n+2] == "::":
					break
				n += 1
			token = s[i:n]
			i = n
		tokens.append(token)
	return tokens

def parse(tokens):
	"Read an expression from a sequence of tokens."
	if len(tokens) == 0:
		raise SyntaxError('unexpected EOF while reading')
	token = tokens.pop(0)
	if '(' == token:
		L = []
		while tokens[0] != ')':
			L.append(parse(tokens))
		tokens.pop(0) # pop off ')'
		return L
	elif ";" == token: #ignore the next full expression
		parse(tokens)
		return parse(tokens) if len(tokens) > 0 else None
	elif "'" == token: #wrap the next expression in a quote
		return [Symbol('quote'),parse(tokens)]
	elif ')' == token:
		raise SyntaxError('unexpected )')
	elif tokens[0] == "::": #lookahead, desugar namespace into eval call
		tokens.pop(0)
		return [Symbol('eval'),atom(token),parse(tokens)]
	else:
		return atom(token)

def atom(token):
	"Numbers become numbers; every other token is a symbol."
	try: return int(token)
	except ValueError:
		try: return float(token)
		except ValueError:
			return Symbol(token) 

def to_string(exp):
	"Convert a Python object back into a Lisp-readable string."
	return '('+' '.join(map(to_string, exp))+')' if isa(exp, list) else str(exp)

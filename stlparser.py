'''
Alexandre Devert

A recursive descent parser for STL files
'''

import re
import numpy

__all__ = ['load', 'ParseError']



class ParseError(Exception):
	def __init__(self, line, value):
		super(ParseError, self).__init__('line %d, %s' % (line, value))
		self.line = line
		self.value = value



def enumerate_char_from_file(in_file, buffer_size = 4096):
	while True:
		chunk = in_file.read(buffer_size)
		for c in chunk:
			yield c

		if len(chunk) < buffer_size:
			return



def tokenize(in_file):
	line_id = 1
	token = None
	for c in enumerate_char_from_file(in_file):
		if c == '\n':
			line_id += 1

		if c.isspace():
			if token is not None:
				yield line_id, ''.join(token)
				token = None
		else:
			if token is None:
				token = [c]
			else:
				token.append(c)

	if token is not None:
		yield line_id, ''.join(token)



keyword_set = frozenset(['solid', 'facet', 'normal', 'outer', 'loop', 'vertex', 'endloop', 'endfacet', 'endsolid'])



def enumerate_lexeme(in_file):
	float_point_re = re.compile(r'[-+]?[0-9]*\.?[0-9]+(\e[-+]?[0-9]+)?')

	for line_id, token in tokenize(in_file):
		float_point_match = float_point_re.match(token)
		if token in keyword_set:
			yield line_id, token, token
		elif float_point_match and len(float_point_match.group(0)) == len(token):
			yield line_id, token, float(token)
		else:
			yield line_id, token, token



class Parser(object):
	def __init__(self, lexer):
		self.lexer = lexer
		self.symbol = None
		self.line_id = None

	def next(self):
		line_id, token, value = self.lexer.next()
		self.line_id = line_id
		self.lookahead = (token, value)

	def accept(self, symbol = None):
		if symbol in keyword_set:
			return self.lookahead[0] == symbol
		elif symbol is str:
			return True
		elif symbol is float:
			return isinstance(self.lookahead[1], float)

		return True

	def consume(self, symbol = None):
		if not self.accept(symbol):
			raise ParseError(self.line_id, 'unexpected symbol "%s", excepted "%s"' % (self.lookahead[0], symbol))

	def parse_vector(self):
		ret = numpy.zeros(3)
		for i in range(3):
			self.next()
			self.consume(float)
			ret[i] = self.lookahead[1]
		return ret

	def parse_triangle(self):
		self.consume('outer')
		self.next()
		self.consume('loop')
		self.next()

		vertex_list = numpy.zeros((3, 3))
		for i in range(3):
			vertex_list[i] = self.parse_vertex()
			self.next()
		self.consume('endloop')

		return vertex_list

	def parse_vertex(self):
		self.consume('vertex')
		return self.parse_vector()

	def parse_normal(self):
		self.consume('normal')
		return self.parse_vector()

	def parse_facet(self):
		self.consume('facet')

		self.next()
		if self.accept('normal'):
			normal = self.parse_normal()
			self.next()
			vertex_list = self.parse_triangle()
		elif self.accept('outer'):
			vertex_list = self.parse_triangle()
			normal = self.parse_normal()

		self.next()
		self.consume('endfacet')

		return vertex_list, normal

	def parse_facet_list(self):
		while True:
			if self.accept('facet'):
				yield self.parse_facet()
				try:
					self.next()
				except StopIteration:
					raise ParseError(self.line_id, 'unexpected end of file, excepted "endsolid"')
			else:
				self.accept('endsolid')
				return

	def parse_mesh(self):
		self.next()
		self.consume('solid')

		self.next()
		if self.accept('facet'):
			name = None
		else:
			name = self.lookahead[1]
			self.next()

		for vertex_list, normal in self.parse_facet_list():
			yield vertex_list, normal

		self.consume('endsolid')
		if name is not None:
			self.consume()



def load(in_file):
	parser = Parser(enumerate_lexeme(in_file))
	for vertex_list, normal in parser.parse_mesh():
		yield vertex_list, normal


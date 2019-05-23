class Sudoku(object):
	def __init__(self):
		self.rows = 'ABCDEFGHI'
		self.cols = '123456789'
		self.board = self.cross()

	def cross(self, rows=None, cols=None):
		rows = rows or self.rows
		cols = cols or self.cols
		return [r + c for r in rows for c in cols]



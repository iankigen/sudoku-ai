class Sudoku(object):
	def __init__(self):
		self.rows = 'ABCDEFGHI'
		self.cols = '123456789'
		self.board = self.cross()
		self.unit_list = self.row_units() + self.col_units() + self.square_units()

	def cross(self, rows=None, cols=None):
		rows = rows or self.rows
		cols = cols or self.cols
		return [r + c for r in rows for c in cols]

	def row_units(self, position=-1):
		all_row_units = [self.cross(r, self.cols) for r in self.rows]
		return all_row_units[position] if 0 <= position < 9 else all_row_units

	def col_units(self, position=-1):
		all_col_units = [self.cross(c, self.rows) for c in self.cols]
		return all_col_units[position] if 0 <= position < 9 else all_col_units

	def square_units(self, position=-1):
		all_square_units = [self.cross(rows, cols) for rows in ('ABC', 'DEF', 'GHI') for cols in ('123', '456', '789')]
		return all_square_units[position] if 0 <= position < 9 else all_square_units



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

	def grid_values(self, values):
		"""Convert grid string into {<box>: <value>} dict with '.' value for empties."""
		assert len(values) == 9 * 9, 'Input grid must be of size 9x9'
		return dict(zip(self.board, values))

	def display_board(self, values):
		"""
		Display the values as a 2-D grid.
		"""
		width = 1 + max(len(values[s]) for s in self.board)
		line = '+'.join(['-' * (width * 3)] * 3)
		for row in self.rows:
			print(''.join(values[row + col].center(width) + ('|' if col in '36' else '') for col in self.cols))

			if row in 'CF':
				print(line)
		return

	def __str__(self):
		return "{}".format(self.board)


sudoku = Sudoku()
unsolved = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."

sudoku.display_board(sudoku.grid_values(unsolved))

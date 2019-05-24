class Sudoku(object):
	def __init__(self):
		self.rows = 'ABCDEFGHI'
		self.digits = '123456789'
		self.cols = self.digits
		self.board = self.cross()
		self.unit_list = self.row_units() + self.col_units() + self.square_units()
		self.units = dict((s, [u for u in self.unit_list if s in u]) for s in self.board)
		self.peers = dict((s, set(sum(self.units[s], [])) - {s}) for s in self.board)

	def cross(self, rows=None, cols=None):
		rows = rows or self.rows
		cols = cols or self.cols
		return [r + c for r in rows for c in cols]

	def row_units(self, position=-1):
		all_row_units = [self.cross(r, self.cols) for r in self.rows]
		return all_row_units[position] if 0 <= position < 9 else all_row_units

	def col_units(self, position=-1):
		all_col_units = [self.cross(self.rows, c) for c in self.cols]
		return all_col_units[position] if 0 <= position < 9 else all_col_units

	def square_units(self, position=-1):
		all_square_units = [self.cross(rows, cols) for rows in ('ABC', 'DEF', 'GHI') for cols in ('123', '456', '789')]
		return all_square_units[position] if 0 <= position < 9 else all_square_units

	def grid_values(self, values):
		"""Convert grid string into {<box>: <value>} dict with '.' value for empties."""
		all_digits = '123456789'
		assert len(values) == 9 * 9, 'Input grid must be of size 9x9'
		return {box: all_digits if value == '.' else value for box, value in zip(self.board, values)}

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

	def eliminate(self, values):
		solved_boxes = [box for box in values.keys() if len(values.get(box)) == 1]
		for box in solved_boxes:
			digit = values[box]
			for peer in self.peers[box]:
				values[peer] = values[peer].replace(digit, '')
		return values

	def only_choice(self, values):
		"""Finalize all values that are the only choice for a unit.
		Go through all the units, and whenever there is a unit with a value
		that only fits in one box, assign the value to this box."""
		for unit in self.unit_list:
			for digit in self.digits:
				dplaces = [box for box in unit if digit in values[box]]
				if len(dplaces) == 1:
					values[dplaces[0]] = digit
		return values

	def __str__(self):
		return "{}".format(self.board)


sudoku = Sudoku()
unsolved = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."

print('BEFORE ELIMINATION')
sudoku.display_board(sudoku.grid_values(unsolved))

print('AFTER ELIMINATION')
sudoku.display_board(sudoku.eliminate(sudoku.grid_values(unsolved)))

sudoku.display_board(sudoku.only_choice(sudoku.eliminate(sudoku.grid_values(unsolved))))

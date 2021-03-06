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

	def reduce_puzzle(self, values):
		"""
		Constraint propagation

		Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
		If the sudoku is solved, return the sudoku.
		If after an iteration of both functions, the sudoku remains the same, return the sudoku.
		"""
		stalled = False

		while not stalled:
			solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
			values = self.eliminate(values)
			values = self.only_choice(values)
			solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
			stalled = solved_values_after == solved_values_before

			# Sanity check. Return false if there's a box with zero available values
			if len([box for box in values.keys() if len(values[box]) == 0]):
				return False
		return values

	def search(self, values):
		"""Using depth-first search and propagation, create a search tree and solve the sudoku."""
		values = self.reduce_puzzle(values)
		if values is False:
			return False  # No solution
		if all(len(values[s]) == 1 for s in values):
			return values  # Solved
		length, box = min((len(values[box]), box) for box in values if len(values[box]) > 1)

		for value in values[box]:
			new_sudoku = values.copy()
			new_sudoku[box] = value
			attempt = self.search(new_sudoku)
			if attempt:
				return attempt

	def __str__(self):
		return "{}".format(self.board)


sudoku = Sudoku()
unsolved = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."

print('BEFORE ELIMINATION')
sudoku.display_board(sudoku.grid_values(unsolved))

print('AFTER ELIMINATION')
sudoku.display_board(sudoku.eliminate(sudoku.grid_values(unsolved)))

print('AFTER APPLYING ONLY CHOICE')
sudoku.display_board(sudoku.only_choice(sudoku.eliminate(sudoku.grid_values(unsolved))))

print('AFTER APPLYING CONSTRAINT PROPAGATION')
sudoku.display_board(sudoku.only_choice(sudoku.reduce_puzzle(sudoku.eliminate(sudoku.grid_values(unsolved)))))

print('=' * 20)
print('TESTING ON UNSOLVED HARDER SUDOKU')
print('=' * 20)
print('BEFORE ELIMINATION')

unsolved_harder_sudoku = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

sudoku.display_board(sudoku.grid_values(unsolved_harder_sudoku))

print('AFTER ELIMINATION')
sudoku.display_board(sudoku.eliminate(sudoku.grid_values(unsolved_harder_sudoku)))

print('AFTER APPLYING ONLY CHOICE')
sudoku.display_board(sudoku.only_choice(sudoku.eliminate(sudoku.grid_values(unsolved_harder_sudoku))))

print('AFTER APPLYING CONSTRAINT PROPAGATION')
"""
The algorithm didn't solve it. It seemed to reduce every box to a number of possibilites, but it won't go farther
than that. 
"""

sudoku.display_board(
	sudoku.only_choice(sudoku.reduce_puzzle(sudoku.eliminate(sudoku.grid_values(unsolved_harder_sudoku)))))

print('AFTER APPLYING DEPTH FIRST SEARCH')
sudoku.display_board(sudoku.search(
	sudoku.only_choice(sudoku.reduce_puzzle(sudoku.eliminate(sudoku.grid_values(unsolved_harder_sudoku))))))

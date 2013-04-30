# Do not import any modules. If you do, the tester may reject your submission.

# Constants for the contents of the maze.

# The visual representation of a wall.
WALL = '#'

# The visual representation of a hallway.
HALL = '.'

# The visual representation of a brussels sprout.
SPROUT = '@'

# Constants for the directions. Use these to make Rats move.

# The left direction.
LEFT = -1

# The right direction.
RIGHT = 1

# No change in direction.
NO_CHANGE = 0

# The up direction.
UP = -1

# The down direction.
DOWN = 1

# The letters for rat_1 and rat_2 in the maze.
RAT_1_CHAR = 'J'
RAT_2_CHAR = 'P'


class Rat:
    """ A rat caught in a maze. """
    def __init__(self, symbol, row, col):
        ''' (Rat, str, int, int) -> None
        >>> rat = Rat('P', 1, 4)
        '''
        self.symbol = symbol
        self.row = row
        self.col = col
        self.num_sprouts_eaten = 0

    def set_location(self, row, col):
        ''' (Rat, int, int) -> None'''
        self.row = row
        self.col = col

    def eat_sprout(self):
        ''' (Rat) -> None'''
        self.num_sprouts_eaten += 1

    def __str__(self):
        ''' (Rat) -> str
        >>> rat = Rat('J', 4, 3)
        >>> rat.eat_sprout()
        >>> rat.eat_sprout()
        >>> str(rat)
        'J at (4, 3) ate 2 sprouts.'
        '''
        return '{0} at ({1}, {2}) ate {3} sprouts.'.format(self.symbol,
                                                           self.row, self.col,
                                                           self.num_sprouts_eaten)


class Maze:
    """ A 2D maze. """

    def __init__(self, maze, rat_1, rat_2):
        ''' (Maze, list of list of str, Rat, Rat) -> None
        >>> maz = Maze([['#', '#', '#', '#', '#', '#', '#'],
        ...             ['#', '.', '.', '.', '.', '.', '#'],
        ...             ['#', '.', '#', '#', '#', '.', '#'],
        ...             ['#', '.', '.', '@', '#', '.', '#'],
        ...             ['#', '@', '#', '.', '@', '.', '#'],
        ...             ['#', '#', '#', '#', '#', '#', '#']],
        ...            Rat('J', 1, 1), Rat('P', 1, 4))
        '''
        # check the rat symbols don't appear in the maze
        num_sprouts_left = 0
        for row in maze:
            for char in row:
                assert char != rat_1.symbol
                assert char != rat_2.symbol
                if char == SPROUT:
                    num_sprouts_left += 1

        self.maze = maze
        self.rat_1 = rat_1
        self.rat_2 = rat_2
        self.num_sprouts_left = num_sprouts_left

    def is_wall(self, row, col):
        ''' (Maze, int, int) -> bool
        >>> maz = Maze([['#', '#', '#', '#', '#', '#', '#'],
        ...             ['#', '.', '.', '.', '.', '.', '#']],
        ...            Rat('J', 1, 1), Rat('P', 1, 3))
        >>> maz.is_wall(0, 0)
        True
        '''
        if self.maze[row][col] == WALL:
            return True
        return False

    def get_character(self, row, col):
        ''' (Maze, int, int) -> str
        >>> maz = Maze([['#', '#', '#', '#', '#', '#', '#'],
        ...             ['#', '.', '.', '.', '.', '.', '#']],
        ...            Rat('J', 1, 1), Rat('P', 1, 3))
        >>> maz.get_character(0, 0)
        '#'
        >>> maz.get_character(1, 1)
        'J'
        '''
        def is_rat(rat, row, col):
            if rat.row == row and rat.col == col:
                return True
            return False

        if is_rat(self.rat_1, row, col):
            return self.rat_1.symbol

        if is_rat(self.rat_2, row, col):
            return self.rat_2.symbol
        return self.maze[row][col]

    def move(self, rat, row_dire, col_dire):
        ''' (Maze, Rat, int, int) -> bool
        >>> rat_1, rat_2 = Rat('J', 1, 1), Rat('P', 1, 3)
        >>> maz = Maze([['#', '#', '#', '#', '#', '#', '#'],
        ...             ['#', '.', '.', '.', '.', '.', '#']],
        ...            rat_1, rat_2)
        >>> maz.move(rat_1, -1, 0)
        False
        >>> maz.move(rat_2, 0, 1)
        True
        '''
        # check whether the new location is a wall
        row = rat.row + row_dire
        col = rat.col + col_dire
        if self.is_wall(row, col):
            return False

        if self.get_character(row, col) == SPROUT:
            rat.eat_sprout()
            self.num_sprouts_left -= 1

        self.maze[rat.row][rat.col] = HALL
        rat.set_location(row, col)
        self.maze[row][col] = rat.symbol
        return True

    def __str__(self):
        ''' (Maze) -> str
        >>> maz = Maze([['#', '#', '#', '#', '#', '#', '#'],
        ...             ['#', '.', '.', '.', '.', '.', '#']],
        ...            Rat('J', 1, 1), Rat('P', 1, 3))
        >>> print maz
        #######
        #J.P..#
        J at (1, 1) ate 0 sprouts.
        P at (1, 3) ate 0 sprouts.
        '''
        string = ''
        for row, line in enumerate(self.maze):
            for col, char in enumerate(line):
                string += self.get_character(row, col)
            string += '\n'
        string += str(self.rat_1) + '\n'
        string += str(self.rat_2)
        return string

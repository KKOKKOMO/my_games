import random
from cell import Cell
import utils
import numpy as np
import enum


class GameState(enum.Enum):
    NOT_RUNNING = 0
    RUNNING = 1
    DEFEAT = 2
    WIN = 3


class Field:
    def __init__(self, row_count, column_count, mines_count, field=None):
        self.row_count = row_count
        self.column_count = column_count
        self.mines_count = mines_count
        self.available_flags_count = self.mines_count
        # closure - замыкание
        def create_row_cells(value):
            return [Cell(value) for _ in range(self.column_count)]
        
        if field is not None:
            self.field = field
        else:
            self.field = np.array([create_row_cells(value=0) for _ in range(self.row_count)])
            
        self.state = GameState.NOT_RUNNING
        
    def run(self):
        self.state = GameState.RUNNING
        
    def put_mines(self):
        mines_counter = 0
        while mines_counter < self.mines_count:        
            rand_row_index = random.randint(0, self.row_count - 1)
            rand_column_index = random.randint(0, self.column_count - 1)
            rand_cell = self.field[rand_row_index][rand_column_index]
            if rand_cell.get_value() != 9:
                rand_cell.set_value(9)
                mines_counter += 1
            
    def fill_numbers(self):
        for i in range(self.row_count):
            for j in range(self.column_count):
                if self.field[i][j].get_value() == 9:
                    continue
                mines_count_around = self.calculate_mines_around(i, j)
                self.field[i][j].set_value(mines_count_around)

    def get_field(self, hidden=True):
        returning_field = []
        def get_state(cell):
            if not hidden:
                return str(cell.get_value())
            else:
                if cell.is_opened():
                    return str(cell.get_value())
                elif cell.is_flagged():
                    return 'F'
                else:
                    return '*'
                
        for i in range(self.row_count):
            prepared_row = list(map(lambda cell: get_state(cell), self.field[i]))
            returning_field.append(prepared_row)
           
        return returning_field
        #['1', '3', '0', 'B', 'F']
        
    def open_cell(self, row_index, col_index):
        current_cell = self.field[row_index][col_index]
        current_value = current_cell.get_value()
        if current_cell.is_opened():
            return
        if current_cell.is_flagged():
            self.available_flags_count += 1
        current_cell.open()
        if current_value == 9:
            self.set_state(GameState.DEFEAT)
            return
        elif current_value != 0:
            return
        
        cells_range = utils.get_cells_range(row_index, col_index, self.row_count, self.column_count)  
        start_row, end_row = cells_range['start_row'], cells_range['end_row']
        start_column, end_column = cells_range['start_column'], cells_range['end_column']        
        for i in range(start_row, end_row + 1):
            for j in range(start_column, end_column + 1):
                cell = self.field[i][j]
                if not cell.is_opened():
                    self.open_cell(i, j) 

    def set_flag(self, i, j):
        cell = self.field[i][j]
        if not cell.is_opened():     
            cell_has_flag = self.field[i][j].is_flagged()
            self.field[i][j].set_flag(not cell_has_flag)
            cell_has_flag = not cell_has_flag
            if cell_has_flag:
                self.available_flags_count -= 1
            else:
                self.available_flags_count += 1 
                            
            if self.is_win():
                self.set_state(GameState.WIN)
             
    def calculate_mines_around(self, row_index, col_index):
        cells_range = utils.get_cells_range(row_index, col_index, self.row_count, self.column_count)
        start_row, end_row = cells_range['start_row'], cells_range['end_row']
        start_column, end_column = cells_range['start_column'], cells_range['end_column']
        area = self.field[start_row:end_row+1, start_column:end_column+1]
        return len(list(filter(lambda cell: cell.get_value() == 9, area.flatten())))
    
    def set_state(self, state):
        self.state = state
        
    def get_state(self):
        return self.state


    def is_win(self):
        def get_flagged_cells_with_mines():
            return list(filter(lambda cell: cell.get_value() == 9 and cell.is_flagged() and not cell.is_opened(), self.field.flatten()))
        
        return self.available_flags_count == 0 and len(get_flagged_cells_with_mines()) == self.mines_count

    def foo(a, b):
        return a+b
    


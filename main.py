from field import GameState, Field
from commander import Commander
import os
import numpy as np
import sys
from cell import Cell

# Введите размер поля

row_count = int(input())
column_count = int(input())
mines_count = int(input())


c = Field(row_count, column_count, mines_count)
c.put_mines()
c.fill_numbers()
c.run()


def int_args(*args, func):
    int_args = list(map(int, args))
    func(int_args)
    
# @int_args(*args)
def open_cell(*args):
    int_args = list(map(int, args))
    c.open_cell(int_args[0] - 1, int_args[1] - 1)
    
def set_flag(*args):
    int_args = list(map(int, args))
    c.set_flag(int_args[0] - 1, int_args[1] - 1)
    
commander = Commander({
    'o':  open_cell,
    'f':  set_flag,
    'exit': lambda: sys.exit(0),
})

# [
#     ['*', '5', '*'],
#     ['*', '*', 'F'],
# ]


def clrscr():
    os.system('cls' if os.name == 'nt' else 'clear')
     
error = None

while True:
        clrscr()
        if error:
            print(error)
            error = None
        gotten_field = None
        if c.get_state() == GameState.DEFEAT:
            print('Game over, Pls matherfucker dont cry, play again')
            gotten_field = c.get_field(hidden=False)
        elif c.get_state() == GameState.WIN:
            print('Congratulations! You win! go hard mode syka')
            gotten_field = c.get_field(hidden=False)
        else:
            gotten_field = c.get_field()
            
        print('   ' + ' '.join([str(i+1) for i in range(c.column_count)]))
        for i, row in enumerate(gotten_field):
            if i < 9:
                print("%d  %s" % (i+1, ' '.join([cell for cell in row])))
            else:
                print("%d %s" % (i+1, ' '.join([cell for cell in row])))
        
        print('available flags count: %d' % c.available_flags_count)
                    
        if c.get_state() == GameState.DEFEAT or c.get_state() == GameState.WIN:
            # clrscr()
            break
        command = input('Input command: ')
        try:
            commander.execute(command)
        except KeyError:
            error = 'Incorrect command. Format: command [arg1, arg2, ..., argN]. Try again'
        except ValueError:
            error = 'Incorrect arguments. Format: command [arg1, arg2, ..., argN]. Try again'
        except IndexError:
            error = "Incorrect arguments. Coordinates out of the field's boundaries. Format: command [arg1, arg2, ..., argN]. Try again"
        except:
            error = 'Unknown error. Format: command [arg1, arg2, ..., argN]. Try again'






            # if pizza > 35
            #     print('таких размеров нет...')
            # elif pizza >= 28
            #     print('Нужна большаяю...')
            # elif pizza > 20
            #     print('нужна средня...')
            # else:
            #     print('маленькая')
            
        

    
    
    

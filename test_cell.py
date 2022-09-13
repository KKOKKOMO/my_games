from cell import Cell
import unittest

class TestCell(unittest.TestCase):

    def test_get_value(self):
        cases = [
            {
                'cell': Cell(9),
                'expected': 9,
            },
            {
                'cell': Cell(0),
                'expected': 0,
            },
            {
                'cell': Cell(5),
                'expected': 5,
            },
            {
                'cell': Cell(3),
                'expected': 3,
            },
        ]
        for case in cases:
            self.assertEqual(case['expected'], case['cell'].get_value())
        

    def test_is_flagged(self):
        cells = [
            Cell(9),
            Cell(0),
            Cell(5),
            Cell(3),
        ]
        
        for cell in cells:
            self.assertFalse(cell.is_flagged())
            cell.flag = True
            self.assertTrue(cell.is_flagged())
            
    def test_open(self):
        cells = [
            Cell(9),
            Cell(0),
            Cell(5),
        ]
        
        for cell in cells:
            cell.open()
            self.assertTrue(cell.opened)
            
        flagged_cell = Cell(4)
        flagged_cell.flag = True 
        flagged_cell.open()
        self.assertTrue(flagged_cell.opened)
        self.assertFalse(flagged_cell.flag)

        opened_cell = Cell(1)
        opened_cell.opened = True
        opened_cell.open()
        self.assertTrue(opened_cell.opened)

    def test_set_flag(self):
        cells = [
            Cell(9),
            Cell(0),
            Cell(5),
        ]
        for cell in cells:
            cell.set_flag(True)
            self.assertTrue(cell.flag)
            cell.set_flag(True)
            self.assertTrue(cell.flag)
            
            cell.set_flag(False)
            self.assertFalse(cell.flag)
            cell.set_flag(False)
            self.assertFalse(cell.flag)

if __name__ == '__main__':
    unittest.main()


# cases = [
#     {
#        'field': [
#             [1, 1, 1, 1],
#             [1, 1, 9, 1],
#             [1, 9, 3, 1],
#             [2, 9, 1, 1],
#         ]
#         'commands': [
#             lambda: field.open_cell(1, 1),
#             lambda: field.open_cell(1, 1),
#             lambda: field.set_flag(1, 1),
#         ],
#         'expected': True,
#     }
# ]
from field import Field, GameState
import unittest
import numpy as np
from cell import Cell
import collections
from collections import namedtuple


class TestField(unittest.TestCase):

    def setUp(self):
        self.field = Field(10, 10, 5)

    def test_get_state(self):
        self.field.run()
        self.assertEqual(GameState.RUNNING, self.field.get_state())

    def test_put_mines(self):
        cases = [
            {
                'field': Field(10, 10, 10),
                'expected': 10,
            },
            {
                'field': Field(20, 10, 50),
                'expected': 50,
            },
            {
                'field': Field(40, 40, 54),
                'expected': 54,
            },
            {
                'field': Field(4, 4, 6),
                'expected': 6,
            },
        ]
        for case in cases:
            case['field'].put_mines()
            mines_count = len(list(filter(lambda cell: cell.get_value(
            ) == 9 and not cell.is_flagged(), case['field'].field.flatten())))
            self.assertEqual(case['expected'], case['field'].mines_count)
            self.assertEqual(case['expected'], mines_count)

    def test_fill_numbers(self):
        cases = [
            {
                'field': [
                    [Cell(0), Cell(0), Cell(0), Cell(9)],
                    [Cell(0), Cell(9), Cell(0), Cell(9)],
                    [Cell(0), Cell(0), Cell(0), Cell(0)],
                    [Cell(0), Cell(0), Cell(0), Cell(9)],
                ],
                'mines_count': 4,
                'expected': [
                    [Cell(1), Cell(1), Cell(3), Cell(9)],
                    [Cell(1), Cell(9), Cell(3), Cell(9)],
                    [Cell(1), Cell(1), Cell(3), Cell(2)],
                    [Cell(0), Cell(0), Cell(1), Cell(9)],
                ],
            },
            {
                'field': [
                    [Cell(0), Cell(0), Cell(0), Cell(0)],
                    [Cell(0), Cell(9), Cell(0), Cell(0)],
                    [Cell(0), Cell(0), Cell(0), Cell(0)],
                    [Cell(0), Cell(0), Cell(0), Cell(0)],
                ],
                'mines_count': 1,
                'expected': [
                    [Cell(1), Cell(1), Cell(1), Cell(0)],
                    [Cell(1), Cell(9), Cell(1), Cell(0)],
                    [Cell(1), Cell(1), Cell(1), Cell(0)],
                    [Cell(0), Cell(0), Cell(0), Cell(0)],
                ],
            },
            {
                'field': [
                    [Cell(0), Cell(0), Cell(0), Cell(0)],
                    [Cell(0), Cell(0), Cell(0), Cell(0)],
                    [Cell(0), Cell(0), Cell(0), Cell(0)],
                    [Cell(0), Cell(0), Cell(0), Cell(0)],
                ],
                'mines_count': 0,
                'expected': [
                    [Cell(0), Cell(0), Cell(0), Cell(0)],
                    [Cell(0), Cell(0), Cell(0), Cell(0)],
                    [Cell(0), Cell(0), Cell(0), Cell(0)],
                    [Cell(0), Cell(0), Cell(0), Cell(0)],
                ],
            },
        ]

        def get_values(row):
            return list(map(lambda cell: cell.value, row))
            #     for j in range(len(field[i])):
            #         retu

        for case in cases:
            global_field = Field(
                4, 4, case['mines_count'], np.array(case['field']))
            global_field.fill_numbers()

            expected = case['expected']
            actual = global_field.field.tolist()
            for i in range(len(expected)):
                for j in range(len(expected[i])):
                    self.assertEqual(expected[i][j].value, actual[i][j].value,
                                     '''expected: {},
                           actual: {}.
                           (i: {}, j: {})'''.format(list(map(get_values, expected)),
                                                    list(
                                                        map(get_values, actual)),
                                                    i,
                                                    j,
                                                    ),
                                     )

    def test_set_flag(self):
        Point = namedtuple('Point', ('x', 'y'))

        cases = [
            {
                'field': [
                    [Cell(0), Cell(0), Cell(0), Cell(9)],
                    [Cell(0), Cell(9), Cell(0), Cell(9)],
                    [Cell(0), Cell(0), Cell(0), Cell(0)],
                    [Cell(0), Cell(0), Cell(0), Cell(9)],
                ],
                'mines_count': 4,
                'flags_coords': [
                    Point(1, 1),  # turple
                    Point(0, 3),
                    Point(1, 3),
                    Point(3, 3),
                ],
                'expected_available_flags_count': 0,
                'expected_state': GameState.WIN,
            },
            {
                'field': [
                    [Cell(0), Cell(0), Cell(0), Cell(9)],
                    [Cell(0), Cell(9), Cell(0), Cell(9)],
                    [Cell(0), Cell(0), Cell(0), Cell(0)],
                    [Cell(0), Cell(0), Cell(0), Cell(9)],
                ],
                'mines_count': 4,
                'flags_coords': [
                    Point(1, 1),  # tuple
                    Point(0, 3),
                    Point(3, 3),
                    Point(3, 3),
                ],
                'expected_available_flags_count': 2,
                'expected_state': GameState.RUNNING,
            },
        ]

        for case in cases:
            global_field = Field(
                4, 4, case['mines_count'], np.array(case['field']))
            global_field.fill_numbers()
            global_field.run()
            for point in case['flags_coords']:
                global_field.set_flag(point.x, point.y)

            self.assertEqual(
                case['expected_available_flags_count'], global_field.available_flags_count)
            self.assertEqual(case['expected_state'], global_field.state)

    def test_open_cell(self):
        Point = namedtuple('Point', ('x', 'y'))
        cases = [
            {
                'field': [
                    [Cell(1), Cell(1), Cell(3), Cell(9)],
                    [Cell(1), Cell(9), Cell(3), Cell(9)],
                    [Cell(1), Cell(1), Cell(3), Cell(2)],
                    [Cell(0), Cell(0), Cell(1), Cell(9)],
                ],
                'mines_count': 4,
                'open_coords': [
                    Point(0, 3),  # tuple
                ],
                'flag_coords': [],
                'expected_available_flags_count': 4,
                'expected_field_state': [
                    [
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': True,
                        },
                    ],
                    [
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },

                    ],
                    [
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },

                    ],
                    [
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                    ],
                ],
                'expected_state': GameState.DEFEAT,
            },
            {
                'field': [
                    [Cell(0), Cell(0), Cell(1), Cell(1)],
                    [Cell(0), Cell(0), Cell(1), Cell(9)],
                    [Cell(0), Cell(1), Cell(2), Cell(2)],
                    [Cell(0), Cell(1), Cell(9), Cell(1)],
                ],
                'mines_count': 2,
                'open_coords': [
                    Point(0, 1),  # tuple
                ],
                'flag_coords': [],
                'expected_available_flags_count': 2,
                'expected_field_state': [
                    [
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                    ],
                    [
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },

                    ],
                    [
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },

                    ],
                    [
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                    ],
                ],
                'expected_state': GameState.RUNNING,
            },
            {
            'field': [
                    [Cell(1), Cell(1), Cell(3), Cell(9)],
                    [Cell(1), Cell(9), Cell(3), Cell(9)],
                    [Cell(1), Cell(1), Cell(3), Cell(2)],
                    [Cell(0), Cell(0), Cell(1), Cell(9)],
                ],
                'mines_count': 4,
                'open_coords': [
                    Point(0, 3),  # tuple
                ],
                'flag_coords': [],
                'expected_available_flags_count': 4,
                'expected_field_state': [
                    [
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': True,
                        },
                    ],
                    [
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },

                    ],
                    [
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },

                    ],
                    [
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                    ],
                ],
                'expected_state': GameState.DEFEAT,
            },
            {
                'field': [
                    [Cell(0), Cell(0), Cell(1), Cell(1)],
                    [Cell(0), Cell(0), Cell(1), Cell(9)],
                    [Cell(0), Cell(1), Cell(2), Cell(2)],
                    [Cell(0), Cell(1), Cell(9), Cell(1)],
                ],
                'mines_count': 2,
                'open_coords': [
                    Point(0, 1),
                    Point(0, 1),
                    Point(1, 3),  # tuple
                ],
                'flag_coords': [
                    Point(1, 3),
                ],
                'expected_available_flags_count': 2,
                
                'expected_field_state': [
                    [
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                    ],
                    [
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': True,
                        },

                    ],
                    [
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },

                    ],
                    [
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': True,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                        {
                            'flag': False,
                            'opened': False,
                        },
                    ],
                ],
                'expected_state': GameState.RUNNING,
            },
        ]

        for case in cases:
            global_field = Field(
                4, 4, case['mines_count'], np.array(case['field']))
            global_field.run()
            for point in case['flag_coords']:
                global_field.field[point.x][point.y].flag = True
                global_field.available_flags_count -= 1

            for point in case['open_coords']:
                global_field.open_cell(point.x, point.y)

            for i in range(4):
                for j in range(4):
                    cell = global_field.field[i][j]
                    expected_field_state = case['expected_field_state']
                    self.assertEqual(expected_field_state[i][j], {
                        'flag': cell.flag,
                        'opened': cell.opened,
                    })
            
            self.assertEqual(case['expected_available_flags_count'], global_field.available_flags_count)

    def test_get_field(self):
        Point = namedtuple('Point', ('x', 'y'))
        cases = [
            {
                'field': [
                    [Cell(0), Cell(0), Cell(1), Cell(1)],
                    [Cell(0), Cell(0), Cell(1), Cell(9)],
                    [Cell(0), Cell(1), Cell(2), Cell(2)],
                    [Cell(0), Cell(1), Cell(9), Cell(1)],
                ],
                'mines_count': 2,

                'hidden': True,

                'open_coords': [
                    # Point(0, 1),  # tuple
                ],

                'flag_coords': [
                    # Point(3, 3),  # tuple
                ],

                'expected_field': [
                    ['*', '*', '*', '*'],
                    ['*', '*', '*', '*'],
                    ['*', '*', '*', '*'],
                    ['*', '*', '*', '*'],
                ]
            },
            {
                'field': [
                    [Cell(0), Cell(0), Cell(1), Cell(1)],
                    [Cell(0), Cell(0), Cell(1), Cell(9)],
                    [Cell(0), Cell(1), Cell(2), Cell(2)],
                    [Cell(0), Cell(1), Cell(9), Cell(1)],
                ],
                'mines_count': 2,

                'hidden': True,

                'open_coords': [
                    Point(0, 1),
                    Point(2, 2),
                    Point(1, 3),
                ],

                'flag_coords': [
                    Point(3, 3),
                    Point(3, 2),
                    Point(0, 0),
                ],

                'expected_field': [
                    ['F', '0', '*', '*'],
                    ['*', '*', '*', '9'],
                    ['*', '*', '2', '*'],
                    ['*', '*', 'F', 'F'],
                ]
            },
            {
                'field': [
                    [Cell(0), Cell(0), Cell(1), Cell(1)],
                    [Cell(0), Cell(0), Cell(1), Cell(9)],
                    [Cell(0), Cell(1), Cell(2), Cell(2)],
                    [Cell(0), Cell(1), Cell(9), Cell(1)],
                ],
                'mines_count': 2,

                'hidden': False,
                'open_coords': [
                    Point(0, 1),
                    Point(2, 2),
                    Point(1, 3),
                ],
                'flag_coords': [
                    Point(3, 3),
                    Point(3, 2),
                    Point(0, 0),
                ],
                'expected_field': [
                    ['0', '0', '1', '1'],
                    ['0', '0', '1', '9'],
                    ['0', '1', '2', '2'],
                    ['0', '1', '9', '1'],
                ]
            }
            ]

        for case in cases:
            global_field = Field(
                4, 4, case['mines_count'], np.array(case['field']))
            global_field.run()
            for point in case['flag_coords']:
                global_field.field[point.x][point.y].flag = True

            for point in case['open_coords']:
                global_field.field[point.x][point.y].opened = True

            actual_field = global_field.get_field(hidden=case['hidden'])
            self.assertEqual(case['expected_field'], actual_field)


if __name__ == '__main__':
    unittest.main()

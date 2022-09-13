class Cell:
    def __init__(self, value=0):
        self.value = value
        self.flag = False
        self.opened = False

    def get_value(self):
        return self.value
    
    def set_value(self, new_value):
        self.value = new_value

    def set_flag(self, state):
        if not self.is_opened():
            self.flag = state
            
    def is_flagged(self):
        return self.flag

    def open(self):
        self.opened = True
        self.flag = False

    def is_opened(self):
        return self.opened
     




     
# a = Cell(a, 5)
# b = Cell(b, 8)
# a = Cell(5)
# b = Cell()
# print(a.get_value())
# a.set_value(9)
# print(a.get_value())

# c = Cell(4)
# print(c.is_flagged())
# print(c.is_opened())
# c.open()
# print(c.is_opened())





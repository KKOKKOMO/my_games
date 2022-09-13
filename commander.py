class Commander():
    def __init__(self, actions):
        self.actions = actions

    def execute(self, command):
        #TODO: 'o 1 4' => ['o', '1', '4']
        action, *args = command.split(' ')
        # 'exit'
        self.actions[action](*args) # = open()
        # self.actions[action] => foo
        # foo(3, 4)
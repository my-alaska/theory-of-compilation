class Memory:

    def __init__(self, name):  # memory name
        self.name = name
        self.memory_dict = {}

    def has_key(self, name):  # variable name
        return name in self.memory_dict.keys()

    def get(self, name):  # gets from memory current value of variable <name>
        if name not in self.memory_dict.keys():
            return None
        return self.memory_dict[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.memory_dict[name] = value


class MemoryStack:

    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        if memory is None:
            memory = Memory("new memory")
        self.stack_list = [memory]

    def get(self, name):  # gets from memory stack current value of variable <name>
        for memory in reversed(self.stack_list):
            if memory.has_key(name):
                return memory.get(name)

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.stack_list[-1].put(name, value)

    def set(self, name, value):  # sets variable <name> to value <value>
        for memory in reversed(self.stack_list):
            if memory.has_key(name):
                memory.put(name,value)
                return
        self.insert(name,value)

    def push(self, memory):  # pushes memory <memory> onto the stack
        self.stack_list.append(Memory(memory))

    def pop(self):  # pops the top memory from the stack
        return self.stack_list.pop()
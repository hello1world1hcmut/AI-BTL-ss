class Node: 
    def __init__(self, state, parent = None, action = None):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
      for node in self.frontier:
        if node.state == state:
          return True
      return False

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
   

class Water_sort:

    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()
        
        contents = contents.splitlines()
        self.num_cups = int(contents[0])
        self.capacity = int(contents[1])

        contents = contents[2:]
        self.initial = []
        for i in range(self.num_cups):
            row = []
            if len(contents[i]) != 0:
                row = contents[i].split(' ')
            self.initial.append(row)
    
    def num_color_similar(self, row):
        clone_row = row[:]
        if len(clone_row) == 0:
            count = 0
        else:
            count = 1
            top_color = clone_row[-1]
            clone_row = clone_row[:-1]
            while len(clone_row) != 0:
                check_color = clone_row[-1]
                clone_row = clone_row[:-1]
                if check_color == top_color:
                    count += 1
                else:
                    break
        return count
    
    def get_legal_move(self, state, i, j):
        len_i = len(state[i])
        len_j = len(state[j])

        if len_i == 0 or len_j == self.capacity or ( len_i != 0 and len_j != 0 and state[i][-1] != state[j][-1]):
            return None
        else:
            num = self.num_color_similar(state[i])
            sum_check = num + len_j
            if sum_check > self.capacity:
                return (i, j, self.capacity - len_j)
            else:
                return (i, j, num)
    
    def move(self, state, legal_move_tuple):
        clone_state = []
        for i in range(self.num_cups):
            new_stack = state[i][:]
            clone_state.append(new_stack)

        i, j, num_to_move = legal_move_tuple

        while num_to_move != 0:
            color_out = clone_state[i][-1]
            clone_state[i] = clone_state[i][:-1]
            clone_state[j].append(color_out)
            num_to_move -= 1
        return clone_state

    def successors(self, state):
        result = []
        for i in range(self.num_cups):
            for j in range(self.num_cups):
                if i == j:
                    continue
                legal_move = self.get_legal_move(state, i, j)
                if legal_move != None:
                    result.append((self.move(state, legal_move), legal_move))
        return result
    
    def is_goal(self, state):
        
        count = 0
        for i in range(self.num_cups):
            if self.num_color_similar(state[i]) == self.capacity or self.num_color_similar(state[i]) == 0:
                count += 1
        
        if count == self.num_cups:
            return True
        else:
            return False
    
    def print_state(self, state):
    	# Print current status
        if state == None:
            print(None)
            return None

        space = " " * 3
        for j in range(self.capacity-1,-1,-1):
            a = ""
            for i in range(self.num_cups):
                if len(state[i]) > j:
                    color = state[i][j]
                else:
                    color = "."
                a += "|" + ("%s"%color).center(6) + "|" + space
            print(a)
        a = ""
        for i in range(self.num_cups):
            a += "\\" + "_".center(6,"_") + "/" + space
        print(a)
    
    def print_result(self, node):
        if node.parent != None:
            self.print_result(node.parent)
        self.print_state(node.state)
        print(node.action)
        print()

    def solve(self):
        self.num_explored = 0
        
        start = Node(state = self.initial)
        frontier = StackFrontier()
        frontier.add(start)
        self.explored = []

        while True:
            if frontier.empty():
                raise Exception("no solution")
            
            node = frontier.remove()
            if self.is_goal(node.state):
                self.print_result(node)
                return

            self.explored.append(node.state)

            for state, legal_move in self.successors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=legal_move)
                    frontier.add(child)




        
            




m = Water_sort('testcase3.txt')
#print(len(m.successors(m.initial)))
#print(m.get_legal_move(m.initial, 0, 1))
#print(m.initial[1])
m.solve()
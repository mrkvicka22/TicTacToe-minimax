import random
EMPTY = 0
X = 1
O = 2
DEFAULT_BOARD = [0, 0, 0, 0, 0, 0, 0, 0, 0]
TEST_BOARD = [2, 1, 2, 2, 1, 1, 1, 2, 1]
finite_layer = []
#TODO: If plays unreasonable swap min and max

def generate_stuff(node):
    for child in node.generate_children():
        if child.finite() is False:
            generate_stuff(child)
        else:
            finite_layer.append(child)


def switch_1_to_2(one_or_two):
    return (one_or_two % 2) + 1

class BoardStateNode:

    def __init__(self, board_state, player, layer):
        self.board_state = board_state
        self.player = player
        self.children = []
        self.layer = layer
        self.value = None


    def generate_children(self):
        self.children = []
        for i in range(len(self.board_state)):
            if self.board_state[i] == EMPTY:
                new_board_state = self.board_state.copy()
                new_board_state[i] = self.player
                self.children.append(BoardStateNode(new_board_state, switch_1_to_2(self.player), self.layer+1))
        return self.children



    def calc_value(self):
        if self.layer % 2 == 0:
            if self.finite() is True:
                return self.value
            else:
                return max([child.calc_value() for child in self.generate_children()])
        else:
            if self.finite() is True:

                return self.value
            else:
                return min([child.calc_value() for child in self.generate_children()])

    def choose(self):
        best_vals = []
        if self.layer % 2 == 0:
            maxi = -1
            for i in self.generate_children():
                val = i.calc_value()
                if val > maxi:
                    best_vals = [i]
                    maxi = val
                elif val == maxi:
                    best_vals.append(i)
                else:
                    pass
        else:
            mini = 1
            for i in self.generate_children():
                val = i.calc_value()
                if val < mini:
                    best_vals = [i]
                    mini = val
                elif val == mini:
                    best_vals.append(i)
                else:
                    pass
        return random.choice(best_vals)


    def finite(self):
        #draw
        if self.board_state.count(EMPTY) == 0:
            self.value = 0
            return True
        #next to each other
        #X
        if self.board_state[0:3].count(X)==3 or self.board_state[3:6].count(X) == 3 or self.board_state[6:9].count(X) == 3:
            self.value = 1
            return True
        #O
        if self.board_state[0:3].count(O) == 3 or self.board_state[3:6].count(O) == 3 or self.board_state[6:9].count(
                O) == 3:
            self.value = -1
            return True

        #below each other
        #X
        for i in range(3):
            if self.board_state[i] == X and self.board_state[i+3]==X and self.board_state[i + 6]==X:
                self.value = 1
                return True
        #O
        for i in range(3):
            if self.board_state[i] == O and self.board_state[i + 3] == O and self.board_state[i + 6] == O:
                self.value = -1
                return True

        #diagonal
        #X
        if self.board_state[0] == X and self.board_state[4] == X and self.board_state[8] == X:
            self.value = 1
            return True
        if self.board_state[2] == X and self.board_state[4] == X and self.board_state[6] == X:
            self.value = 1
            return True
        #O
        if self.board_state[0] == O and self.board_state[4] == O and self.board_state[8] == O:
            self.value = -1
            return True
        if self.board_state[2] == O and self.board_state[4] == O and self.board_state[6] == O:
            self.value = -1
            return True

        return False

    def __str__(self):
        s = ""
        for i in range(0,9,3):
            s+= " ".join([str(self.board_state[j]) for j in range(i,i+3)]) + "\n"
        return s
        #return self.board_state.__str__()


root = BoardStateNode(DEFAULT_BOARD, X, 0)

state = root
print("now you will play against the ai")
print(state)
i = 0
while not state.finite():
    if i % 2 == 0:
        state = state.choose()
        print(state)
    else:

        state.board_state[int(input("Type 1-9"))-1] = O
        brd = state.board_state
        state = BoardStateNode(brd, i % 2, i-1)
        print(state)
    i+=1

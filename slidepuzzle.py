from enum import Enum
from collections import deque 
import os, time
class Moves(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    START = 5

class GameState:
    def __init__(self, state, width, index = None, previous = None):
        self.state = state
        self.width = width
        self.length = len(state)
        self.previous = previous
        if not index:
            self.index = state.index('*')
        else:
            self.index = index
    def __str__(self):
        out = ""
        for (i, c) in enumerate(self.state):
            out += c + " "
            if i%self.width == self.width-1:
                out += "\n"
        return out
    def __eq__(self, other):
        return self.state == other.state
    def __hash__(self):
        return hash("".join(self.state))
    def apply_moves(self, move):
        new_index = -1
        if move is Moves.UP and self.index >= self.width:
            new_index = self.index - self.width
        elif move is Moves.DOWN and self.index < self.length - self.width:
            new_index = self.index + self.width
        elif move is Moves.LEFT and self.index%self.width > 0:
            new_index = self.index - 1
        elif move is Moves.RIGHT and self.index%self.width < self.width-1:
            new_index = self.index + 1

        if new_index == -1:
            return None

        new_state = self.state.copy()

        new_state[new_index] = self.state[self.index] 
        new_state[self.index] = self.state[new_index] 

        return GameState(new_state, 3, new_index, self)
    def get_reverse_history(self):
        history = [self]
        prev = self.previous
        while prev:
            history.append(prev)
            prev = prev.previous
        return history
        
    def get_history(self):
        history = self.get_reverse_history()
        history.reverse()
        return history

    def legal_moves(self):
        return filter(lambda f: f, map(lambda m: self.apply_moves(m), [Moves.UP, Moves.DOWN, Moves.LEFT, Moves.RIGHT]))

def search(start, end):
    seen = { start }
    todo = deque( [ start ])

    while len(todo):
        for moved in todo.popleft().legal_moves():
            if moved in seen: continue
            if moved == end:
                return moved.get_history()
            seen.add(moved)
            todo.append(moved)
            #if len(start)%10000 == 0:
            #    print(f"seen: { len(start) }, todo: { len(todo) } ")        
    return []

def double_ended_search(start, end):
    start_seen = { start }
    start_todo = deque( [ start ])
    end_seen = { end }
    end_todo = deque( [ end ] )

    while len(start_todo) or len(end_todo):
        for moved in start_todo.popleft().legal_moves():
            if moved in start_seen: continue
            if moved in end_seen:
                end_seen_list = list(end_seen)
                end_moved = end_seen_list[end_seen_list.index(moved)]
                return moved.get_history() + end_moved.previous.get_reverse_history()
            start_seen.add(moved)
            start_todo.append(moved)
        for moved in end_todo.popleft().legal_moves():
            if moved in end_seen: continue
            if moved in start_seen:
                start_seen_list = list(start_seen)
                start_moved = start_seen_list[start_seen_list.index(moved)]
                return start_moved.get_history() + moved.previous.get_reverse_history()
            end_seen.add(moved)
            end_todo.append(moved)
        
    return []

millis = lambda: time.time()*1000.0

start = GameState(['0', '1', '2',
                   '3', '7', '6',
                   '5', '*', '0'], 3)

end = GameState(['0', '1', '2',
                 '3', '*', '5',
                 '6', '7', '0'], 3)

stime = millis()
solution = double_ended_search(start, end)
etime = millis() - stime

s2time = millis()
solution2 = search(start, end)
e2time = millis() - s2time
for (i,s) in enumerate(solution):
    print(f"------{i}:\n{s}")
    # print(f"------{i}:\n{s}\n\n{solution2[i]}")
print("Double ended search:")
print(f"Number of moves: {len(solution)-1}")
print(f"Time taken: {etime}ms")
print("Regular search:")
print(f"Number of moves: {len(solution2)-1}")
print(f"Time taken: {e2time}ms")
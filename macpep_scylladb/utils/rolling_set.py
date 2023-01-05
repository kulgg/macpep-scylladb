from collections import deque


class RollingSet:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.set = set()
        self.order = deque()

    def add(self, value):
        if value in self.set:
            # If the value is already in the set, move it to the end of the order
            self.order.remove(value)
        elif len(self.set) == self.maxsize:
            # If the set is at maximum size, remove the least recently accessed value
            self.set.remove(self.order.popleft())
        self.set.add(value)
        self.order.append(value)

    def __contains__(self, value):
        if value in self.set:
            # If the value is in the set, move it to the end of the order
            self.order.remove(value)
            self.order.append(value)
            return True
        return False

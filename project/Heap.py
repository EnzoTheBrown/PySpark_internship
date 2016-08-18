import math

class myHeap:
    def __init__(self):
        self.heap = []

    def push(self,
             value):
        print(value[1])
        self.heap.append(value)
        current = len(self.heap) - 1
        if len(self.heap) != 1:
            while True:
                if (self.compare(self.heap[int((current - 1) / 2)], self.heap[current])):
                    self.swap(current, int((current - 1) / 2))
                current = int((current - 1) / 2)
                if (current == 0 or (self.compare(self.heap[current], self.heap[int((current - 1) / 2)]))):
                    break
        self.first = self.heap[0]
        self.last = self.heap[len(self.heap) - 1]
        print('end')

    def pop(self):
        self.swap(0, len(self.heap) - 1)
        max = self.heap.pop()
        current = 0
        while True:
            child = current*2 + 1
            if child < len(self.heap) and child + 1 >= len(self.heap):
                if self.compare(self.heap[child], self.heap[current]):
                    self.swap(current, child)
                break
            if child >= len(self.heap) or child + 1 >= len(self.heap):
                break
            if self.compare(self.heap[child], self.heap[child + 1]):
                child += 1
            if self.compare(self.heap[current], self.heap[child]):
                self.swap(current, child)
            else:
                break
            current = child
        return max

    def swap(self,
             a,
             b):
        temp = self.heap[a]
        self.heap[a] = self.heap[b]
        self.heap[b] = temp

    def display(self):
        print(self.heap)

    def is_heap(self):
        i = 0
        while i < len(self.heap):
            if self.compare(self.heap[int((i - 1) / 2)], self.heap[i]):
                return False
            i += 1
        return True

    def compare(self,
                left,
                right):
        if(left[1] > right[1]):
            return True
        return False

    def empty(self):
        if len(self.heap) == 0:
            return True
        return False


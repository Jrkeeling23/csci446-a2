
class PriorityQueue:
    """
    basic Priority Queue that ignores priority ties, and does not return the priority on a get.
    can also be a standard queue by flipping the priority boolean to False
    """
    def __init__(self):
        self.queue = []
        self.empty = True
        self.priority = True

    def put(self, data, priority=0):
        # add data at end if unordered
        if not self.priority:
            self.queue.append([priority, data])
        # otherwise insert before first higher priority
        else:
            if self.empty:
                self.queue.append([priority, data])
            else:
                placed = False
                for i in range(len(self.queue)):
                    # start at front and work forward
                    if self.queue[i][0] > priority:
                        # place immediately in front of the higher value
                        self.queue.insert(i, [priority, data])
                        placed = True
                # was not placed, so place at end
                if not placed:
                    self.queue.append([priority, data])
        # no longer empty
        self.empty = False

    def get(self):
        if self.empty:
            return None
        else:
            if len(self.queue) == 1:
                self.empty = True
            return self.queue.pop(0)[1]
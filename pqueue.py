# Priority queue implementation modified from the one at
# https://docs.python.org/2/library/heapq.html
#
# The only substantive differences are:
#
# 1. Removed the entry counter because we don't care about what order
#    equivalent priority nodes are retrieved in (i.e. no sort
#    stability).
#
# 2. Added an empty() method to query whether there's anything left in
#    the queue.

import heapq

REMOVED = '<removed-task>'      # placeholder for a removed task
class PriorityQueue:
    def __init__(self):
        self.pq = []            # list of entries arranged in a heap
        self.entry_finder = {}  # mapping of tasks to entries

    def add_task(self, task, priority):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        entry = [priority, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)

    def remove_task(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = REMOVED

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, task = heapq.heappop(self.pq)
            if task is not REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    def empty(self):
        'Returns True if there are no non-removed tasks queued.'
        # TODO: Find a better way to check whether there are any live
        # tasks than walking the list. A "live tasks" count would do
        # it, but that adds complexity. We'll see if things are slow
        # before we go there.
        return all((task is REMOVED) for _,task in self.pq)


if __name__ == '__main__':
    # Run some tests. Ideally we'd put this into a proper test
    # fixture, but we can optimize for maintainability later.

    # Basic task addition.
    pq = PriorityQueue()
    assert pq.empty()
    pq.add_task(1, priority=100)
    assert not pq.empty()
    pq.add_task(2, priority=-1)
    assert not pq.empty()
    task = pq.pop_task()
    assert task == 2
    task = pq.pop_task()
    assert task == 1
    assert pq.empty()

    # Task deletion
    pq.add_task(1, priority=100)
    pq.add_task(2, priority=0)
    pq.remove_task(2)
    task = pq.pop_task()
    assert task == 1
    assert pq.empty()

    # Task reprioritization
    pq.add_task(1, priority=100)
    pq.add_task(2, priority=0)
    pq.add_task(1, priority=-1)
    task = pq.pop_task()
    assert task == 1
    task = pq.pop_task()
    assert task == 2
    assert pq.empty()

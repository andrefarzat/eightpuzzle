from typing import List
from eightpuzzle import State
from eightpuzzle.searches import InteractiveSearch, DepthFirstSearch, BreadthFirstSearch


def main():
    # initial_state = State([1, 2, 3, 4, 5, 6, 7, 0, 8])
    initial_state = State([1, 2, 3, 4, 5, 0, 6, 7, 8])
    # initial_state = State([0, 8, 7, 6, 5, 4, 3, 2, 1])

    final_state = State([1, 2, 3, 4, 5, 6, 7, 8, 0])

    # search = InteractiveSearch(initial_state, final_state)
    # search = DepthFirstSearch(initial_state, final_state)
    search = BreadthFirstSearch(initial_state, final_state)
    state = search.do_search()
    # import pdb; pdb.set_trace()
    print_finish(state)


def print_finish(state: State):
    print('')
    parents: List[State] = []
    current_state: State = state

    while current_state.parent:
        current_state = current_state.parent
        parents.append(current_state)

    parents.reverse()

    for i, parent in enumerate(parents):
        parent.print('State index %s' % i)

    state.print("Found state:")


if __name__ == '__main__':
    main()

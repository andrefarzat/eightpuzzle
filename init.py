from typing import List, Type

from eightpuzzle import State
from eightpuzzle.searches import (InteractiveSearch, DepthFirstSearch, BreadthFirstSearch, HillClimbingSearch,
                                  HillClimbingWithAnnealingSearch, AStarSearch, Search)


SEARCHES: List[Type[Search]] = [InteractiveSearch, DepthFirstSearch, BreadthFirstSearch, HillClimbingSearch,
                                HillClimbingWithAnnealingSearch, AStarSearch]


def main():
    # initial_state = State([1, 2, 3, 4, 5, 6, 7, 0, 8])
    # initial_state = State([1, 2, 3, 4, 5, 6, 0, 7, 8])
    # initial_state = State([1, 2, 3, 4, 5, 0, 6, 7, 8])
    initial_state = State([1, 2, 3, 0, 4, 5, 7, 8, 6])
    # initial_state = State([0, 8, 7, 6, 5, 4, 3, 2, 1])

    final_state = State([1, 2, 3, 4, 5, 6, 7, 8, 0])

    initial_state.print('Initial state: ')
    final_state.print('Final state: ')

    print('')
    search_class = get_search_class()
    search = search_class(initial_state, final_state)

    print('')
    state = search.do_search()

    if not state:
        print('Fail :(')
    else:
        print_finish(state)


def print_finish(state: State):
    print('')
    parents: List[State] = state.get_parents()
    parents.reverse()

    for i, parent in enumerate(parents):
        parent.print('State index %s' % i)

    state.print("Found state in index %s in %s evaluations:" % (i+1, State.count))


def get_search_class() -> Type[Search]:
    while True:
        for i, search in enumerate(SEARCHES):
            print("%s: %s" % (i, search.__name__))

        try:
            index = int(input('Informe qual busca utilizar: '))
        except ValueError:
            print('Opção inválida')
            continue

        try:
            s = SEARCHES[index]
        except IndexError:
            print('Opção inválida')
            continue

        return s


if __name__ == '__main__':
    try:
        main()
    except RecursionError:
        print('Infinity loop in %s' % State.count)


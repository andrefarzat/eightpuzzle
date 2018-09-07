from eightpuzzle import State
from eightpuzzle.searches import InteractiveSearch


def main():
    initial_state = State(0, 8, 7, 6, 5, 4, 3, 2, 1)
    final_state = State(1, 2, 3, 4, 5, 6, 7, 8, 0)

    search = InteractiveSearch(initial_state, final_state)
    search.do_search()


if __name__ == '__main__':
    main()

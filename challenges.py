######################################
#                                    #
# Level 1 (2 pts each)               #
#                                    #
######################################
import math
import string


def is_pal(word):
    """
    >>> is_pal("cars")
    False
    >>> is_pal("tacocat")
    True
    >>> is_pal("aa")
    True
    >>> is_pal("abaa")
    False
    >>> is_pal("tacobcat")
    False
    """
    if word == word[::-1]:
        return True
    return False


def add_evens(nums):
    """
    >>> add_evens([5])
    5
    >>> add_evens([1, 2, 3, 4, 5])
    9
    >>> add_evens([-4, 3, 0, 2])
    -4
    """
    tot = 0
    for i in range(len(nums)):
        if i % 2 == 0:
            tot += nums[i]
    return tot


def add_evens_followup(nums):
    """
    >>> add_evens(5)
    5
    >>> add_evens(12345)
    9
    >>> add_evens(4302])
    5
    """
    nums, tot = str(nums)[::-1], 0
    for i in range(len(nums)):
        if i % 2 == 0:
            tot += int(nums[i])
    return tot


######################################
#                                    #
# Level 2 (3 pts each)               #
#                                    #
######################################


def can_cheese(small: int, big: int, goal: int) -> bool:
    """
    >>> can_cheese(3, 1, 8)
    True
    >>> can_cheese(3, 1, 9)
    False
    >>> can_cheese(3, 2, 10)
    True
    >>> can_cheese(1, 3, 12)
    False
    >>> can_cheese(13, 1, 13)
    True
    >>> can_cheese(14, 0, 13)
    True
    """
    pass


def can_cheese_followup(small, small_size, big, big_size, goal) -> bool:
    """
    More test cases to come...
    >>> can_cheese(3, 3, 5, 5, 27)
    True
    >>> can_cheese(3, 3, 5, 5, 28)
    True
    >>> can_cheese(3, 3, 5, 5, 32)
    False
    """
    pass


def min_of_maxes(nums: int, k: int) -> int:
    """
    >>> min_of_maxes([1,3,-1,-3,5,3,6,7], 3)
    3
    >>> min_of_maxes([1,3,-1,-3,5,3,6,7], 1)
    -3
    """
    pass


######################################
#                                    #
# Level 3 (4 pts each)               #
#                                    #
######################################


def space_acquaintance(space_from: list, space_to: list) -> int:
    """
    >>> space_acquaintance([1, 2, 2, 3, 4, 5], [2, 4, 5, 5, 5, 6])
    3
    >>> space_acquaintance([1, 4, 4, 2, 5, 6, 7, 2], [3, 1, 3, 5, 6, 7, 5, 6])
    0
    """
    pass


def shortest_path(graph: dict, A: int, B: int) -> int:
    """
    >>> shortest_path({1:[2], 2:[]}, 1,2)
    1
    >>> shortest_path({1: [2, 3], 2: [1, 3, 8], 3: [1, 2, 4, 8], 5: [3, 6], 6: [5, 7], 7: [6, 8], 8: [2, 7]}, 1, 1)
    0
    >>> shortest_path({1: [2, 3], 2: [1, 3, 8], 3: [1, 2, 4, 8], 5: [3, 6], 6: [5, 7], 7: [6, 8], 8: [2, 7]}, 1, 8)
    2
    >>> shortest_path({1: [2, 3], 2: [1, 3, 8], 3: [1, 2, 4, 8], 5: [3, 6], 6: [5, 7], 7: [6, 8], 8: [2, 7]}, 4, 7)
    3
    """
    if A == B:
        return 0

    if A not in graph:
        connections = []
        for departure_station in list(graph):
            if A in graph[departure_station]:  # departure_station has a route to A...
                connections.append(departure_station)  # ...so A has a route to departure_station
        graph[A] = connections
    if B not in graph:
        connections = []
        for departure_station in list(graph):
            if B in graph[departure_station]:
                connections.append(departure_station)
        graph[B] = connections

    path_options = []
    for next_station in graph[A]:
        reduced_graph = graph.copy()
        del reduced_graph[A]  # rid the graph of the current station, to avoid (infinite) loops back to it
        if next_station in reduced_graph:
            path_options.append(shortest_path(reduced_graph, next_station, B))
        else:
            path_options.append(math.inf)
    # return the cost of the best route from this station, plus the cost to get to this station in the first place
    return 1 + min(path_options)


def longest_uppercase(input, k):
    """
    >>> longest_uppercase("aaabbcajnnaddgfjn", 2)
    5
    >>> longest_uppercase("aaabbbcajnnnnaddgfjn", 1)
    4
    >>> longest_uppercase("aaabbbcajnnnnadddgfjn", 4)
    9
    """
    input = input.lower()
    max_length = 0
    for i in range(len(input)):
        uppercase_letters = []
        substring = ""
        for l in input[i:]:
            if l not in string.ascii_lowercase or (len(uppercase_letters) >= k and l not in uppercase_letters):
                break
            substring += l
            if l not in uppercase_letters:
                uppercase_letters.append(l)
        max_length = max(max_length, len(substring))
    return max_length


######################################
#                                    #
# Extras (0 pts each)                #
#                                    #
######################################


def max_tastiness(ice_creams):
    """
    >>> round(max_tastiness([(4,.9), (6,.5)]), 5)
    9.4
    >>> round(max_tastiness([(10,0.1),(5,0.1),(4,0.2),(2,0.6)]), 5)
    10.544
    >>> round(max_tastiness([(0,1),(1,1),(0,0),(1,0),(5,0.4),(4,0.5),(2,0.7)]), 5)
    8.14
    >>> ar = [((0.003*x*x*x + 0.001*x*x + 4.159)%100, (0.00265*x*x)%1) for x in range(10000)]
    >>> round(max_tastiness(ar), 5)
    7534.58121
    """
    pass


def lifeguard_budget(intervals):
    """
    >>> lifeguard_budget([(0,1000),(0,500),(500,1440)])
    1440
    >>> lifeguard_budget([(0,1000),(0,500),(501,1440)])
    1939
    >>> lifeguard_budget([(a*5-7,a*5) for a in range(400)])
    2016
    >>> lifeguard_budget([(a*6-10,a*6-2) for a in range(400)][::-1])
    1928
    """
    pass


def largest_valid_tree(edge_string):
    """
    >>> largest_valid_tree("AB AC BD")
    3
    >>> largest_valid_tree("AB BC CA")
    2
    """
    pass


if __name__ == "__main__":
    import doctest

    doctest.testmod()

######################################
#                                    #
# Level 1 (2 pts each)               #
#                                    #
######################################
import copy
import fractions
import math
import string
from typing import List, Dict, Tuple, Set, Union


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
    >>> add_evens_followup(5)
    5
    >>> add_evens_followup(12345)
    9
    >>> add_evens_followup(4302)
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
    return can_cheese_followup(small, 1, big, 5, goal)


def can_cheese_followup(small, small_size, big, big_size, goal) -> bool:
    """
    >>> can_cheese_followup(4, 3, 5, 5, 27)
    True
    >>> can_cheese_followup(3, 3, 5, 5, 28)
    True
    >>> can_cheese_followup(3, 3, 5, 5, 32)
    False
    """
    if small < 0:
        return False
    big_needed = fractions.Fraction(goal - small_size * small, big_size)
    if big_needed.denominator == 1:  # quantity of big cheeses is a whole number
        if big >= big_needed >= 0:  # we aren't exceeding our big cheese limit
            return True
    return can_cheese_followup(small - 1, small_size, big, big_size, goal)


def min_of_maxes(nums: List[int], k: int) -> int:
    """
    >>> min_of_maxes([1,3,-1,-3,5,3,6,7], 3)
    3
    >>> min_of_maxes([1,3,-1,-3,5,3,6,7], 1)
    -3
    """
    if k > len(nums):
        k = len(nums)
    maxima = []
    for i in range(len(nums) - k + 1):
        maxima.append(max(nums[i: i + k]))
    return min(maxima)


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
    if len(space_from) != len(space_to):
        return -1  # this behaviour is not defined

    acquaintance_index: Dict[int, List[int]] = {}  # maps each astronaut to a list of other astronauts whom they know
    for i in range(len(space_from)):
        if space_from[i] == space_to[i]:
            continue
        if space_from[i] not in acquaintance_index:  # if we haven't yet started building an index for this astronaut...
            acquaintance_index[space_from[i]] = []  # ...start building an index
        if space_to[i] not in acquaintance_index:
            acquaintance_index[space_to[i]] = []
        # add each astronaut to the other's index, if they're not already there
        if space_to[i] not in acquaintance_index[space_from[i]]:
            acquaintance_index[space_from[i]].append(space_to[i])
        if space_from[i] not in acquaintance_index[space_to[i]]:
            acquaintance_index[space_to[i]].append(space_from[i])
    # sort acquaintance indices
    for astronaut in list(acquaintance_index):
        acquaintance_index[astronaut].sort()

    astronauts = list(acquaintance_index)
    astronauts.sort()
    trios: List[tuple] = []
    for astronaut in astronauts:
        # find all trios containing this astronaut
        # for a trio, this first astronaut must know a second astronaut, who knows a third astronaut, who in turn knows
        # this first astronaut
        for second_astronaut in acquaintance_index[astronaut]:
            for third_astronaut in acquaintance_index[second_astronaut]:
                if astronaut in acquaintance_index[third_astronaut]:  # this is a trio
                    # we list trios as 3-tuples, with the astronauts in ascending order
                    # if these astronauts are not in ascending order, we need not record this trio, as it will duplicate
                    # the previous record of this same trio
                    if astronaut < second_astronaut < third_astronaut:
                        trios.append((astronaut, second_astronaut, third_astronaut))

    if len(trios) == 0:
        return -1

    acquaintance_sums: List[int] = []
    for trio in trios:
        # list the astronauts known by this trio
        acquaintances: List[int] = []
        for astronaut in acquaintance_index[trio[0]]:
            if astronaut not in acquaintances and astronaut not in trio:
                acquaintances.append(astronaut)
        for astronaut in acquaintance_index[trio[1]]:
            if astronaut not in acquaintances and astronaut not in trio:
                acquaintances.append(astronaut)
        for astronaut in acquaintance_index[trio[2]]:
            if astronaut not in acquaintances and astronaut not in trio:
                acquaintances.append(astronaut)
        acquaintance_sums.append(len(acquaintances))

    return min(acquaintance_sums)


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
    if len(path_options) == 0:
        path_options.append(math.inf)  # destination unreachable
    # return the cost of the best route from this station, plus the cost to get to this station in the first place
    return 1 + min(path_options)


def longest_uppercase(input_string, k):
    """
    >>> longest_uppercase("aaabbcajnnaddgfjn", 2)
    5
    >>> longest_uppercase("aaabbbcajnnnnaddgfjn", 1)
    4
    >>> longest_uppercase("aaabbbcajnnnnadddgfjn", 4)
    10
    """
    input_string = input_string.lower()
    max_length = 0
    for i in range(len(input_string)):
        uppercase_letters = []
        substring = ""
        for letter in input_string[i:]:
            if letter not in string.ascii_lowercase or (
                    len(uppercase_letters) >= k and letter not in uppercase_letters):
                break
            substring += letter
            if letter not in uppercase_letters:
                uppercase_letters.append(letter)
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


def lifeguard_budget(intervals: List[Tuple[int, int]]) -> int:
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
    intervals.sort(key=lambda interval: interval[0])
    return lifeguard_shift({i for i in range(0, 1440)}, intervals)


def lifeguard_shift(shifts_required: Set[int], lifeguards: List[Tuple[int, int]]) -> Union[int, float]:
    """Return the minimum cost of hiring lifeguards to cover all the shifts

    :param shifts_required: a set of times (minutes) which must be covered by lifeguards
    :param lifeguards: a list of the time intervals for which each respective lifeguard is available, in ascending order
        by start time
    :return: the minimum cost of hiring lifeguards from the lifeguards list, in order to fully cover the shifts
    """

    reduced_lifeguards = copy.deepcopy(lifeguards)
    current_lifeguard = reduced_lifeguards.pop(0)

    if len(shifts_required) == 0:
        # shifts are already fully covered
        return 0
    else:
        if min(shifts_required) < current_lifeguard[0]:
            # lifeguards will only have progressively later start times from here on out
            # we can't cover this first part of the shift
            return math.inf

    # The full shift covered by current_lifeguard
    current_shift = {i for i in range(current_lifeguard[0], current_lifeguard[1])}
    # The remaining shifts to be covered assuming we have hired current_lifeguard
    reduced_shifts = shifts_required.difference(current_shift)

    if len(lifeguards) == 1:  # current_lifeguard is the only lifeguard remaining
        if len(reduced_shifts) == 0:
            # we can cover all shifts by hiring current_lifeguard
            return abs(current_lifeguard[1] - current_lifeguard[0])
        return math.inf  # there is no way to cover all the shifts

    # The minimum cost possible if we hire current_lifeguard
    hiring_cost = abs(current_lifeguard[1] - current_lifeguard[0]) + lifeguard_shift(reduced_shifts, reduced_lifeguards)

    if hiring_cost == math.inf:
        return math.inf  # don't bother checking what happens if we skip

    # The portion of current_lifeguard's shift which overlaps with another lifeguard
    overlapping_shift = current_shift.difference(shifts_required)
    # The unique shift covered by current_lifeguard (i.e. the portion of current_lifeguard's shift which is not already
    # covered by another lifeguard)
    unique_shift = current_shift.difference(overlapping_shift)

    if min(unique_shift) < lifeguards[1][0]:
        # current_lifeguard covers a shift that nobody else can cover
        # we therefore must hire them
        return hiring_cost

    # The minimum cost possible if we don't hire current_lifeguard
    skipping_cost = lifeguard_shift(shifts_required, reduced_lifeguards)

    return min(skipping_cost, hiring_cost)


def largest_valid_tree(edge_string: str) -> int:
    """
    >>> largest_valid_tree("AB AC BD")
    3
    >>> largest_valid_tree("AB BC CA")
    2
    """
    edge_string = edge_string.lower()
    edges: Dict[str, List[str]] = parse_edges(edge_string)[0]

    if len(list(edges)) == 0:
        return 0

    subtree_sizes: List[int] = []
    for parent in list(edges):
        subtree_sizes.append(largest_valid_subtree(edge_string, parent))
    return max(subtree_sizes)


def largest_valid_subtree(edge_string: str, root: str) -> int:
    edges: Dict[str, List[str]] = parse_edges(edge_string)[0]

    if root not in edges:
        return 0

    # stores the nodes at each level of the tree, where levels[0] is a list of nodes at the root level (i.e. just the
    # root node), levels[1] is a list of nodes at the level below that, and so forth.
    levels: List[List[str]] = [[root]]
    next_level = get_level_below(edge_string, [root])
    while len(next_level) != 0:
        levels.append(next_level)
        next_level = get_level_below(edge_string, levels[-1])
        for node in next_level:
            if node in edges:  # node has children
                for child in edges[node]:
                    if exists_in_higher_level(levels, child):  # node links to another node which already exists
                        # remove this illegal link
                        if edge_string.count(node + child) > 0:
                            i = edge_string.index(node + child)
                            edge_string = edge_string[:i] + edge_string[i + 3:]

    edge_count = 0
    for level in levels:
        edge_count += len(level)
    edge_count -= 1  # discount the root node
    edge_count -= duplicate_node_count(levels)  # discount extraneous links
    return edge_count


def duplicate_node_count(levels: List[List[str]]) -> int:
    unique_node_names: List[str] = []
    for level in levels:
        for node in level:
            if node not in unique_node_names:
                unique_node_names.append(node)
    count = 0
    for name in unique_node_names:
        num_instances_of_name = 0
        for level in levels:
            for node in level:
                if name == node:
                    num_instances_of_name += 1
        count += num_instances_of_name - 1  # ignore the unique instance
    return count


def exists_in_higher_level(levels: List[List[str]], node: str) -> bool:
    for level in levels:
        if node in level:
            return True
    return False


def get_level_below(edge_string: str, current_level: List[str]) -> List[str]:
    edges = parse_edges(edge_string)[0]
    level: List[str] = []
    for potential_parent in current_level:
        if potential_parent in edges:
            for child in edges[potential_parent]:
                level.append(child)
    return level


def parse_edges(edge_string: str) -> (Dict[str, List[str]], Dict[str, List[str]]):
    edges: Dict[str, List[str]] = {}  # maps parent nodes to a list of child nodes
    for i in range(len(edge_string) - 1):
        if edge_string[i] in string.ascii_lowercase and edge_string[i + 1] in string.ascii_lowercase:
            if edge_string[i] not in edges:
                edges[edge_string[i]] = []
            edges[edge_string[i]].append(edge_string[i + 1])

    reverse_edges: Dict[str, List[str]] = {}  # maps child nodes to a list of its parents (hopefully only one parent)
    for i in range(len(edge_string) - 1):
        if edge_string[i] in string.ascii_lowercase and edge_string[i + 1] in string.ascii_lowercase:
            if edge_string[i + 1] not in reverse_edges:
                reverse_edges[edge_string[i + 1]] = []
            reverse_edges[edge_string[i + 1]].append(edge_string[i])

    return edges, reverse_edges


if __name__ == "__main__":
    import doctest

    doctest.testmod()

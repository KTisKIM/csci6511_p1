import numpy as np
from queue import PriorityQueue


def read_input_file(filename):
    """
    Parsing an input file from the user.
    """
    with open(filename, "r") as file:
        pitchers = list(map(int, file.readline().strip().split(",")))  # First line, Pitchers should be all integers before the GCD calculation.
        target_quantity = int(file.readline().strip())  # Second line

    return pitchers, target_quantity

def gcd_list(pitchers):
    """
    Calculating the GCD of a list of numbers.
    """
    return np.gcd.reduce(pitchers)  # Use GCD(Greatest Common Divisor) on the list of numbers(pitcher capacities)

def heuristic_score(state, pitchers, target_quantity):
    """
    Calculating the Heuristic(h) function: This is the 'lower bound' of steps required to meet the goal state.
    """
    biggest_pitcher = max(pitchers[:-1])  # Not including the "infinite" pitcher, and find the max value.
    remain_quantity = abs(target_quantity - state[-1])  # Remaining quantity to meet the target quantity

    if remain_quantity == 0:  # When remaining quantity is 0, it means it's on the goal state.
        return 0

    steps = remain_quantity // biggest_pitcher
    if remain_quantity % biggest_pitcher != 0:
        steps += 1

    return steps

def create_successors(state, pitchers):
    """
    Create successors for the state
    """
    successors = []
    infinite_pitcher_index = len(pitchers) - 1    # Not including the "infinite" pitcher

    for i in range(infinite_pitcher_index):
        # Filling Pitcher i
        if state[i] < pitchers[i]:
            new_state = list(state)
            new_state[i] = pitchers[i]
            successors.append(tuple(new_state))
        # Emptying Pitcher i into the infinite pitcher
        if state[i] > 0:
            new_state = list(state)
            new_state[infinite_pitcher_index] += new_state[i]  # Will increase the volume of the "Inifinite" pitcher depending on how much it emptied
            new_state[i] = 0
            successors.append(tuple(new_state))
        # Move water from another pitcher to another, not including the "Infinite" pitcher
        for j in range(infinite_pitcher_index):
            if i != j:
                new_state = list(state)
                move_amount = min(state[i], pitchers[j] - state[j])
                # Move water i -> j
                new_state[i] -= move_amount
                new_state[j] += move_amount
                successors.append(tuple(new_state))

    return successors

def a_star_search(pitchers, target_quantity):
    """
    A* Search Algorithm (Informed Search)
    """
    if min(pitchers) > target_quantity:  # Check if the target quantity is smaller than the smallest pitcher's capacity.
        return -1  # If the target quantity is the smallest, then return -1.

    # Appending the virtual "infinite" pitcher to the pitchers as stated in the instruction.
    pitchers_infinite = list(pitchers) + [np.inf]

    initial_state = tuple([0] * (len(pitchers) + 1))  # Add an additional zero(virtual space) for the "infinite" pitcher
    priority_queue = PriorityQueue()  # allows algorithms to always expand the node with the lowest f-score next.
    priority_queue.put((0, initial_state))
    total_cost = {initial_state: 0}

    while not priority_queue.empty():  # repeat this until the queue is empty
        _, current = priority_queue.get()
        if current[-1] == target_quantity:  # See if the "Infinite" pitcher has the target amount
            return total_cost[current]  # Return the cost(=number of steps)
        for next_state in create_successors(current, pitchers_infinite):
            new_cost = total_cost[current] + 1  # Each move is 1 step
            if next_state not in total_cost or new_cost < total_cost[next_state]:
                total_cost[next_state] = new_cost
                priority = new_cost + heuristic_score(next_state, pitchers_infinite, target_quantity)
                priority_queue.put((priority, next_state))

    return -1


if __name__ == "__main__":
    pitchers, target_quantity = read_input_file("P1_Option2_WaterPitcher/cat input1.txt")  # Change the input file if needed.
    # print(f"Pitchers: {pitchers}\nTarget Quantity: {target_quantity}")  # Check what the pitchers and target are.

    # Check the GCD for the pitchers without "infinite" capacity pitcher to see if it's solvable.
    if target_quantity % gcd_list(pitchers) != 0:
        print("-1")  # If there is NO path, then simply return -1.
    else:
        steps = a_star_search(pitchers, target_quantity)  # Use the A* Search function to calculate the number of steps.
        print(steps)  # Output is a single number which represents "the number of steps".

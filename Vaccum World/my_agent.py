"""
my_agent.py  --  YOUR CODE GOES HERE

Run it with:
    python my_agent.py              (start in A, both squares dirty)
    python my_agent.py --start B,1,0
    python my_agent.py --step       (press Enter to advance each step)
    python my_agent.py --all        (test all 8 starting states)

State / percept format: (agent_location, dirt_in_A, dirt_in_B)
    e.g. ("A", True, False)
"""

from vacuum_world import LEFT, RIGHT, SUCK, NOOP, main


# ---------------------------------------------------------------------------
# PART 1: The problem formulation (the five bullets from the textbook)
# ---------------------------------------------------------------------------
class VacuumProblem:
    def __init__(self, initial_state, goal):
        # TODO: store the initial state and the goal
        pass

    def actions(self, state):
        """Return the list of actions available in `state`."""
        raise NotImplementedError("TODO: actions")

    def result(self, state, action):
        """Transition model: return the NEW state after doing `action` in `state`.
        Remember the 'no effect' cases from the textbook."""
        raise NotImplementedError("TODO: result")

    def goal_test(self, state):
        """Return True if `state` satisfies the goal."""
        raise NotImplementedError("TODO: goal_test")

    def step_cost(self, state, action, next_state):
        raise NotImplementedError("TODO: step_cost")


# ---------------------------------------------------------------------------
# PART 2: Search
# ---------------------------------------------------------------------------
def search(problem):
    """Return a list of actions that gets from problem's initial state
    to a goal state, or None if there is no solution."""
    raise NotImplementedError("TODO: search")


# ---------------------------------------------------------------------------
# PART 3: The agent (translate the pseudocode box)
# ---------------------------------------------------------------------------
class SimpleProblemSolvingAgent:
    def __init__(self):
        # TODO: the four "static" variables.
        # Tip: name the plan `self.seq` and the visualizer will display it.
        pass

    def __call__(self, percept):
        # TODO: translate the pseudocode here, line by line.
        # Must return LEFT, RIGHT, SUCK, or NOOP (NOOP = "I'm done").
        return NOOP

    def update_state(self, state, percept):
        raise NotImplementedError("TODO: update_state")

    def formulate_goal(self, state):
        raise NotImplementedError("TODO: formulate_goal")

    def formulate_problem(self, state, goal):
        raise NotImplementedError("TODO: formulate_problem")

    def recommendation(self, seq, state):
        raise NotImplementedError("TODO: recommendation")

    def remainder(self, seq, state):
        raise NotImplementedError("TODO: remainder")


if __name__ == "__main__":
    main(SimpleProblemSolvingAgent)

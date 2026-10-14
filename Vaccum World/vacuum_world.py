"""
vacuum_world.py  --  the ENVIRONMENT + VISUALIZER 

The two-square vacuum world from Russell & Norvig, Ch. 2-3.

    +-------------+-------------+
    |      A      |      B      |
    |    [o_o]    |             |
    |   *DIRTY*   |    clean    |
    +-------------+-------------+

Percept / state format:  (agent_location, dirt_in_A, dirt_in_B)
    e.g. ("A", True, False) -> agent in A, A dirty, B clean

Your agent must be callable:   action = agent(percept)
and return one of: LEFT, RIGHT, SUCK, NOOP   (NOOP means "I'm done").

If your agent stores its plan in a field called `seq`, the visualizer
will display it so you can watch the plan shrink each step.
"""

import argparse
import os
import sys
import time

LEFT, RIGHT, SUCK, NOOP = "Left", "Right", "Suck", "NoOp"
VALID_ACTIONS = (LEFT, RIGHT, SUCK, NOOP)

if os.name == "nt":
    os.system("")  # enables ANSI escape codes on Windows terminals


# ---------------------------------------------------------------------------
# The environment (the "real world")
# ---------------------------------------------------------------------------
class VacuumEnvironment:
    def __init__(self, location="A", dirt_a=True, dirt_b=True):
        self.location = location
        self.dirt = {"A": dirt_a, "B": dirt_b}
        self.steps = 0

    def percept(self):
        return (self.location, self.dirt["A"], self.dirt["B"])

    def is_clean(self):
        return not self.dirt["A"] and not self.dirt["B"]

    def execute(self, action):
        if action == LEFT:
            self.location = "A"
        elif action == RIGHT:
            self.location = "B"
        elif action == SUCK:
            self.dirt[self.location] = False
        self.steps += 1


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------
CELL = 13
ROBOT = "[o_o]"


def _cell(text):
    return text.center(CELL)


def render(env, step, last_action, agent, message=""):
    if sys.stdout.isatty():
        print("\033[2J\033[H", end="")  # clear the screen

    border = "+" + "-" * CELL + "+" + "-" * CELL + "+"
    labels = "|" + _cell("A") + "|" + _cell("B") + "|"
    robots = "|" + "|".join(
        _cell(ROBOT if env.location == sq else "") for sq in "AB"
    ) + "|"
    dirt = "|" + "|".join(
        _cell("*DIRTY*" if env.dirt[sq] else "clean") for sq in "AB"
    ) + "|"

    print(f" Step {step}    Last action: {last_action or '-'}")
    print(" " + border)
    print(" " + labels)
    print(" " + robots)
    print(" " + dirt)
    print(" " + border)
    print(f" Percept: {env.percept()}")

    seq = getattr(agent, "seq", None)
    if seq is not None:
        print(f" Agent's remaining plan (seq): {list(seq)}")
    if message:
        print(f"\n {message}")
    print()


# ---------------------------------------------------------------------------
# Run loop: percept -> agent -> action -> environment, repeat
# ---------------------------------------------------------------------------
def run(agent, initial_state=("A", True, True), max_steps=20,
        delay=0.8, step_mode=False):
    env = VacuumEnvironment(*initial_state)
    render(env, 0, None, agent, f"Starting state: {initial_state}")
    _pause(delay, step_mode)

    for step in range(1, max_steps + 1):
        percept = env.percept()
        action = agent(percept)  # one call = one time step

        if action not in VALID_ACTIONS:
            render(env, step, action, agent,
                   f"ERROR: agent returned {action!r}. "
                   f"It must return one of {VALID_ACTIONS}.")
            return False

        if action == NOOP:
            if env.is_clean():
                msg = f"Agent stopped. GOAL REACHED in {env.steps} actions."
            else:
                msg = "Agent stopped (NoOp), but there is still dirt left!"
            render(env, step, action, agent, msg)
            return env.is_clean()

        env.execute(action)
        render(env, step, action, agent)
        _pause(delay, step_mode)

    render(env, max_steps, "-", agent,
           f"Stopped after {max_steps} steps without the agent returning NoOp.")
    return False


def _pause(delay, step_mode):
    if step_mode:
        input(" Press Enter for the next step...")
    else:
        time.sleep(delay)


ALL_STATES = [(loc, a, b) for loc in "AB"
              for a in (True, False) for b in (True, False)]


def main(agent_class):
    parser = argparse.ArgumentParser(description="Run an agent in the vacuum world.")
    parser.add_argument("--start", default="A,1,1",
                        help="starting state as LOC,DIRT_A,DIRT_B  e.g. B,1,0 (default A,1,1)")
    parser.add_argument("--all", action="store_true",
                        help="run all 8 possible starting states")
    parser.add_argument("--step", action="store_true",
                        help="press Enter to advance each step")
    parser.add_argument("--delay", type=float, default=0.8,
                        help="seconds between steps (default 0.8)")
    args = parser.parse_args()

    if args.all:
        starts = ALL_STATES
    else:
        loc, a, b = args.start.upper().split(",")
        starts = [(loc, a == "1", b == "1")]

    results = []
    for start in starts:
        agent = agent_class()  # fresh agent each run (resets static variables)
        results.append((start, run(agent, start, delay=args.delay,
                                   step_mode=args.step)))
        if args.all:
            time.sleep(args.delay)

    if len(results) > 1:
        print(" Summary:")
        for start, ok in results:
            print(f"   {start}: {'PASS' if ok else 'FAIL'}")

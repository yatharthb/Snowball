import simpy
import random

# Define the Snowball algorithm as a Process in simPy
class Snowball(object):
    def __init__(self, env, state, nodes):
        # Initialize the Process and store the environment instance, state, and nodes
        # some issue with Snowball class as a generator
        self.env = env
        self.state = state
        self.nodes = nodes
        print(state)
        print(nodes)
    def run(self):
    # Poll 3 random nodes and check if the majority have the same state as this node
     while True:
        poll_nodes = random.sample(self.nodes, 3)
        poll_states = [node.state for node in poll_nodes]
        print(poll_states)
        if poll_states.count(self.state) >= 2:
            # Change the state of this node to the state of the majority of the polled nodes
            self.state = max(set(poll_states), key=poll_states.count)
        else:
            # Keep the same state
            pass
        # Yield control to other processes (might not be needed)
        yield self.env.timeout(1)

# Create an instance of the Environment class
env = simpy.Environment()

# Create the state and nodes dictionaries
state = {"snowball1": "A", "snowball2": "A", "snowball3": "B", "snowball4": "B", "snowball5": "B"}
nodes = {"snowball1": ["snowball2", "snowball3", "snowball4", "snowball5"],
         "snowball2": ["snowball1", "snowball3", "snowball4", "snowball5"],
         "snowball3": ["snowball1", "snowball2", "snowball4", "snowball5"],
         "snowball4": ["snowball1", "snowball2", "snowball3", "snowball5"],
         "snowball5": ["snowball1", "snowball2", "snowball3", "snowball4"]}
# Create instances of the Snowball class
snowball1 = Snowball(env, state["snowball1"], nodes["snowball1"])
snowball2 = Snowball(env, state["snowball2"], nodes["snowball2"])
snowball3 = Snowball(env, state["snowball3"], nodes["snowball3"])
snowball4 = Snowball(env, state["snowball4"], nodes["snowball4"])
snowball5 = Snowball(env, state["snowball5"], nodes["snowball5"])

# Start the 5 Snowball algorithm processes concurrently
env.process(snowball1)
env.process(snowball2)
env.process(snowball3)
env.process(snowball4)
env.process(snowball5)

# Run the simulation until all the snowball instances have the same state
while len(set([state[node] for node in ["snowball1", "snowball2", "snowball3", "snowball4", "snowball5"]])) > 1:
    env.step()


#Print the final state of the algorithms
print(snowball1.state)
print(snowball2.state)
print(snowball3.state)
print(snowball4.state)
print(snowball5.state)

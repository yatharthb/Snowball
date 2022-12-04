import simpy
import random

# Define the Snowball algorithm as a Process in simPy
class Snowball(simpy.Process):
    def __init__(self, env, state, nodes):
        # Initialize the Process and store the environment instance, state, and nodes
        super().__init__(env, generator=self.run())
        self.state = state
        self.nodes = nodes
        
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
            yield self.env.timeout(0)

# Create an instance of the Environment class
env = simpy.Environment()

# Create 5 instances of the Snowball algorithm, 2 with state A and 3 with state B
snowball1 = Snowball(env, "A", [])
snowball2 = Snowball(env, "A", []) 
snowball3 = Snowball(env, "B", [])
snowball4 = Snowball(env, "B", [])
snowball5 = Snowball(env, "B", [])
#Add each Snowball algorithm instance to the list of nodes of the other instances
snowball1.nodes = [snowball2, snowball3, snowball4, snowball5] 

snowball2.nodes = [snowball1, snowball3, snowball4, snowball5] 

snowball3.nodes = [snowball1, snowball2, snowball4, snowball5] 

snowball4.nodes = [snowball1, snowball2, snowball3, snowball5] 

snowball5.nodes = [snowball1, snowball2, snowball3, snowball4] 
#Start the 5 Snowball algorithm processes concurrently 
env.process(snowball1)
env.process(snowball2)
env.process(snowball3)
env.process(snowball4)
env.process(snowball5)

#Run the simulation until all the algorithms have the same state
while len(set([node.state for node in [snowball1, snowball2, snowball3, snowball4, snowball5]])) > 1:
   env.step()

#Print the final state of the algorithms
print(snowball1.state)
print(snowball2.state)
print(snowball3.state)
print(snowball4.state)
print(snowball5.state)

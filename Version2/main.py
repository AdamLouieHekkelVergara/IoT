import simpy
from Version2.Network import Network

print("Dodag")


def main():
    NEW_MESSAGES = 5 # Total number of customers
    INTERVAL_MESSAGES = 10  # Generate new customers roughly every x seconds
    env = simpy.Environment()

    env = simpy.Environment()
    # initialize network with number of nodes placed on a grid:
    network = Network(env, 110)
    env.process(network.source(NEW_MESSAGES,INTERVAL_MESSAGES))
    env.run()

main()
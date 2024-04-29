import numpy as np
from callApi import *
import os

# Hyperparameters
alpha = 0.1  # Learning rate
gamma = 0.6  # Discount factor
epsilon = 0.8  # Exploration rate
episodes = 10000  # Number of episodes to run
teamId = "1399"
worldId = "1"
exitReward = 1000
filename = 'q-table.npy'
runTimes = 5  # run 5 times in a world
exit = (24, 24)

# Initialize the Q-table, arbitrarily assuming a nxn grid world
# Q_table = np.zeros((40, 40, 4))
actions = {0: 'N', 1: 'S', 2: 'E', 3: 'W'}  # action to index mapping


def choose_action(state, Q_table):

    if np.random.uniform(0, 1) < epsilon:
        return np.random.choice(list(actions.keys()))  # Explore
    else:
        print("State for indexing:", state)
        print("Shape of Q_table:", Q_table.shape)

        return np.argmax(Q_table[state])  # Exploit the best known action


def choose_quick_action_randomly(state):
    # W: -1,0   N: 0,+1  S: 0,-1  E:+1,0
    conditions = [
        (state[1] < exit[1], 0),
        (state[1] > exit[1], 1),
        (state[0] < exit[0], 2),
        (state[0] > exit[0], 3)
    ]

    # Randomize the order of the conditions
    random.shuffle(conditions)

    # Check each condition in the random order
    for condition, result in conditions:
        if condition:
            return result

    return np.random.choice(list(actions.keys()))


def learn(state, state2, reward, action):
    stateStr = ','.join(map(str, state))
    print("learning at position: " + stateStr + "   action:")
    print(action)

    print("Type and value of state:", type(state), state)
    print("Type and value of action:", type(action), action)
    print("Shape of Q_table:", Q_table.shape)

    predict = Q_table[state][action]
    if state2 == null:
        target = reward + gamma * exitReward
    else:
        target = reward + gamma * np.max(Q_table[state2])
    Q_table[state][action] += alpha * (target - predict)
    np.save(filename, Q_table)


def autoRun(startWorld: int, endWorld: int):
    # enter this world
    postAPI = POST()
    getAPI = GET()
    for world in range(startWorld, endWorld + 1):
        enterInfo = postAPI.enterWorld(str(world), teamId)
        print(enterInfo)
        # if fail, continue in this current world
        currentWorld, _ = getAPI.getLocation(teamId)
        # run {counter} times in a world
        counter = runTimes
        filename = "q-table" + str(currentWorld) + ".npy"

        while (counter > 0):  # run {counter} times in a world
            # Initialization
            # If the file is not found, we create a new table
            if os.path.exists(filename):
                # Load the Q-table if it exists
                Q_table = np.load(filename)
            else:
                # Create a new Q-table with all values initialized to zero
                Q_table = np.zeros((40, 40, 4), dtype = float)
                # Save the new Q-table to the file
                np.save(filename, Q_table)
            # Main loop
            for episode in range(episodes):
                # getAPI = GET()
                _, state = getAPI.getLocation(teamId)  # Get initial state
                print(state)
                runId = getAPI.getRuns(teamId, 1)["runs"][0]["runId"]

                total_reward = 0
                done = False

                # postAPI = POST()
                while not done:
                    action = choose_action(state, Q_table)
                    moveJson = postAPI.makeMove(teamId, actions[action], str(currentWorld))
                    print(moveJson)
                    reward = moveJson["reward"]
                    scoreIncrement = moveJson["scoreIncrement"]
                    _, state2 = getAPI.getLocation(teamId)
                    learn(state, state2, reward, action, Q_table, filename)  # Update Q-values
                    if state2 == null:
                        total_reward = getAPI.getRuns(teamId, 1)["runs"][0]["score"]
                        break

                    state = state2
                    total_reward = getAPI.getRuns(teamId, 1)["runs"][0]["score"]

                    if scoreIncrement == 0:
                        done = True
                        break

                print(f"Episode {episode + 1}: total reward -> {total_reward}")

            # After training save your model or Q-table, here we are printing the Q-table
            print(Q_table)
            # save the QTable
            # np.save(filename, Q_table)
            counter -=1


if __name__ == "__main__":
    # Initialization
    Q_table = np.load(filename)
    # Main loop
    for episode in range(episodes):
        getAPI = GET()
        postAPI = POST()
        state = getAPI.getLocation("1399")[1]  # Get initial state
        print(state)
        if not state:
            # if you want the program never stop, # the 'break' below
            break
            postAPI.enterWorld(worldId, teamId)
            state = getAPI.getLocation("1399")[1]
        runId = getAPI.getRuns(teamId, 1)["runs"][0]["runId"]

        total_reward = 0
        done = False

        while not done:
            # action = choose_action(state)
            action = choose_quick_action_randomly(state)
            moveJson = postAPI.makeMove(teamId, actions[action], worldId)
            print(moveJson)
            reward = moveJson["reward"]
            scoreIncrement = moveJson["scoreIncrement"]
            state2 = getAPI.getLocation("1399")[1]
            learn(state, state2, reward, action)  # Update Q-values
            if state2 == null:
                total_reward = getAPI.getRuns(teamId, 1)["runs"][0]["score"]
                break

            state = state2
            total_reward = getAPI.getRuns(teamId, 1)["runs"][0]["score"]

            if scoreIncrement == 0:
                done = True
                break

        print(f"Episode {episode + 1}: total reward -> {total_reward}")

    # After training save your model or Q-table, here we are printing the Q-table
    print(Q_table)

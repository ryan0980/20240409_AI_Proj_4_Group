import numpy as np
from callApi import *
import os

# Hyperparameters
alpha = 0.1  # Learning rate
gamma = 0.6  # Discount factor
epsilon = 0.8  # Exploration rate
episodes = 10000  # Number of episodes to run
teamId = "1399"
worldId = "4"
exitReward = 1000
filename = 'q-table4.npy'
runTimes = 5  # run 5 times in a world
exit = (39, 39)

# Initialize the Q-table, arbitrarily assuming a nxn grid world
# Q_table = np.zeros((40, 40, 4))
actions = {0: 'N', 1: 'S', 2: 'E', 3: 'W'}  # action to index mapping


def choose_action(state):
    if np.random.uniform(0, 1) < epsilon:
        return np.random.choice(list(actions.keys()))  # Explore
    else:
        return np.argmax(Q_table[state])  # Exploit the best known action


def choose_quick_action(state):
    # W: -1,0   N: 0,+1  S: 0,-1  E:+1,0
    if state[0] < exit[0]:
        return 2
    if state[0] > exit[0]:
        return 3
    if state[1] < exit[1]:
        return 0
    if state[1] > exit[1]:
        return 1
    return np.random.choice(list(actions.keys()))


def learn(state, state2, reward, action):
    stateStr = ','.join(map(str, state))
    print("learning at position: " + stateStr + "   action:")
    print(action)
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
                Q_table = np.zeros((40, 40, 4))
                # Save the new Q-table to the file
                np.save(filename, Q_table)
            Q_table = np.load(filename)
            # Main loop
            for episode in range(episodes):
                # getAPI = GET()
                state = getAPI.getLocation(teamId)  # Get initial state
                print(state)
                runId = getAPI.getRuns(teamId, 1)["runs"][0]["runId"]

                total_reward = 0
                done = False

                # postAPI = POST()
                while not done:
                    action = choose_action(state)
                    moveJson = postAPI.makeMove(teamId, actions[action], worldId)
                    print(moveJson)
                    reward = moveJson["reward"]
                    scoreIncrement = moveJson["scoreIncrement"]
                    _, state2 = getAPI.getLocation(teamId)
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
            # save the QTable
            np.save(filename, Q_table)


if __name__ == "__main__":
    # Initialization
    Q_table = np.load(filename)
    # Main loop
    for episode in range(episodes):
        getAPI = GET()
        state = getAPI.getLocation("1399")[1]  # Get initial state
        print(state)
        if state == null:
            break
        runId = getAPI.getRuns(teamId, 1)["runs"][0]["runId"]

        total_reward = 0
        done = False

        postAPI = POST()
        while not done:
            # action = choose_action(state)
            action = choose_quick_action(state)
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

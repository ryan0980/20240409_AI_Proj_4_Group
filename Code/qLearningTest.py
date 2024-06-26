import numpy as np
from callApi import *
import os
import random

# Hyperparameters
alpha = 0.1  # Learning rate
gamma = 0.6  # Discount factor
epsilon = 0.8  # Exploration rate
episodes = 10000  # Number of episodes to run
teamId = "1399"
worldId = "7"
filename = 'q-table7.npy'
runTimes = 5  # run 5 times in a world
# exit = (3, 0)
badExits = {}

# Initialize the Q-table, arbitrarily assuming a nxn grid world
# Q_table = np.zeros((40, 40, 4))
actions = {0: 'N', 1: 'S', 2: 'E', 3: 'W'}  # action to index mapping
actionEffect = {0: (0, 1), 1: (0, -1), 2: (1, 0), 3: (-1, 0)}
# actionEffect = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}


def choose_action(state, Q_table):
    if np.random.uniform(0, 1) < epsilon:
        return np.random.choice(list(actions.keys()))  # Explore
    else:
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


def meetGhost(currentstate, action):
    stateStr = ','.join(map(str, currentstate))
    actionStr = ','.join(map(str, actionEffect[action]))
    print("meetGhostTest at position: " + stateStr + "   action:" + actionStr)
    for badExit in badExits:
        if map(sum, zip(actionEffect[action], currentstate)) == badExit:
            return True
    return False


def learn(state, state2, reward, action):
    stateStr = ','.join(map(str, state))
    print("learning at position: " + stateStr + "   action:")
    print(action)

    predict = Q_table[state][action]
    if state2 == null:
        target = reward + gamma * reward
    else:
        target = reward + gamma * np.max(Q_table[state2])
    Q_table[state][action] += alpha * (target - predict)
    np.save(filename, Q_table)



if __name__ == "__main__":
    # Initialization
    Q_table = np.load(filename)
    counter = 0
    scoreIncrement = 0
    # Main loop
    with open('logWorld.txt', 'a') as log_file:
        for episode in range(episodes):
            getAPI = GET()
            postAPI = POST()
            state = getAPI.getLocation(teamId)[1]  # Get initial state
            print(state)
            if not state:
                # if you want the program never stop, # the 'break' below
                # break
            # try to enter a world
                postAPI.enterWorld(worldId, teamId)
                state = getAPI.getLocation(teamId)[1]
            runId = getAPI.getRuns(teamId, 1)["runs"][0]["runId"]

            total_reward = 0
            done = False

            while not done:
                action = choose_action(state, Q_table)
                while meetGhost(state, action):
                    action = choose_action(state, Q_table)

                # action = choose_quick_action_randomly(state)
                # if counter >= 90 and scoreIncrement == 0:
                #    action = choose_quick_action_randomly(state)

                # if counter >= 90 and scoreIncrement == 0:
                #     action = choose_quick_action_randomly(state)
                # if counter <= 40:
                #     action = 2
                # if 40 < counter < 90:
                #     action = 3
                # if counter >= 90 and scoreIncrement != 0:
                #     counter = 0
                #     break
                counter += 1
                print("action:"+actions[action])
                moveJson = postAPI.makeMove(teamId, actions[action], worldId)
                print(moveJson)
                log_file.write(str(moveJson)+'\n')
                reward = moveJson["reward"]
                scoreIncrement = moveJson["scoreIncrement"]
                state2 = getAPI.getLocation("1399")[1]
                learn(state, state2, reward, action)  # Update Q-values
                if not state2:
                    total_reward = getAPI.getRuns(teamId, 1)["runs"][0]["score"]
                    break

                state = state2
                total_reward = getAPI.getRuns(teamId, 1)["runs"][0]["score"]

                if scoreIncrement == 0:
                    done = True
                    break

            print(f"Episode {episode + 1}: total reward -> {total_reward}")
            # log_file.write(f"Episode {episode + 1}: total reward -> {total_reward}")

    # After training save your model or Q-table, here we are printing the Q-table
        print(Q_table)
        # log_file.write(str(Q_table))

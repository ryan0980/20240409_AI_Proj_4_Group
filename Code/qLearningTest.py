import numpy as np
from callApi import *
import os

# Hyperparameters
alpha = 0.1  # Learning rate
gamma = 0.6  # Discount factor
epsilon = 0.8  # Exploration rate
episodes = 10000  # Number of episodes to run
teamId = "1413"
worldId = "2"
exitReward = 1000
# filename = 'q-table2.npy'
runTimes = 5  # run 5 times in a world
exit = (17, 11)

# Initialize the Q-table, arbitrarily assuming a nxn grid world
# Q_table = np.zeros((40, 40, 4))
actions = {0: 'N', 1: 'S', 2: 'E', 3: 'W'}  # action to index mapping


def choose_action(state, Q_table):
    
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


def learn(state, state2, reward, action, Q_table, filename):
    stateStr = ','.join(map(str, state))
    print("learning at position: " + stateStr + "   action:")
    # print(action)
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
    with open('log.txt', 'a') as log_file:
        for world in range(startWorld, endWorld + 1):
            enterInfo = postAPI.enterWorld(str(world), teamId)
            # if fail, continue in this current world
            currentWorld, _ = getAPI.getLocation(teamId)
            # run {counter} times in a world
            counter = runTimes
            filename = "q-table" + str(currentWorld) + ".npy"
            exitFound = False
            while counter > 0 and exitFound == False:  # run {counter} times in a world
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
                    ## if an exit is found
                    if state ==null:
                        exitFound =True
                        break
                    
                    runId = getAPI.getRuns(teamId, 1)["runs"][0]["runId"]

                    total_reward = 0
                    done = False
                    # postAPI = POST()
                    while not done and exitFound == False:
                        action = choose_action(state, Q_table)
                        moveJson = postAPI.makeMove(teamId, actions[action], str(currentWorld))
                        print(moveJson)
                        log_file.write(str(moveJson) + '\n')
                        reward = moveJson["reward"]
                        scoreIncrement = moveJson["scoreIncrement"]
                        _, state2 = getAPI.getLocation(teamId)
                        if state2 == null:
                            exitFound =True
                            break
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

            
                counter -=1


if __name__ == "__main__":
    # Initialization
    autoRun(6,10)
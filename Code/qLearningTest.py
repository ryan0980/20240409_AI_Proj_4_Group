import numpy as np
from callApi import *

# Hyperparameters
alpha = 0.1  # Learning rate
gamma = 0.6  # Discount factor
epsilon = 0.8  # Exploration rate
episodes = 10000  # Number of episodes to run
teamId = "1399"
worldId = "1"
filename = 'q-table.npy'

# Initialize the Q-table, arbitrarily assuming a nxn grid world
# Q_table = np.zeros((40, 40, 4))
actions = {0: 'N', 1: 'S', 2: 'E', 3: 'W'}  # action to index mapping


def choose_action(state):
    if np.random.uniform(0, 1) < epsilon:
        return np.random.choice(list(actions.keys()))  # Explore
    else:
        return np.argmax(Q_table[state])  # Exploit the best known action


def learn(state, state2, reward, action):
    stateStr = ','.join(map(str, state))
    print("learning at position: " + stateStr + "   action:")
    print(action)
    predict = Q_table[state][action]
    if state2 == null:
        target = reward + gamma * 10000
    else:
        target = reward + gamma * np.max(Q_table[state2])
    Q_table[state][action] += alpha * (target - predict)
    np.save(filename, Q_table)


if __name__ == "__main__":
    Q_table = np.load(filename)
    # Main loop
    for episode in range(episodes):
        getAPI = GET()
        state = getAPI.getLocation("1399")  # Get initial state
        print(state)
        runId = getAPI.getRuns(teamId, 1)["runs"][0]["runId"]

        total_reward = 0
        done = False

        postAPI = POST()
        while not done:
            action = choose_action(state)
            moveJson = postAPI.makeMove(teamId, actions[action], worldId)
            print(moveJson)
            reward = moveJson["reward"]
            scoreIncrement = moveJson["scoreIncrement"]
            state2 = getAPI.getLocation("1399")
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

import numpy as np
from callApi import *

# Hyperparameters
alpha = 0.1  # Learning rate
gamma = 0.6  # Discount factor
epsilon = 0.1  # Exploration rate
episodes = 10000  # Number of episodes to run
teamId = "1399"
worldId = "1"

# Initialize the Q-table, arbitrarily assuming a nxn grid world
Q_table = np.zeros((100, 100, 4))
actions = {0: 'N', 1: 'S', 2: 'E', 3: 'W'}  # action to index mapping


def choose_action(state):
    if np.random.uniform(0, 1) < epsilon:
        return np.random.choice(list(actions.keys()))  # Explore
    else:
        return np.argmax(Q_table[state])  # Exploit the best known action


def learn(state, state2, reward, action):
    stateStr = ','.join(map(str, state))
    print("state: " + stateStr)
    print(action)
    predict = Q_table[state][action]
    target = reward + gamma * np.max(Q_table[state2])
    Q_table[state][action] += alpha * (target - predict)


if __name__ == "__main__":
    print(Q_table[1, 12][0])

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

            state = state2
            total_reward += scoreIncrement

            if getAPI.getRuns(teamId, 1)["runs"][0]["runId"] != runId:
                done = True

        print(f"Episode {episode + 1}: total reward -> {total_reward}")

    # After training save your model or Q-table, here we are printing the Q-table
    print(Q_table)

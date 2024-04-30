import numpy as np
import os
from callApi import *

class QLearningAgent:
    def __init__(self, team_id):
        self.teamId = team_id
        self.get_api = GET()
        self.post_api = POST()
        self.world_id = self.get_current_world()
        self.table_folder = 'table'
        self.filename = os.path.join(self.table_folder, f'q_table_{self.world_id}.npy')
        self.actions = {0: 'N', 1: 'S', 2: 'E', 3: 'W'}
        self.epsilon = 0.8  # Exploration rate
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.6  # Discount factor
        self.q_table = self.load_q_table()

    def get_current_world(self):
        return 2
        # You need to implement this method to set the current world id
        # get_api = GET()

        # # Call the getLocation method and unpack its results
        # current_world, additional_info = get_api.getLocation('1414')
        # print(f"Current World: {current_world}")
        # print(f"Additional Info: {additional_info}")
        # return current_world

    def load_q_table(self):
        if not os.path.exists(self.filename):
            return np.zeros((40, 40, 4))  # Assuming a 40x40 grid world
        return np.load(self.filename)

    def save_q_table(self):
        np.save(self.filename, self.q_table)

    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(list(self.actions.keys()))  # Explore
        else:
            return np.argmax(self.q_table[state])  # Exploit

    def learn(self, state, action, reward, next_state):
        predict = self.q_table[state][action]
        target = reward + self.gamma * (np.max(self.q_table[next_state]) if next_state is not None else 10000)
        self.q_table[state][action] += self.alpha * (target - predict)
        self.save_q_table()

    def run_episode(self):
        state = self.get_api.getLocation(self.teamId)
        total_reward = 0
        done = False

        while not done:
            action = self.choose_action(state)
            move_json = self.post_api.makeMove(self.teamId, self.actions[action], self.world_id)
            reward = move_json["reward"]
            score_increment = move_json["score_increment"]
            next_state = self.get_api.getLocation(self.teamId)

            self.learn(state, action, reward, next_state)

            state = next_state if next_state is not None else state
            total_reward += reward

            if score_increment == 0 or next_state is None:
                done = True

        return total_reward

    def train(self, episodes):
        for episode in range(episodes):
            total_reward = self.run_episode()
            print(f"Episode {episode + 1}: total reward -> {total_reward}")

if __name__ == "__main__":
    agent = QLearningAgent(team_id="1414")
    #agent.train(episodes=10000)
    post_test_results=GET()
    current_world, additional_info = post_test_results.getLocation('1414')
    post=POST()
    post.enterWorld('2','1414')
    print(current_world)



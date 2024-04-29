import numpy as np
from callApi import GET, POST

class QLearningAgent:
    def __init__(self, team_id):
        self.team_id = team_id
        self.get_api = GET()
        self.post_api = POST()
        self.world_id = self.get_current_world()
        self.filename = f'q_table_{self.world_id}.npy'
        self.actions = {0: 'N', 1: 'S', 2: 'E', 3: 'W'}
        self.epsilon = 0.8  # Exploration rate
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.6  # Discount factor
        self.q_table = self.load_q_table()

    def get_current_world(self):
        location_response = self.get_api.getLocation(self.team_id)
        if location_response is None:
            self.post_api.enterWorld('defaultWorldId', self.team_id)  # Enter a default world if none is currently active
            location_response = self.get_api.getLocation(self.team_id)
        return location_response['worldId']

    def load_q_table(self):
        try:
            return np.load(self.filename)
        except FileNotFoundError:
            return np.zeros((40, 40, 4))  # Assume a 40x40 grid world for the Q-table

    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(list(self.actions.keys()))
        else:
            return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        prediction = self.q_table[state][action]
        target = reward + self.gamma * (0 if next_state is None else np.max(self.q_table[next_state]))
        self.q_table[state][action] += self.alpha * (target - prediction)
        np.save(self.filename, self.q_table)

    def run_episode(self):
        state = self.get_api.getLocation(self.team_id)
        done = False
        while not done:
            action = self.choose_action(state)
            move_result = self.post_api.makeMove(self.team_id, self.actions[action], self.world_id)
            reward = move_result['reward']
            next_state = self.get_api.getLocation(self.team_id)
            self.update_q_table(state, action, reward, next_state)
            if next_state is None or move_result.get('scoreIncrement', 0) == 0:
                done = True
            state = next_state

    def train(self, episodes):
        for episode in range(episodes):
            self.run_episode()
            print(f"Episode {episode + 1} completed")
        print(self.q_table)

if __name__ == "__main__":
    agent = QLearningAgent("1399")
    agent.train(10000)

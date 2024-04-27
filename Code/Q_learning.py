#Each world is 40 x 40

import numpy as np

class MultiWorldGrid:
    def __init__(self, num_worlds=10, grid_size=(40, 40), num_actions=4):
        # Initialize a 4D Q-table
        self.q_table = np.zeros((num_worlds, grid_size[0], grid_size[1], num_actions))

    def update_q_value(self, world_id, x, y, action, reward, next_world_id, next_x, next_y, alpha=0.1, gamma=0.9):
        # Future rewards from the next state in the specified world
        future_rewards = np.max(self.q_table[next_world_id, next_x, next_y])
        # Update Q-value for the current world, state, and action
        self.q_table[world_id, x, y, action] += alpha * (reward + gamma * future_rewards - self.q_table[world_id, x, y, action])

    def choose_action(self, world_id, x, y, epsilon=0.1):
        # Epsilon-greedy policy for action selection
        if np.random.random() < epsilon:
            return np.random.randint(4)  # Random action
        else:
            return np.argmax(self.q_table[world_id, x, y])  # Best action based on current Q-values

    def best_action(self, world_id, x, y):
        # Return the best action from the current state
        return np.argmax(self.q_table[world_id, x, y])

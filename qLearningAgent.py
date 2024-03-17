import numpy as np
import time

# Define the high latency system environment
class HighLatencyEnv:
    def __init__(self):
        self.latency = 5  # Default latency
        self.action_space = [0, 1]  # Actions: [do nothing, optimize latency]

    def step(self, action):
        if action == 1:  # Optimize latency
            self.latency -= 1
            if self.latency < 1:
                self.latency = 1
        time.sleep(self.latency)  # Simulate latency
        return self.latency, 0  # Return current latency and reward (0 for now)

    def reset(self):
        self.latency = 5
        return self.latency

# Q-learning agent
class QLearningAgent:
    def __init__(self, action_space):
        self.action_space = action_space
        self.q_table = np.zeros((1, len(action_space)))  # Q-table

    def choose_action(self, state, epsilon=0.1):
        if np.random.uniform(0, 1) < epsilon:
            return np.random.choice(self.action_space)
        else:
            return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state, alpha=0.1, gamma=0.95):
        next_max = np.max(self.q_table[next_state])
        td_target = reward + gamma * next_max
        td_error = td_target - self.q_table[state, action]
        self.q_table[state, action] += alpha * td_error

# Train the agent
def train_agent(env, agent, episodes=1000):
    for episode in range(episodes):
        state = env.reset()
        done = False
        while not done:
            action = agent.choose_action(state)
            next_state, reward = env.step(action)
            agent.update_q_table(state, action, reward, next_state)
            state = next_state

# Test the agent
def test_agent(env, agent, episodes=10):
    for episode in range(episodes):
        state = env.reset()
        done = False
        while not done:
            action = agent.choose_action(state, epsilon=0)  # Disable exploration and stop hilling climbing
            next_state, _ = env.step(action)
            state = next_state

# test driver
if __name__ == "__main__":
    env = HighLatencyEnv()
    agent = QLearningAgent(env.action_space)
    train_agent(env, agent)
    test_agent(env, agent)

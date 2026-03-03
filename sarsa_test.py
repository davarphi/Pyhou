import gymnasium as gym
import numpy as np
import random

env = gym.make("Taxi-v3")

alpha = 0.9 # Learning rate 1-alpha
gamma = 0.95 # Discount rate
epsilon = 1.0 # Probability of exploration
epsilon_decay = 0.999 # Decay of probability of exploration
min_epsilon = 0.01 # SO that exploration can always be chosen
num_episodes = 15000 # Episode untuk training
max_steps = 100 # Maksa berhenti agar tidak lama

q_table = np.zeros((env.observation_space.n, env.action_space.n))

def choose_action(state):
    if random.uniform(0, 1) < epsilon:
        return env.action_space.sample()
    else:
        return np.argmax(q_table[state, :])

# Training process
print("Begin training")
for episodes in range(num_episodes):
    state, _ = env.reset()
    
    done = False

    action = choose_action(state)

    for step in range(max_steps):
        next_state, reward, done, truncated, info = env.step(action)

        old_value = q_table[state, action]
        next_action = choose_action(next_state)

        q_table[state, action] = (1-alpha)*old_value + alpha*(reward + q_table[next_state, next_action] * gamma)
        state = next_state
        action = next_action

        if done or truncated:
            break
    
    epsilon = max(epsilon*epsilon_decay, min_epsilon)
    if (episodes % 1000 == 0):
        print("Episode ", episodes, "reached")


env = gym.make("Taxi-v3", render_mode = "human")

print("Begin testing")
for episode in range(5):
    state, _ = env.reset()

    done = False

    print("Episode : ", episode)

    for steps in range(max_steps):
        env.render()
        action = np.argmax(q_table[state, :])
        next_state, reward, done, truncated, info = env.step(action)
        state = next_state

        if done:
            env.render()
            print("Finished episode ", episode, "with reward ", reward)
            break
    
    else:
        print("Task failed.")


env.close()





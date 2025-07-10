import gymnasium as gym


if __name__ == "__main__":
    env = gym.make("CartPole-v1")
    total_reward = 0.0
    total_steps = 0
    obs, _ = env.reset()

    print("First observation: " + str(obs))

    while True:
        action = env.action_space.sample()
        obs, reward, is_done, is_trunc, _ = env.step(action)
        print(f"Observation: {obs}, Reward: {reward}, Done: {is_done}, Truncated: {is_trunc}")
        
        total_reward += reward
        total_steps += 1
        if is_done:
            break

    print("Episode done in %d steps, total reward %.2f" % (total_steps, total_reward))

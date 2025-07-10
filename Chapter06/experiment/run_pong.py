import sys
import termios
import tty

import gymnasium as gym
import matplotlib.pyplot as plt

import ale_py

def getch():
    """Get a single character from stdin without pressing Enter"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return char


def render_frame(env: gym.Env):
    frame = env.render()
    plt.imshow(frame)
    plt.axis('off')
    plt.show(block=False)


def main() -> None:
    gym.register_envs(ale_py)
    env = gym.make("PongNoFrameskip-v4", render_mode="rgb_array")
    print(env.action_space)
    print(env.observation_space)

    env.reset()
    print(env.render())

    env.close()


if __name__ == "__main__":
    main()

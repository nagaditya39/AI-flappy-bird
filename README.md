# Flappy Bird AI with NEAT

This is a Pygame-based implementation of the classic Flappy Bird game, featuring an AI model trained using the NEAT (NeuroEvolution of Augmenting Topologies) genetic algorithm. The AI learns optimal bird control to navigate past pipes by iteratively evolving over generations, refining gameplay strategies along the way.

## Overview

The game involves the familiar mechanics of Flappy Bird where the player controls a bird, guiding it through a series of pipes without collision. The AI model, powered by NEAT, is trained to autonomously control the bird's movements, gradually improving its performance through successive generations.

![flappy](flappy.gif)

## Installation

1. Clone the repository:

```
git clone https://github.com/nagaditya39/AI-flappy-bird.git
```

2. Install dependencies:

```
pip install pygame
pip install neat-python
```

3. Run the game:

```
python flappy.py
```

## How to Play

- The AI model automatically controls the bird's movements, aiming to achieve the highest score possible.


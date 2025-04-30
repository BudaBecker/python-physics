# Physics in Python (No Physics Library!)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Libraries](https://img.shields.io/badge/Libraries-Math%2C%20NumPy%2C%20Pygame-orange.svg)
![Coffee Level](https://img.shields.io/badge/Coffee-A%20Lot-brown.svg)
![Static Badge](https://img.shields.io/badge/Lines-1800%2B-darkgreen)

## Overview

This repository contains Python scripts demonstrating fundamental physics concepts through simulations. The unique aspect of this project is the **absence of dedicated physics libraries**. Instead, all calculations and simulations are built from scratch using Python's built-in `math` module, the numerical power of `NumPy`, and the visualization capabilities of `Pygame`.

This approach offers a deeper understanding of the underlying physics principles and the mathematical implementations involved in creating simulations. It's a testament to the fact that with a bit of mathematical know-how and a lot of coffee, you can bring the laws of nature to life on your screen!

## Features

This repository currently showcases simulations of:

* **Bouncy Balls:** Demonstrates the trajectory of objects under gravity and elastic collisions, including adjustable launch angles and velocities.
* **Slingshot Effect:** Visualizes the gravitational slingshot effect.
* **Simple Pendulum:** Implements a pendulum with or without air friction.
* **Spring Pendulum:** Implements a simple elastic pendulum.
* **Double Pendulum/Double Elastic Pendulum:** Visualy demonstrates the chaos theory with double pendulums.
* **The Three-Body Problem:** Simulates the chaotic motion of three celestial bodies that interact with each other through gravitational forces.
   * Includes a folder (`periodic_solutions_3BP`) with a few periodic solutions.
* **Pi Colliding Blocks:** This problem illustrates that elastic collisions in classical mechanics are arithmetic in nature, as revealed through this method to compute Pi's digits.
   * This problem became very famous after 3blue1brown's video.
* **Raytracing:** Simulates "basic" ray tracing principles.

## Getting Started

**Steps to run a simulation:**

1.  Clone this repository to your local machine:
    ```bash
    git clone https://github.com/BudaBecker/python-physics.git
    cd python-physics
    ```
2.  Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```
2.  Navigate to the directory of the specific simulation you want to run (e.g., `bouncy_balls`).

3.  Execute the main Python script:
    ```bash
    python bouncy_balls.py
    ```

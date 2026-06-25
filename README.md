# Chua's Circuit Simulator 
A Python project that simulates **Chua's Circuit**—the simplest electronic circuit that creates true mathematical chaos.

This project builds a simulation engine from scratch using Python to calculate, plot, and animate how chaos develops over time.

## What is this project about?
In physics and engineering, some systems are **chaotic**. This doesn't mean they are completely random; it means they are incredibly sensitive. If you change the starting point by even a microscopic amount, the system will end up in a completely different place over time. This is also known as the **Butterfly Effect**.

Because the circuit contains a special non-linear component (Chua's Diode), we cannot solve its equations using basic algebra. We have to use a programming algorithm called **RK4 (4th-order Runge-Kutta)** to guess the circuit's behavior step-by-step.

---

## Features
* **Built from Scratch:** The physics solver (RK4) is written manually without using heavy simulation libraries.
* **Visualizes Chaos:** Plots the famous **Double Scroll Attractor** in both 2D and 3D.
* **Stability Test:** Shows what happens if your simulation math step size ($h$) is too large (the math breaks down!).
* **The Butterfly Effect:** Simulates two identical circuits with a tiny starting difference of just $0.00001$ to show how quickly they drift apart.
* **Lyapunov Distance Plot:** Tracks the Euclidean distance between the two trajectories over time, making exponential divergence visible.
* **3D Live Animation:** A standalone script that lets you watch the chaotic trajectory draw itself in real-time.

---

## Project Structure
```text
├── codes/
│   ├── main.py    
│   └── animation.py    
├── plots/             
├── animation/
├── README.md                 
└── requirements.txt          
```

---

## The Math (briefly)
Chua's Circuit is governed by three coupled differential equations:

$$\frac{dx}{dt} = \alpha \left[ y - x - f(x) \right]$$

$$\frac{dy}{dt} = x - y + z$$

$$\frac{dz}{dt} = -\beta y$$

Where $f(x)$ is the piecewise-linear characteristic of Chua's Diode:

$$f(x) = m_1 x + \frac{1}{2}(m_0 - m_1)(|x+1| - |x-1|)$$

The standard parameters used in this simulation are:

| Parameter | Value |
|-----------|-------|
| α | 9.35 |
| β | 14.79 |
| m₀ | −1.14 |
| m₁ | −0.71 |

---

## How to Run

**1. Clone the repository**
```bash
git clone https://github.com/your-username/chuas-circuit-simulation.git
cd chuas-circuit-simulation
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the main simulation** (saves all plots to the `plots/` folder)
```bash
python src/simulation.py
```

**4. Run the live 3D animation** (optional)
```bash
python src/animation.py
```

---

## Output Plots

| File | Description |
|------|-------------|
| `01_variables_vs_time.png` | Time-series of x(t), y(t), z(t) over the first 30 seconds |
| `02_2d_phase_portraits.png` | Phase portraits in the X–Y and X–Z planes |
| `03_numerical_stability.png` | Comparison of stable (h=0.01) vs unstable (h=0.1) step sizes |
| `04_parameter_influence.png` | Chaotic (α=9.35) vs periodic (α=8.0) attractor side by side |
| `05_3d_double_scroll.png` | The iconic Double Scroll Attractor in 3D |
| `06_sensitivity_comparison.png` | Two trajectories diverging from near-identical starting points |
| `07_lyapunov_distance.png` | Euclidean distance between the two trajectories (log scale) |

---

## Requirements
* Python 3.8+
* NumPy
* Matplotlib
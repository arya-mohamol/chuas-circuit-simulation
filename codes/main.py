import numpy as np
import matplotlib.pyplot as plt

alpha = 9.35
beta = 14.79
m0 = -1.14
m1 = -0.71

def f(x, m1, m0):
    return (m1 * x) + 0.5 * (m0 - m1) * (np.abs(x + 1) - np.abs(x - 1))

def chua(vars, alpha, beta, f_value):
    x, y, z = vars
    dxdt = alpha * (y - x - f_value)
    dydt = x - y + z
    dzdt = (-1) * beta * y
    return np.array([dxdt, dydt, dzdt])

def rk4(f_system, t, X, h):
    k1 = f_system(t, X)
    k2 = f_system(t + h/2, X + (h/2) * k1)
    k3 = f_system(t + h/2, X + (h/2) * k2)
    k4 = f_system(t + h, X + h * k3)
    return X + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)

def run_simulation(X_init, t_end, h, alpha_val=alpha):
    steps = int(t_end / h)
    history = np.zeros((steps + 1, 4))
    
    t = 0.0
    X = np.array(X_init, dtype=float)
    history[0] = [t, X[0], X[1], X[2]]
    
    chua_adapter = lambda time, state: chua(state, alpha_val, beta, f(state[0], m1, m0))    
    for i in range(1, steps + 1):
        X = rk4(chua_adapter, t, X, h)
        t += h
        history[i] = [t, X[0], X[1], X[2]]
        
    return history

if __name__ == "__main__":
    init_cond = [0.1, 0.1, -0.1]
    h_stable = 0.01
    
    # 1
    base_data = run_simulation(init_cond, t_end=100.0, h=h_stable)
    t_val, x_val, y_val, z_val = base_data[:, 0], base_data[:, 1], base_data[:, 2], base_data[:, 3]
    
    # 2
    h_unstable = 0.1
    unstable_data = run_simulation(init_cond, t_end=15.0, h=h_unstable)
    
    # 3
    alpha_periodic = 8.0
    periodic_data = run_simulation(init_cond, t_end=60.0, h=h_stable, alpha_val=alpha_periodic)
    
    # 4
    perturbed_cond = [init_cond[0] + 1e-5, init_cond[1], init_cond[2]]
    nominal_path = run_simulation(init_cond, t_end=60.0, h=h_stable, alpha_val=alpha)
    perturbed_path = run_simulation(perturbed_cond, t_end=60.0, h=h_stable, alpha_val=alpha)
    
    t_s = nominal_path[:, 0]
    distance = np.sqrt((nominal_path[:, 1] - perturbed_path[:, 1])**2 + (nominal_path[:, 2] - perturbed_path[:, 2])**2 + (nominal_path[:, 3] - perturbed_path[:, 3])**2)

    # 1
    plt.figure(figsize=(10, 4))
    limit = int(30.0 / h_stable)
    plt.plot(t_val[:limit], x_val[:limit], label='x(t)')
    plt.plot(t_val[:limit], y_val[:limit], label='y(t)')
    plt.plot(t_val[:limit], z_val[:limit], label='z(t)', alpha=0.7)
    plt.title("State variables vs time")
    plt.xlabel("Time")
    plt.ylabel("amplitudes")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.savefig("plots/01_variables_vs_time.png", dpi=300)
    
    # 2
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.plot(x_val, y_val, lw=0.5, color='royalblue')
    ax1.set_title("X-Y")
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.grid(True, alpha=0.3)

    ax2.plot(x_val, z_val, lw=0.5, color='seagreen')
    ax2.set_title("X-Z")
    ax2.set_xlabel("X")
    ax2.set_ylabel("Z")
    ax2.grid(True, alpha=0.3)
    plt.savefig("plots/02_2d_phase_portraits.png", dpi=300)
    
    # 3
    plt.figure(figsize=(10, 4))
    plt.plot(unstable_data[:, 0], unstable_data[:, 1], color='crimson', label=f'h = {h_unstable} (Unstable)')
    plt.plot(t_val[:int(15.0/h_stable)], x_val[:int(15.0/h_stable)], color='navy', label=f'h = {h_stable} (Stable)', alpha=0.8)
    plt.title("Numerical Stability Analysis")
    plt.xlabel("Time")
    plt.ylabel("X")
    plt.yscale('symlog')  
    plt.grid(True, linestyle='--')
    plt.legend()
    plt.savefig("plots/03_numerical_stability.png", dpi=300)

    # 4
    fig, (ax3, ax4) = plt.subplots(1, 2, figsize=(12, 5))
    ax3.plot(x_val, y_val, lw=0.5, color='indigo')
    ax3.set_title(f"Chaotic behavior alpha= {alpha}")
    ax3.set_xlabel("X")
    ax3.set_ylabel("Y")
    ax3.grid(True, alpha=0.3)

    ax4.plot(periodic_data[:, 1], periodic_data[:, 2], lw=0.8, color='darkorange')
    ax4.set_title(f"periodic behavior alpha = {alpha_periodic}")
    ax4.set_xlabel("X")
    ax4.set_ylabel("Y")
    ax4.grid(True, alpha=0.3)
    plt.savefig("plots/04_parameter_influence.png", dpi=300)
    
    # 5
    fig_3d = plt.figure(figsize=(8, 7))
    ax_3d = fig_3d.add_subplot(111, projection='3d')
    ax_3d.plot(x_val, y_val, z_val, lw=0.4, color='indigo')
    ax_3d.set_title("3D")
    ax_3d.set_xlabel("X Axis")
    ax_3d.set_ylabel("Y Axis")
    ax_3d.set_zlabel("Z Axis")
    plt.savefig("plots/05_3d_double_scroll.png", dpi=300)

    #Lyapunov 
    plt.figure(figsize=(10, 4))
    plt.plot(t_s, distance, color='darkgreen', lw=1.2)
    plt.title("Lyapunov")
    plt.xlabel("Time")
    plt.ylabel("Euclidean Distance")
    plt.yscale('log')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig("plots/07_lyapunov_distance.png", dpi=300)
    
    # 6
    plt.figure(figsize=(10, 4))
    plt.plot(t_s, nominal_path[:, 1], label='Original Trajectory x(t)', color='navy', lw=1.5)               # main plot
    plt.plot(t_s, perturbed_path[:, 1], label='Perturbed Trajectory x(t) (+1e-5)', color='crimson', linestyle='--', lw=1.2)             #  with the slight difference of : 10^-5 
    
    plt.title("Sensitivity to Initial conditions (Butterfly Effect)")
    plt.xlabel("Time")
    plt.ylabel("X Amplitude")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.savefig("plots/06_sensitivity_comparison.png", dpi=300)
    
    plt.show()
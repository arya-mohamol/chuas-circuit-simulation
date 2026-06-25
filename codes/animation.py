import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D 

ALPHA = 9.35
BETA  = 14.79
M0    = -1.14
M1    = -0.71

INIT  = np.array([0.1, 0.1, -0.1])
H     = 0.01
STEPS = 10_000          

TRAIL = 600             
SPEED = 4               

#derivative
def _derivatives(s):
    x, y, z = s
    fx = M1*x + 0.5*(M0 - M1)*(abs(x + 1) - abs(x - 1))
    return np.array([
        ALPHA * (y - x - fx),
        x - y + z,
        -BETA * y
    ])
#rk4
def _integrate():
    traj = np.empty((STEPS + 1, 3))
    traj[0] = INIT
    s = INIT.copy()
    for i in range(1, STEPS + 1):
        k1 = _derivatives(s)
        k2 = _derivatives(s + H/2 * k1)
        k3 = _derivatives(s + H/2 * k2)
        k4 = _derivatives(s + H   * k3)
        s  = s + (H/6) * (k1 + 2*k2 + 2*k3 + k4)
        traj[i] = s
    return traj

traj = _integrate()
X, Y, Z = traj[:, 0], traj[:, 1], traj[:, 2]
N = len(X)



fig = plt.figure(figsize=(9, 8), facecolor="#0a0a0f")
ax  = fig.add_subplot(111, projection="3d", facecolor="#0a0a0f")

ax.set_xlim(X.min(), X.max())
ax.set_ylim(Y.min(), Y.max())
ax.set_zlim(Z.min(), Z.max())
ax.set_xlabel("X", color="#5555A0")
ax.set_ylabel("Y", color="#666688")
ax.set_zlabel("Z", color="#666688")
ax.tick_params(colors="#444466", labelsize=7)

for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
    pane.fill = False
    pane.set_edgecolor("#1a1a2e")

ax.set_title("Chua's Circuit  —  Double Scroll Attractor",color="white", fontsize=12, pad=12)

trail,  = ax.plot([], [], [], lw=0.8,  color="#00cfff", alpha=0.5)
head,   = ax.plot([], [], [], "o",     color="white",   markersize=5, zorder=6)
t_label = ax.text2D(0.02, 0.96, "", transform=ax.transAxes,color="#888899", fontsize=9, va="top")



_state = {"i": 0, "paused": False}

def _init():
    trail.set_data([], [])
    trail.set_3d_properties([])
    head.set_data([], [])
    head.set_3d_properties([])
    return trail, head, t_label

def _step(_frame):
    if _state["paused"]:
        return trail, head, t_label

    i     = _state["i"]
    start = max(0, i - TRAIL)

    trail.set_data(X[start:i], Y[start:i])
    trail.set_3d_properties(Z[start:i])
    head.set_data([X[i]], [Y[i]])
    head.set_3d_properties([Z[i]])
    t_label.set_text(f"t = {i * H:.2f}")

    ax.view_init(elev=22, azim=(_frame * 0.18) % 360)

    _state["i"] = (i + SPEED) % N
    return trail, head, t_label

anim = animation.FuncAnimation(
    fig, _step,
    init_func=_init,
    interval=16,
    blit=False,
    repeat=True,
    cache_frame_data=False
)

plt.tight_layout()
plt.show()
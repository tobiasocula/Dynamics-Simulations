from vispy import scene, app
from vispy.scene.visuals import Line, Markers
import imageio
import numpy as np
from funcs import system_solve
import sys

# sinewave
func = lambda x: np.sin(0.5 * x)

Tmax = 30 # maximal time to simulate
mu = 0.002 # friction coefficient
v0 = 0 # initial velocity (scalar)
x0 = 3.8 # starting position (x coordinate)
dt = 0.01 # timestep
x_to = 15.0 # furthest possible x-coordinate

sol = system_solve(func, mu, x0, dt, Tmax)

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
view.camera = 'panzoom'  # 2D camera for curve plotting

# Curve line (starts with first point)
#curve_pos = np.column_stack([sol[2, :], sol[3, :]])
x = np.linspace(0, 20, 1000)
curve_pos = np.column_stack([x, func(x)])
curve_line = Line(pos=curve_pos, color='cyan', width=3, method='gl')
view.add(curve_line)

# Current point marker
marker_pos = np.array([[sol[2, 0], sol[3, 0]]])
marker = Markers()
marker.set_data(marker_pos, face_color='red', edge_color='darkred', size=12)
view.add(marker)

# Set view limits
view.camera.set_range(x=[x0, x_to], y=[-2, 2])

app.process_events()

l = sol.shape[1]

idx = 1
def update(ev):
    global idx
    if idx >= l:
        return
    new_pos = np.array([[sol[2, idx], sol[3, idx]]])
    marker.set_data(new_pos, face_color='red', size=12)
    idx += 1

timer = app.Timer(interval=dt, connect=update, start=True)  # ~60 FPS

app.run()
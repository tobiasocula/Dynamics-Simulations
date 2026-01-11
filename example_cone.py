from vispy import scene, app
from vispy.scene import visuals
from vispy.geometry import MeshData
import numpy as np
from funcs import system_solve_3
import numpy as np

mu = 0.01
Tmax = 30
dt = 0.01

x0 = 2.0
y0 = 2.0
vx0 = 0.0
vy0 = 0.0
vz0 = 0.0

func = lambda x,y: np.sqrt(1.5 + x*x + y*y)

result = system_solve_3(func, x0, y0, vx0, vy0, vz0, mu, Tmax, dt)

x = result[0, :]
y = result[1, :]
vx = result[2, :]
vy = result[3, :]
vz = result[4, :]

xvalues = np.linspace(-4, 4, 60)
yvalues = np.linspace(-4, 4, 60)
X, Y = np.meshgrid(xvalues, yvalues)
Z = func(X, Y)

# Flatten grid
vertices = np.c_[X.flatten(), Y.flatten(), Z.flatten()]

# Create faces (each square -> 2 triangles)
faces = []
nx, ny = X.shape
for i in range(nx - 1):
    for j in range(ny - 1):
        # 2 triangles per square
        idx = i * ny + j
        faces.append([idx, idx + 1, idx + ny])
        faces.append([idx + 1, idx + ny + 1, idx + ny])
faces = np.array(faces)

# Create MeshData object
mesh_data = MeshData(vertices=vertices, faces=faces)

# Create the Mesh visual
mesh = visuals.Mesh(meshdata=mesh_data, color=(0.5, 0.8, 0.5, 1), shading='smooth')

# Add to scene
canvas = scene.SceneCanvas(keys='interactive', show=True, bgcolor='white', size=(600, 600))
view = canvas.central_widget.add_view()
view.camera = scene.cameras.TurntableCamera(fov=45, azimuth=30, elevation=30, distance=20)
view.add(mesh)

# animating

scatter = visuals.Markers()
initial_pos = np.array([[x[0], y[0], func(x[0], y[0])]])
scatter.set_data(initial_pos, face_color='red', size=12)
view.add(scatter)

l = result.shape[1]

idx = 1
def update(ev):
    global idx
    if idx >= l:
        return
    new_pos = np.array([[x[idx], y[idx], func(x[idx], y[idx])]])
    print('new pos:', new_pos, 'idx:', idx)
    scatter.set_data(new_pos, face_color='red', size=12)
    idx += 1

timer = app.Timer(interval=dt, connect=update, start=True)  # ~60 FPS

app.run()
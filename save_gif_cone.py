import numpy as np
from vispy import scene, app
from vispy.scene.visuals import Markers
import imageio
from vispy.geometry import MeshData
from vispy.scene import visuals
from funcs import system_solve_3
from vispy.visuals.filters import ShadingFilter
from vispy.gloo.util import _screenshot  # Better for capture

mu = 0.01
Tmax = 30
dt = 0.01

x0 = 2.0
y0 = 2.0
vx0 = 0.0
vy0 = 0.0
vz0 = 0.0

func = lambda x,y: np.sqrt(1.5 + x*x + y*y) - 2

result = system_solve_3(func, x0, y0, vx0, vy0, vz0, mu, Tmax, dt)

x = result[0, :]
y = result[1, :]
vx = result[2, :]
vy = result[3, :]
vz = result[4, :]

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(400,400))
canvas.context.set_state(depth_test=True)
view = canvas.central_widget.add_view()
view.camera = scene.cameras.TurntableCamera(distance=10)

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
mesh = visuals.Mesh(meshdata=mesh_data, color=(0.5, 0.8, 0.5, 1))
view.add(mesh)

scatter = Markers()
initial_pos = np.array([[x[0], y[0], func(x[0], y[0])]])
scatter.set_data(initial_pos, face_color='red', size=10, edge_color='red')
view.add(scatter)

app.process_events()  # Draw camera transform

# Shading last
shading_filter = ShadingFilter()
mesh.attach(shading_filter)
shading_filter.ambient_light = (1, 1, 1, 0.6)
shading_filter.diffuse_light = (1, 1, 1, 0.8)
shading_filter.specular_coefficient = (1, 1, 1, 0.3)
shading_filter.shininess = 50
shading_filter.light_dir = (0, 0, -1)
mesh.update()

app.process_events() # let VisPy initialize

view.camera.center = (0, 0, 0)
view.camera.distance = 15  # Pull back for full view
view.camera.elevation = 45  # Angle down
view.camera.azimuth = 0

frames = []
for idx in range(result.shape[1] // 4):
    new_pos = np.array([[x[idx], y[idx], func(x[idx], y[idx])]])
    scatter.set_data(new_pos, face_color='red', size=15)
    
    app.process_events()
    canvas.update()
    
    # Reliable offscreen capture (flips Y for correct top-left origin)
    img = _screenshot()[:, :, :3] / 255.0  # Shape (H, W, 3)
    
    frames.append((img * 255).astype(np.uint8))

print('saving')
imageio.mimsave("animation2.gif", frames, fps=30)
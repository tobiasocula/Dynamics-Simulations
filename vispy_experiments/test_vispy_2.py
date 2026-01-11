from vispy import scene, app
from vispy.scene import visuals
import numpy as np
from vispy.geometry import MeshData

"""
summary of VisPy:

Think of VisPy in terms of scene graphs:

Canvas → the window or drawing surface

View → a camera + container for visuals

Visuals → renderable objects (Mesh, Markers, Line, etc.)

Camera → controls view and perspective (Turntable, Fly, Arcball)

Timer → updates visuals for real-time animations

Everything you want to render is a visual attached to a view, and any dynamic updates happen by changing the visual’s data.

"""

# ===============================
# 1️⃣ Create canvas and 3D view
# ===============================
canvas = scene.SceneCanvas(keys='interactive', show=True, bgcolor='white', size=(600, 600))
view = canvas.central_widget.add_view()
view.camera = scene.cameras.TurntableCamera(fov=45, azimuth=30, elevation=30, distance=10)

# ===============================
# 2️⃣ Create a static mesh (optional)
# ===============================
# For demonstration, a simple wavy surface
x = np.linspace(-4, 4, 50)
y = np.linspace(-4, 4, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

vertices = np.c_[X.flatten(), Y.flatten(), Z.flatten()]

# Create faces for the mesh
faces = []
nx, ny = X.shape
for i in range(nx - 1):
    for j in range(ny - 1):
        idx = i * ny + j
        faces.append([idx, idx + 1, idx + ny])
        faces.append([idx + 1, idx + ny + 1, idx + ny])
faces = np.array(faces)

mesh_data = MeshData(vertices=vertices, faces=faces)
mesh = visuals.Mesh(meshdata=mesh_data, color=(0.5, 0.8, 0.5, 1), shading='smooth')
view.add(mesh)

# ===============================
# 3️⃣ Create animated point
# ===============================
scatter = visuals.Markers()
initial_pos = np.array([[0, 0, 1]])
scatter.set_data(initial_pos, face_color='red', size=12)
view.add(scatter)

# ===============================
# 4️⃣ Animation function
# ===============================
t = 0
def update(ev):
    global t
    t += 0.05
    # Moving point along a 3D parametric path
    new_pos = np.array([[np.sin(t), np.cos(t), np.sin(2*t)]])
    scatter.set_data(new_pos, face_color='red', size=12)

# ===============================
# 5️⃣ Timer for real-time animation
# ===============================
timer = app.Timer(interval=0.016, connect=update, start=True)  # ~60 FPS

# ===============================
# 6️⃣ Run the app
# ===============================
if __name__ == "__main__":
    app.run()

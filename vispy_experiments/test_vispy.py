from vispy import scene, app
from vispy.scene import visuals
from vispy.geometry import MeshData
import numpy as np

# Create vertices and faces for a simple surface
x = np.linspace(-4, 4, 50)
y = np.linspace(-4, 4, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

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
view.camera = scene.cameras.TurntableCamera(fov=45, azimuth=30, elevation=30, distance=10)
view.add(mesh)

# Run
if __name__ == "__main__":
    app.run()

import numpy as np
from vispy import scene, app
from vispy.scene.visuals import Markers
import imageio

# ===============================
# 1. Setup canvas and view
# ===============================
canvas = scene.SceneCanvas(keys='interactive', show=False, size=(400,400))
view = canvas.central_widget.add_view()
view.camera = scene.cameras.TurntableCamera(distance=10)

# ===============================
# 2. Add scatter (animated point)
# ===============================
scatter = Markers()
scatter.set_data(np.array([[0,0,0]]), face_color='red', size=10)
view.add(scatter)

# ===============================
# 3. Generate frames
# ===============================
frames = []
t = 0
for i in range(60):  # 60 frames
    t += 0.1
    new_pos = np.array([[np.sin(t), np.cos(t), np.sin(2*t)]])
    scatter.set_data(new_pos, face_color='red', size=10)
    
    # render scene
    canvas.render() # returns an RGBA float image in [0,1]
    img = canvas.render(bgcolor='white')  # returns (H,W,4)
    frames.append((img*255).astype(np.uint8))  # convert to uint8

# ===============================
# 4. Save as GIF
# ===============================
imageio.mimsave("animation.gif", frames, fps=30)
print("GIF saved as animation.gif")

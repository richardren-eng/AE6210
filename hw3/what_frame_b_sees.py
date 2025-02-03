import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ax_font_size = 36
frame_label_font_size = 60
point_size = 24
point_color = 'red'
iframe_color = 'black'
bframe_color = 'blue'
vector_color = 'lime'

# Set up figure and axis
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_xlim(-1, 21)
ax.set_ylim(-1, 21)

# Set background colors
fig.patch.set_facecolor('gray')
ax.set_facecolor('gray')

# Define stationary frame I
scale_factor = 5
I_vectors = np.array([[1, 0], [0, 1]]) * scale_factor

# Define origin of frame B
x_B, y_B = 10, 10

# Initialize quiver for frame B
B_quiver = ax.quiver([x_B, x_B], [y_B, y_B], I_vectors[:, 0], I_vectors[:, 1], 
                     color=bframe_color, angles='xy', scale_units='xy', scale=0.7, width=0.03,
                     headwidth=3, headaxislength=5)

# Labels for frame B
B_label_b1 = ax.text(x_B + scale_factor * 0.5, y_B, r'$\hat{b}_1$', fontsize=ax_font_size, color='cyan')
B_label_b2 = ax.text(x_B, y_B + scale_factor * 0.5, r'$\hat{b}_2$', fontsize=ax_font_size, color='cyan')

# Plot point B
ax.plot(x_B, y_B, 'ro', markersize=point_size)
ax.text(x_B + 0.3, y_B - 0.3, 'B', fontsize=ax_font_size, color=point_color)

# Point P (relative to B)
P_offset = np.array([3, 4])
P_marker, = ax.plot([], [], 'ro', markersize=point_size)
P_label = ax.text(0, 0, 'P', fontsize=ax_font_size, color='red')

# Initialize vector r^{BP}
r_BP_quiver = ax.quiver([x_B], [y_B], [0], [0], angles='xy', scale_units='xy', scale=1, width=0.01, color='lime')
r_BP_label = ax.text(x_B, y_B, '', fontsize=ax_font_size, color='#7FFF00')

# Point P is fixed
def update(frame):
    global r_BP_quiver, r_BP_label  # Allow modifications in each frame

    theta = np.radians(frame)  # Convert frame rotation to radians
    R = np.array([[1, 0], [0, 1]])  # Rotation matrix
    B_vectors = I_vectors @ R.T  # Rotate frame B

    # Update quiver for frame B, keeping its origin at (x_B, y_B)
    B_quiver.set_UVC(B_vectors[:, 0], B_vectors[:, 1])

    # Update positions of labels for rotating frame B
    B_label_b1.set_position([x_B + B_vectors[0, 0], y_B + B_vectors[0, 1]])
    B_label_b2.set_position([x_B + B_vectors[1, 0], y_B + B_vectors[1, 1]])

    # Define unit vector along 60-degree axis in frame B
    phi = np.radians(60)  # Fixed direction
    direction_vector = np.array([np.cos(phi), np.sin(phi)])

    # Compute oscillating displacement along this direction
    amplitude = 0.40 * np.linalg.norm(P_offset)  # Adjust as needed
    displacement = amplitude * np.sin(np.radians(frame * 4))  # Bobbing motion
    P_oscillating = P_offset + displacement * direction_vector  # Move P along the 60-degree axis

    # Rotate P's new position with frame B
    P_rotated = R @ P_oscillating  

    # Update point P position
    P_marker.set_data(x_B + P_rotated[0], y_B + P_rotated[1])

    # Update label position for point P
    P_label.set_position([x_B + P_rotated[0] + 0.3, y_B + P_rotated[1] - 0.3])

    # Compute and update the r^{BP} vector
    if r_BP_quiver is not None:
        r_BP_quiver.remove()
    r_BP_quiver = ax.quiver(x_B, y_B, P_rotated[0], P_rotated[1], 
                            angles='xy', scale_units='xy', scale=1, width=0.01, color='lime')

    # Update the label for r^{BP}
    if r_BP_label is not None:
        r_BP_label.remove()
    r_BP_label = ax.text(x_B + P_rotated[0] / 2 - 0.75, y_B + P_rotated[1] / 2 + 1, r'$\mathbf{r}^{BP}$', 
                         fontsize=ax_font_size, color='#7FFF00')

    return B_quiver, B_label_b1, B_label_b2, P_marker, P_label, r_BP_quiver, r_BP_label



# Create animation
ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=40)

plt.show()

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
ax.set_xlim(-1, 20)
ax.set_ylim(-1, 20)

# Set the background color of the figure and axis
fig.patch.set_facecolor('gray')  # Set figure background to gray
ax.set_facecolor('gray')  # Set axis background to gray

# Define basis vectors for frame I (stationary)
scale_factor = 5  # Make the arrows longer
I_vectors = np.array([[1, 0], [0, 1]]) * scale_factor  # Scale the unit vectors

# Define origin of frame B (unaligned)
x_B, y_B = 12.5, 12  # Change this to move frame B

# Plot stationary frame I
ax.quiver([0, 0], [0, 0], I_vectors[:, 0], I_vectors[:, 1], 
          color=iframe_color, angles='xy', scale_units='xy', scale=0.7, width=0.03,
          headwidth=3, headaxislength=5)

# Label frame I's axes
ax.text(1.0, 5.0, r'$\{I\}$', fontsize=frame_label_font_size, color=iframe_color)  # Frame I
ax.text(7.6, 0.0, r'$\hat{i}$', fontsize=ax_font_size, color=iframe_color)  # x-axis (î)
ax.text(0.0, 7.6, r'$\hat{j}$', fontsize=ax_font_size, color=iframe_color)  # y-axis (ĵ)

# Plot point O (origin of frame I)
ax.plot(0, 0, 'ro', markersize=point_size)  # 'ko' stands for black circle marker
ax.text(-1.2, -1.2, 'O', fontsize=ax_font_size, color=point_color)  # Label for point O

# Initialize quiver for frame B (rotating) in blue
B_quiver = ax.quiver([x_B, x_B], [y_B, y_B], I_vectors[:, 0], I_vectors[:, 1], 
                     color='blue', angles='xy', scale_units='xy', scale=0.7, width=0.03,
                     headwidth=3, headaxislength=5)

# Labels for Frame B's axes (initial positions, before rotation)
B_label_b1 = ax.text(x_B + scale_factor * 0.5, y_B, r'$\hat{b}_1$', fontsize=ax_font_size, color='cyan')
B_label_b2 = ax.text(x_B, y_B + scale_factor * 0.5, r'$\hat{b}_2$', fontsize=ax_font_size, color='cyan')


# Plot point B (origin of frame B)
ax.plot(x_B, y_B, 'ro', markersize=point_size)  
ax.text(x_B + 0.3, y_B - 0.3, 'B', fontsize=ax_font_size, color=point_color)  # Label for point B

# Plot point P (initial position of P)
P_offset = np.array([4, 5])  # Initial offset for point P (relative to frame B origin)
P_marker, = ax.plot([], [], 'ro', markersize=point_size)  # Initialize point P marker
P_label = ax.text(0, 0, 'P', fontsize=ax_font_size, color='red')  # Label for point P

# Draw vector r^{OB} connecting O to B
r_OB = np.array([x_B, y_B])  # Vector from O (0,0) to B (x_B, y_B)
ax.quiver(0, 0, r_OB[0], r_OB[1], angles='xy', scale_units='xy', scale=1, width=0.01, color=vector_color)
ax.text(x_B / 2, y_B / 2 - 1, r'$\mathbf{r}^{OB}$', fontsize=ax_font_size, color='#7FFF00')  # Label for the vector

# Initialize variables to hold the previous vector r^{BP} and its label
r_BP_quiver = None
r_BP_label = None

# Rotation function
def update(frame):
    global r_BP_quiver, r_BP_label  # Make them global to modify in each frame

    theta = np.radians(frame)  # Convert degrees to radians
    R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])  # Rotation matrix
    B_vectors = I_vectors @ R.T  # Rotate frame B

    # Update quiver for frame B, keeping its origin at (x_B, y_B)
    B_quiver.set_UVC(B_vectors[:, 0], B_vectors[:, 1])

    # Update positions of labels for rotating frame B
    # Label for b1 (x-axis of frame B) positioned at the tip of the vector
    B_label_b1.set_position([x_B + B_vectors[0, 0], y_B + B_vectors[0, 1]])

    # Label for b2 (y-axis of frame B) positioned at the tip of the vector
    B_label_b2.set_position([x_B + B_vectors[1, 0], y_B + B_vectors[1, 1]])

    # Update position of point P (rotate it with frame B)
    P_rotated = R @ P_offset  # Rotate point P with the same rotation matrix
    P_marker.set_data(x_B + P_rotated[0], y_B + P_rotated[1])  # Update point P position

    # Update position of label for point P
    P_label.set_position([x_B + P_rotated[0] + 0.3, y_B + P_rotated[1] - 0.3])

    # Update the vector r^{BP}
    r_BP_rotated = R @ P_offset  # Rotate the vector r^{BP}

    # If the previous vector exists, remove it
    if r_BP_quiver is not None:
        r_BP_quiver.remove()

    # Draw the new r^{BP} vector
    r_BP_quiver = ax.quiver(x_B, y_B, r_BP_rotated[0], r_BP_rotated[1], 
                            angles='xy', scale_units='xy', scale=1, width=0.01, color='lime')

    # Remove the old label for r^{BP} if it exists
    if r_BP_label is not None:
        r_BP_label.remove()

    # Update the label for the vector r^{BP}
    r_BP_label = ax.text(x_B + r_BP_rotated[0] / 2, y_B + r_BP_rotated[1] / 2, r'$\mathbf{r}^{BP}$', 
                         fontsize=ax_font_size, color='#7FFF00')  # Label for the vector

    return B_quiver, B_label_b1, B_label_b2, P_marker, P_label, r_BP_quiver, r_BP_label

# Create animation
ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=40)

plt.show()

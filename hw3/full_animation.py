import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button

ax_font_size = 36
frame_label_font_size = 60
point_size = 24
point_color = 'red'
iframe_color = 'black'
bframe_color = 'blue'
vector_color = 'lime'
cross_vector_color = 'magenta'  # Color for the cross product vector

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

# Plot stationary frame I
ax.quiver([0, 0], [0, 0], I_vectors[:, 0], I_vectors[:, 1], 
          color=iframe_color, angles='xy', scale_units='xy', scale=0.7, width=0.03,
          headwidth=3, headaxislength=5)

# Label frame I
ax.text(1.0, 5.0, r'$\{I\}$', fontsize=frame_label_font_size, color=iframe_color)
ax.text(7.6, 0.0, r'$\hat{i}$', fontsize=ax_font_size, color=iframe_color)
ax.text(0.0, 7.6, r'$\hat{j}$', fontsize=ax_font_size, color=iframe_color)

# Plot origin O
ax.plot(0, 0, 'ro', markersize=point_size)
ax.text(-1.2, -1.2, 'O', fontsize=ax_font_size, color=point_color)

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

# Draw vector r^{OB}
ax.quiver(0, 0, x_B, y_B, angles='xy', scale_units='xy', scale=1, width=0.01, color=vector_color)
ax.text(x_B / 2, y_B / 2 - 1, r'$\mathbf{r}^{OB}$', fontsize=ax_font_size, color='#7FFF00')

# Initialize vector r^{BP}
r_BP_quiver = ax.quiver([x_B], [y_B], [0], [0], angles='xy', scale_units='xy', scale=1, width=0.01, color='lime')
r_BP_label = ax.text(x_B, y_B, '', fontsize=ax_font_size, color='#7FFF00')

# Initialize cross product vector
cross_product_quiver = ax.quiver([], [], [], [], angles='xy', scale_units='xy', scale=1, width=0.01, color=cross_vector_color)
cross_product_label = ax.text(0, 0, '', fontsize=ax_font_size, color=cross_vector_color)

# Animation pause flag
is_paused = False

# Cross product visibility flag
show_cross_product = False

# Define pause button callback
def toggle_pause(event):
    global is_paused
    is_paused = not is_paused
    if is_paused:
        ani.event_source.stop()
    else:
        ani.event_source.start()

# Define toggle cross product button callback
def toggle_cross_product(event):
    global show_cross_product
    show_cross_product = not show_cross_product
    if not show_cross_product:
        cross_product_quiver.set_UVC([], [])  # Hide the cross product vector
        cross_product_label.set_text('')  # Hide the label
    else:
        update(ani.frame_seq.__next__())  # Update to show the cross product vector

# Rotation function
def update(frame):
    if is_paused:
        return []  # If paused, skip updating the animation

    global r_BP_quiver, r_BP_label, cross_product_quiver, cross_product_label  # Allow modifications in each frame

    theta = np.radians(frame)  # Convert frame rotation to radians
    R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])  # Rotation matrix
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
    r_BP_label = ax.text(x_B + P_rotated[0] / 2, y_B + P_rotated[1] / 2, r'$\mathbf{r}^{BP}$', 
                         fontsize=ax_font_size, color='#7FFF00')

    # Cross product calculation: Cross product of z-axis (0, 0, 1) and r^{BP}
    vel_scale = 0.5
    z_axis = vel_scale * np.array([0, 0, 1])  # z-axis vector
    r_BP = np.array([P_rotated[0], P_rotated[1], 0])  # r^{BP} vector (3D, z=0)
    cross_product = np.cross(z_axis, r_BP)  # Cross product result

    # The result of cross product is in the z-direction, so update it as a 2D vector
    cross_product_2d = np.array([cross_product[0], cross_product[1]])

    # Update cross product quiver, with its tail at point P (x_B + P_rotated[0], y_B + P_rotated[1])
    if cross_product_quiver is not None:
        cross_product_quiver.remove()
    if show_cross_product:
        cross_product_quiver = ax.quiver(x_B + P_rotated[0], y_B + P_rotated[1], cross_product_2d[0], cross_product_2d[1], 
                                         angles='xy', scale_units='xy', scale=1, width=0.01, color=cross_vector_color)

        # Update the label for cross product vector
        if cross_product_label is not None:
            cross_product_label.remove()
        cross_product_label = ax.text(x_B + P_rotated[0] + cross_product_2d[0] / 2, 
                                      y_B + P_rotated[1] + cross_product_2d[1] / 2, r'$^{I}\mathbf{\omega}^{B} \times \mathbf{r}^{BP}$', 
                                      fontsize=ax_font_size, color=cross_vector_color)
    else:
        cross_product_quiver = ax.quiver([], [], [], [], angles='xy', scale_units='xy', scale=1, width=0.01, color=cross_vector_color)
        cross_product_label.set_text('')

    return B_quiver, B_label_b1, B_label_b2, P_marker, P_label, r_BP_quiver, r_BP_label, cross_product_quiver, cross_product_label

# Create pause button
ax_pause = plt.axes([0.8, 0.02, 0.1, 0.05])
button_pause = Button(ax_pause, 'Freeze Time', color='lightgoldenrodyellow', hovercolor='yellow')
button_pause.on_clicked(toggle_pause)

# Create toggle cross product button
ax_toggle_cross = plt.axes([0.65, 0.02, 0.15, 0.05])
button_toggle_cross = Button(ax_toggle_cross, 'Toggle Cross Product', color='lightgoldenrodyellow', hovercolor='yellow')
button_toggle_cross.on_clicked(toggle_cross_product)

# Create animation
ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=40)

plt.show()
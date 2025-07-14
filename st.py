import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class SpinningTopAnimation:
    def __init__(self):
        # Initialize parameters
        self.velocity = 100  # Initial velocity
        self.velocity_decay_rate = 0.5  # Rate at which velocity decays

        # Initialize plot
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        self.ax.set_zlim(0, 1)
        self.ax.set_title("Spinning Top Motion")
        self.ax.set_xlabel("X axis")
        self.ax.set_ylabel("Y axis")
        self.ax.set_zlabel("Z axis")

        # Meshgrid for the top's shape
        self.u = np.linspace(0, 2 * np.pi, 50)
        self.v = np.linspace(0, 1, 20)
        self.U, self.V = np.meshgrid(self.u, self.v)

        # Initial top shape
        self.x, self.y, self.z = self.create_top()

    def create_top(self):
        """Define the spinning top shape based on velocity."""
        velocity_factor = self.velocity / 100  # Normalize velocity to [0, 1]
        x = (1 - self.V) * np.cos(self.U) * velocity_factor
        y = (1 - self.V) * np.sin(self.U) * velocity_factor
        z = 1 - self.V  # Invert to place the tip at the top
        return x, y, z

    def rotate_top(self):
        """Rotate the top shape for animation."""
        # Precession rotation around Z-axis
        c, s = np.cos(0.1), np.sin(0.1)
        Rz = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

        # Nutation rotation around Y-axis
        c, s = np.cos(0.05), np.sin(0.05)
        Ry = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

        # Combine rotations
        R = Rz @ Ry

        coords = np.array([self.x.flatten(), self.y.flatten(), self.z.flatten()])
        rotated_coords = R @ coords
        self.x = rotated_coords[0].reshape(self.x.shape)
        self.y = rotated_coords[1].reshape(self.y.shape)
        self.z = rotated_coords[2].reshape(self.z.shape)

    def update(self):
        """Update the animation frame."""
        # Decay the velocity
        self.velocity = max(0, self.velocity - self.velocity_decay_rate)

        # Update the top's shape based on the current velocity
        self.x, self.y, self.z = self.create_top()

        # Rotate the top
        self.rotate_top()

        # Clear and redraw the plot
        self.ax.clear()
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        self.ax.set_zlim(0, 1)
        self.ax.plot_surface(self.x, self.y, self.z, color="blue", alpha=0.8)
        self.ax.set_title(f"Spinning Top Motion\nVelocity: {self.velocity:.2f}")
        self.ax.set_xlabel("X axis")
        self.ax.set_ylabel("Y axis")
        self.ax.set_zlabel("Z axis")
        plt.pause(0.05)  # Pause for animation effect

    def run(self):
        """Run the animation."""
        for _ in range(200):  # Simulate 200 frames
            self.update()
        plt.show()

if __name__ == '__main__':
    animation = SpinningTopAnimation()
    animation.run()

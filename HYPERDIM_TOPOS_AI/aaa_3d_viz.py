import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class AAACosmosViz:
    def __init__(self):
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.nodes = []
        self.labels = []

    def add_node(self, q, label, salience=1.0):
        # We project the 8D section to 3D for visualization
        q_3d = q[:3]
        self.nodes.append(q_3d)
        self.labels.append(label)
        # Visual weight based on salience
        self.ax.scatter(q_3d[0], q_3d[1], q_3d[2], s=salience*100, label=label)

    def draw_connections(self):
        # Draw connections between nodes to visualize the sheaf structure
        if len(self.nodes) > 1:
            for i in range(len(self.nodes) - 1):
                n1, n2 = self.nodes[i], self.nodes[i+1]
                self.ax.plot([n1[0], n2[0]], [n1[1], n2[1]], [n1[2], n2[2]], 'gray', alpha=0.5)

    def render(self, title="n-Cosmos UTAI Visibility"):
        self.ax.set_title(title)
        self.ax.set_xlabel('Dim 1')
        self.ax.set_ylabel('Dim 2')
        self.ax.set_zlabel('Dim 3')
        # Draw Poincaré boundary (unit sphere slice)
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x = np.cos(u)*np.sin(v)
        y = np.sin(u)*np.sin(v)
        z = np.cos(v)
        self.ax.plot_wireframe(x, y, z, color="r", alpha=0.1)
        
        plt.legend()
        plt.show()

if __name__ == "__main__":
    viz = AAACosmosViz()
    viz.add_node([0.5, 0.2, 0.1], "Z/k_Graded_Sheaf", salience=1.5)
    viz.add_node([-0.3, 0.4, 0.6], "U(1)_Continuous_Phase", salience=1.2)
    viz.draw_connections()
    viz.render()

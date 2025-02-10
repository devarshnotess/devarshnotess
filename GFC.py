# Gravitational Force calculator 
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

G = 1.0  # Gravitational constant (arbitrary units)
dt = 0.01  # Time step (smaller for better stability)
epsilon = 1e-6  # Small value to prevent division by zero

class CelestialBody:
    def __init__(self, mass, x, y, vx, vy, color='blue'):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = 0.0
        self.ay = 0.0
        self.path = []
        self.color = color
        self.path.append((x, y))

class BodyInputGUI:
    def __init__(self):
        self.bodies = []
        self.colors = ['blue', 'red', 'green', 'orange', 'purple']
        self.color_index = 0
        
        self.root = tk.Tk()
        self.root.title("Celestial Body Input")
        self.root.geometry("300x300")

        # Create input fields
        entries = [
            ("Mass", 0),
            ("X Position", 1),
            ("Y Position", 2),
            ("X Velocity", 3),
            ("Y Velocity", 4)
        ]

        self.entries = {}
        for label_text, row in entries:
            label = ttk.Label(self.root, text=label_text)
            label.grid(row=row, column=0, padx=5, pady=2)
            entry = ttk.Entry(self.root)
            entry.grid(row=row, column=1, padx=5, pady=2)
            self.entries[label_text] = entry

        # Add Body button
        self.add_button = ttk.Button(self.root, text="Add Body", command=self.add_body)
        self.add_button.grid(row=5, column=0, columnspan=2, pady=5)

        # Simulate button
        self.simulate_button = ttk.Button(self.root, text="Simulate", command=self.simulate)
        self.simulate_button.grid(row=6, column=0, columnspan=2, pady=5)

    def add_body(self):
        try:
            mass = float(self.entries["Mass"].get())
            x = float(self.entries["X Position"].get())
            y = float(self.entries["Y Position"].get())
            vx = float(self.entries["X Velocity"].get())
            vy = float(self.entries["Y Velocity"].get())
            
            color = self.colors[self.color_index % len(self.colors)]
            self.color_index += 1
            
            body = CelestialBody(mass, x, y, vx, vy, color)
            self.bodies.append(body)
            
            # Clear entries
            for entry in self.entries.values():
                entry.delete(0, tk.END)
                
        except ValueError:
            print("Invalid input. Please enter numbers.")

    def simulate(self):
        if len(self.bodies) < 1:
            print("Add at least one body to simulate")
            return
        
        self.root.destroy()
        simulate_gravity(self.bodies)

def simulate_gravity(bodies):
    fig, ax = plt.subplots()
    ax.set_title("Gravitational Simulation")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    
    # Initialize plot elements
    scat = ax.scatter(
        [body.x for body in bodies],
        [body.y for body in bodies],
        c=[body.color for body in bodies],
        s=[body.mass*10 for body in bodies]
    )
    
    lines = [ax.plot([], [], '-', color=body.color, lw=1)[0] for body in bodies]
    
    # Set initial plot limits
    all_positions = [coord for body in bodies for coord in (body.x, body.y)]
    max_extent = max(1, max(abs(p) for p in all_positions)) * 1.2
    ax.set_xlim(-max_extent, max_extent)
    ax.set_ylim(-max_extent, max_extent)

    def update(frame):
        # Calculate accelerations
        for i in range(len(bodies)):
            bodies[i].ax = 0.0
            bodies[i].ay = 0.0
            for j in range(len(bodies)):
                if i != j:
                    dx = bodies[j].x - bodies[i].x
                    dy = bodies[j].y - bodies[i].y
                    r_sq = dx**2 + dy**2
                    
                    if r_sq < epsilon:
                        continue
                    
                    r = math.sqrt(r_sq)
                    acceleration = G * bodies[j].mass / r_sq
                    
                    bodies[i].ax += acceleration * dx / r
                    bodies[i].ay += acceleration * dy / r

        # Update positions and velocities
        for body in bodies:
            body.vx += body.ax * dt
            body.vy += body.ay * dt
            body.x += body.vx * dt
            body.y += body.vy * dt
            body.path.append((body.x, body.y))

        # Update plot elements
        scat.set_offsets([(body.x, body.y) for body in bodies])
        scat.set_sizes([max(5, body.mass*10) for body in bodies])
        
        for line, body in zip(lines, bodies):
            if len(body.path) > 1:
                x_vals, y_vals = zip(*body.path)
                line.set_data(x_vals, y_vals)
        
        # Dynamically adjust view
        current_positions = [coord for body in bodies for coord in (body.x, body.y)]
        current_max = max(1, max(abs(p) for p in current_positions)) * 1.2
        ax.set_xlim(-current_max, current_max)
        ax.set_ylim(-current_max, current_max)
        
        return [scat] + lines

    ani = animation.FuncAnimation(
        fig, update, 
        interval=20,
        blit=True,
        cache_frame_data=False
    )
    plt.show()

if __name__ == "__main__":
    gui = BodyInputGUI()
    gui.root.mainloop()

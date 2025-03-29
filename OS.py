#Deadlock detection toolkit it checks all about processes, resources, avilable resource,
#Max Need (per process, separated by semicolon ;):,Allocation (per process, separated by semicolon ;):
import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Banker's Algorithm Implementation
class BankersAlgorithm:
    def __init__(self, processes, resources, available, max_need, allocation):
        self.processes = processes
        self.resources = resources
        self.available = available
        self.max_need = max_need
        self.allocation = allocation
        self.need = [[self.max_need[i][j] - self.allocation[i][j] for j in range(len(resources))] for i in
                     range(len(processes))]

    def is_safe(self):
        work = self.available.copy()
        finish = [False] * len(self.processes)
        safe_sequence = []

        while True:
            found = False
            for i in range(len(self.processes)):
                if not finish[i] and all(self.need[i][j] <= work[j] for j in range(len(self.resources))):
                    work = [work[j] + self.allocation[i][j] for j in range(len(self.resources))]
                    finish[i] = True
                    safe_sequence.append(self.processes[i])
                    found = True

            if not found:
                break

        if all(finish):
            return True, safe_sequence
        else:
            return False, []


# Deadlock Detection with Cycle Identification
def detect_deadlock_with_position(allocation, request, processes, resources):
    G = nx.DiGraph()

    # Add nodes
    for process in processes:
        G.add_node(process, type='process')
    for resource in resources:
        G.add_node(resource, type='resource')

    # Add edges for allocations and requests
    for i in range(len(processes)):
        for j in range(len(resources)):
            if allocation[i][j] > 0:
                G.add_edge(resources[j], processes[i])  # Resource to Process
            if request[i][j] > 0:
                G.add_edge(processes[i], resources[j])  # Process to Resource

    # Detect cycles
    try:
        cycle = nx.find_cycle(G, orientation='original')
        deadlock_positions = [(edge[0], edge[1]) for edge in cycle]
        return True, deadlock_positions, G
    except nx.NetworkXNoCycle:
        return False, [], G


# Resource Allocation Graph Visualization
def draw_resource_allocation_graph(G, deadlock_positions):
    pos = nx.spring_layout(G)
    node_colors = ['lightblue' if G.nodes[node]['type'] == 'process' else 'lightgreen' for node in G.nodes]
    edge_colors = ['red' if (u, v) in deadlock_positions else 'black' for u, v in G.edges]

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=3000, font_size=10,
            font_weight='bold')
    plt.show()


# GUI Implementation
class DeadlockToolkitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deadlock Detection Toolkit")
        self.root.geometry("800x600")

        ttk.Label(root, text="Processes (comma-separated):").pack()
        self.processes_entry = ttk.Entry(root, width=50)
        self.processes_entry.pack()

        ttk.Label(root, text="Resources (comma-separated):").pack()
        self.resources_entry = ttk.Entry(root, width=50)
        self.resources_entry.pack()

        ttk.Label(root, text="Available Resources (comma-separated):").pack()
        self.available_entry = ttk.Entry(root, width=50)
        self.available_entry.pack()

        ttk.Label(root, text="Max Need (rows for processes, semicolon-separated):").pack()
        self.max_need_entry = ttk.Entry(root, width=50)
        self.max_need_entry.pack()

        ttk.Label(root, text="Allocation (rows for processes, semicolon-separated):").pack()
        self.allocation_entry = ttk.Entry(root, width=50)
        self.allocation_entry.pack()

        ttk.Label(root, text="Request (rows for processes, semicolon-separated):").pack()
        self.request_entry = ttk.Entry(root, width=50)
        self.request_entry.pack()

        ttk.Button(root, text="Check Safe State", command=self.check_safe_state).pack(pady=5)
        ttk.Button(root, text="Detect Deadlock", command=self.detect_deadlock).pack(pady=5)
        ttk.Button(root, text="Draw Graph", command=self.draw_graph).pack(pady=5)

    def check_safe_state(self):
        try:
            processes = self.processes_entry.get().split(',')
            resources = self.resources_entry.get().split(',')
            available = list(map(int, self.available_entry.get().split(',')))
            max_need = [list(map(int, row.split(','))) for row in self.max_need_entry.get().split(';')]
            allocation = [list(map(int, row.split(','))) for row in self.allocation_entry.get().split(';')]

            banker = BankersAlgorithm(processes, resources, available, max_need, allocation)
            is_safe, safe_sequence = banker.is_safe()

            if is_safe:
                messagebox.showinfo("Safe State", f"The system is in a safe state. Safe sequence: {safe_sequence}")
            else:
                messagebox.showwarning("Unsafe State", "The system is in an unsafe state. Deadlock may occur.")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def detect_deadlock(self):
        try:
            processes = self.processes_entry.get().split(',')
            resources = self.resources_entry.get().split(',')
            allocation = [list(map(int, row.split(','))) for row in self.allocation_entry.get().split(';')]
            request = [list(map(int, row.split(','))) for row in self.request_entry.get().split(';')]

            deadlock, positions, G = detect_deadlock_with_position(allocation, request, processes, resources)

            if deadlock:
                messagebox.showwarning("Deadlock Detected", f"Deadlock occurs at: {positions}")
            else:
                messagebox.showinfo("No Deadlock", "No deadlock detected.")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def draw_graph(self):
        try:
            processes = self.processes_entry.get().split(',')
            resources = self.resources_entry.get().split(',')
            allocation = [list(map(int, row.split(','))) for row in self.allocation_entry.get().split(';')]
            request = [list(map(int, row.split(','))) for row in self.request_entry.get().split(';')]

            deadlock, positions, G = detect_deadlock_with_position(allocation, request, processes, resources)
            draw_resource_allocation_graph(G, positions)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = DeadlockToolkitApp(root)
    root.mainloop()

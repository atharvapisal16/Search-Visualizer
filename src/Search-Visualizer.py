"""
Search Visualizer - Python Edition
A beautiful GUI application to visualize search algorithms
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import math
from threading import Thread

class SearchVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Search Visualizer")
        self.root.geometry("1400x900")
        self.theme = 'dark'
        # Initialize with dark theme; can be toggled to light
        self.dark_colors = {
            'bg': '#1a1a2e',
            'panel': '#2c3e50',
            'default': '#3498db',
            'current': '#f39c12',
            'visited': '#95a5a6',
            'found': '#2ecc71',
            'text': '#ecf0f1',
            'accent': '#e74c3c',
            'muted_text': '#7f8c8d',
            'separator': '#34495e',
            'canvas_bg': '#0f172a',
            'canvas_text': '#c9d1d9',
            'index_text': '#7f8c8d',
            'bar_outline': '#2980b9',
            'code_bg': '#0d1117',
            'code_fg': '#c9d1d9',
            'entry_bg': '#1f2937',
            'header_bg': '#0b1220',
            'header_text': '#e5e7eb',
            'card_bg': '#16233a',
            'card_border': '#0f1b2d',
            'primary': '#2563eb',
            'danger': '#ef4444',
            'success': '#10b981',
            'warning': '#f59e0b',
            'purple': '#8b5cf6',
            'button_text': '#ffffff'
        }
        self.light_colors = {
            'bg': '#f6f7fb',
            'panel': '#ffffff',
            'default': '#2b6cb0',
            'current': '#d97706',
            'visited': '#9ca3af',
            'found': '#059669',
            'text': '#111827',
            'accent': '#dc2626',
            'muted_text': '#6b7280',
            'separator': '#d1d5db',
            'canvas_bg': '#ffffff',
            'canvas_text': '#111827',
            'index_text': '#6b7280',
            'bar_outline': '#2563eb',
            'code_bg': '#f3f4f6',
            'code_fg': '#111827',
            'entry_bg': '#ffffff',
            'header_bg': '#ffffff',
            'header_text': '#1f2937',
            'card_bg': '#ffffff',
            'card_border': '#e5e7eb',
            'primary': '#2563eb',
            'danger': '#ef4444',
            'success': '#10b981',
            'warning': '#f59e0b',
            'purple': '#8b5cf6',
            'button_text': '#ffffff'
        }
        self.colors = self.dark_colors.copy()
        self.root.configure(bg=self.colors['bg'])
        self.root.resizable(False, False)
        
        # Data
        self.array = [3, 7, 12, 18, 24, 31, 45, 52, 67, 89]
        self.comparisons = 0
        self.is_running = False
        self.animation_speed = 1.0
        
        self.setup_ui()
        self.draw_array()
        self.update_pseudocode()
    
    def set_theme(self, theme: str):
        """Apply theme colors based on selection"""
        self.theme = theme
        if theme == 'light':
            self.colors = self.light_colors.copy()
        else:
            self.colors = self.dark_colors.copy()
        
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        if self.is_running:
            messagebox.showinfo("Busy", "Please wait until the visualization completes to change theme.")
            return
        # Save current UI state
        selected_algo = self.algorithm_var.get() if hasattr(self, 'algorithm_var') else "Binary Search"
        current_speed = self.speed_var.get() if hasattr(self, 'speed_var') else 1.0
        target_text = self.target_entry.get() if hasattr(self, 'target_entry') else ""
        
        # Switch theme
        self.set_theme('light' if self.theme == 'dark' else 'dark')
        
        # Rebuild UI to apply colors uniformly
        for child in self.root.winfo_children():
            child.destroy()
        self.root.configure(bg=self.colors['bg'])
        self.setup_ui()
        
        # Restore state
        self.algorithm_var.set(selected_algo)
        self.speed_var.set(current_speed)
        self.update_speed(current_speed)
        self.target_entry.delete(0, tk.END)
        if target_text:
            self.target_entry.insert(0, target_text)
        
        # Redraw visualization and pseudocode with new theme
        self.draw_array()
        self.update_pseudocode()
        
    def setup_ui(self):
        # Header/Navbar with theme toggle
        header = tk.Frame(self.root, bg=self.colors['header_bg'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Left side: App icon + title
        left_header = tk.Frame(header, bg=self.colors['header_bg'])
        left_header.pack(side=tk.LEFT, padx=20, pady=10)
        
        title_label = tk.Label(
            left_header,
            text="🔍 Search Visualizer",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors['header_bg'],
            fg=self.colors['header_text']
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(
            left_header,
            text="Interactive Algorithm Visualizer",
            font=("Segoe UI", 9),
            bg=self.colors['header_bg'],
            fg=self.colors['muted_text']
        )
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Right side: Theme toggle
        toggle_text = "☀️" if self.theme == 'dark' else "🌙"
        theme_btn = tk.Button(
            header,
            text=toggle_text,
            font=("Segoe UI", 16),
            bg=self.colors['header_bg'],
            fg=self.colors['header_text'],
            activebackground=self.colors['header_bg'],
            activeforeground=self.colors['header_text'],
            relief=tk.FLAT,
            bd=0,
            command=self.toggle_theme,
            cursor="hand2",
            padx=10,
            pady=5
        )
        theme_btn.pack(side=tk.RIGHT, padx=20)
        
        # Separator line
        separator = tk.Frame(self.root, bg=self.colors['separator'], height=1)
        separator.pack(fill=tk.X)
        
        # Title section (kept for compatibility)
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(pady=15)
        
        # Visualization Canvas
        canvas_frame = tk.Frame(self.root, bg=self.colors['bg'])
        canvas_frame.pack(pady=10)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            width=1160,
            height=200,
            bg=self.colors['canvas_bg'],
            highlightthickness=2,
            highlightbackground=self.colors['card_border']
        )
        self.canvas.pack()
        
        # Controls Frame
        controls_frame = tk.Frame(self.root, bg=self.colors['bg'])
        controls_frame.pack(pady=20)
        
        # Algorithm Selection
        algo_frame = tk.Frame(controls_frame, bg=self.colors['bg'])
        algo_frame.grid(row=0, column=0, padx=15)
        
        tk.Label(
            algo_frame,
            text="ALGORITHM",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['muted_text']
        ).pack()
        
        self.algorithm_var = tk.StringVar(value="Binary Search")
        
        # Configure ttk style for combobox
        style = ttk.Style(self.root)
        try:
            style.theme_use('clam')
        except Exception:
            pass
        style.configure('TCombobox', 
                       fieldbackground=self.colors['entry_bg'], 
                       background=self.colors['panel'],
                       foreground=self.colors['text'],
                       arrowcolor=self.colors['text'])
        style.map('TCombobox', fieldbackground=[('readonly', self.colors['entry_bg'])])
        
        self.algorithm_combo = ttk.Combobox(
            algo_frame,
            textvariable=self.algorithm_var,
            values=["Binary Search", "Linear Search"],
            state="readonly",
            width=18,
            font=("Segoe UI", 11)
        )
        self.algorithm_combo.pack(pady=8)
        self.algorithm_combo.bind("<<ComboboxSelected>>", lambda e: self.update_pseudocode())
        
        # Target Input
        target_frame = tk.Frame(controls_frame, bg=self.colors['bg'])
        target_frame.grid(row=0, column=1, padx=15)
        
        tk.Label(
            target_frame,
            text="SEARCH TARGET",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['muted_text']
        ).pack()
        
        self.target_entry = tk.Entry(
            target_frame,
            font=("Segoe UI", 11),
            width=15,
            bg=self.colors['entry_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief=tk.FLAT,
            bd=2
        )
        self.target_entry.pack(pady=8)
        
        # Control Buttons
        button_frame = tk.Frame(controls_frame, bg=self.colors['bg'])
        button_frame.grid(row=0, column=2, padx=15)
        
        tk.Label(
            button_frame,
            text="CONTROLS",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['muted_text']
        ).pack()
        
        btn_container = tk.Frame(button_frame, bg=self.colors['bg'])
        btn_container.pack(pady=8)
        
        self.start_btn = tk.Button(
            btn_container,
            text="▶ Start",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['success'],
            fg=self.colors['button_text'],
            command=self.start_visualization,
            width=10,
            cursor="hand2",
            relief=tk.FLAT,
            activebackground=self.colors['success']
        )
        self.start_btn.grid(row=0, column=0, padx=4)
        
        self.reset_btn = tk.Button(
            btn_container,
            text="↻ Reset",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['danger'],
            fg=self.colors['button_text'],
            command=self.reset_visualization,
            width=10,
            cursor="hand2",
            relief=tk.FLAT,
            activebackground=self.colors['danger']
        )
        self.reset_btn.grid(row=0, column=1, padx=4)
        
        # Speed Control
        speed_frame = tk.Frame(controls_frame, bg=self.colors['bg'])
        speed_frame.grid(row=0, column=3, padx=15)
        
        tk.Label(
            speed_frame,
            text="SPEED",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['muted_text']
        ).pack()
        
        speed_container = tk.Frame(speed_frame, bg=self.colors['bg'])
        speed_container.pack(pady=8)
        
        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_scale = tk.Scale(
            speed_container,
            from_=0.5,
            to=3.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            bg=self.colors['bg'],
            fg=self.colors['text'],
            highlightthickness=0,
            length=130,
            command=self.update_speed,
            troughcolor=self.colors['panel']
        )
        self.speed_scale.grid(row=0, column=0, padx=5)
        
        self.speed_label = tk.Label(
            speed_container,
            text="1.0x",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            width=4
        )
        self.speed_label.grid(row=0, column=1)
        
        # Bottom Section: Legend and Pseudocode side by side
        bottom_frame = tk.Frame(self.root, bg=self.colors['bg'])
        bottom_frame.pack(pady=15, fill=tk.BOTH, expand=True, padx=20)
        
        # Legend (Left side)
        legend_frame = tk.Frame(bottom_frame, bg=self.colors['bg'])
        legend_frame.grid(row=0, column=0, padx=20, sticky="nw")
        
        tk.Label(
            legend_frame,
            text="LEGEND",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['muted_text']
        ).pack(anchor="w", pady=(0, 12))
        
        legends = [
            ("■", self.colors['current'], "Current"),
            ("■", self.colors['visited'], "Visited"),
            ("■", self.colors['found'], "Found"),
            ("■", self.colors['default'], "Default")
        ]
        
        for symbol, color, text in legends:
            frame = tk.Frame(legend_frame, bg=self.colors['bg'])
            frame.pack(anchor="w", pady=4)
            
            tk.Label(
                frame,
                text=symbol,
                font=("Segoe UI", 20),
                bg=self.colors['bg'],
                fg=color
            ).pack(side=tk.LEFT, padx=(0, 12))
            
            tk.Label(
                frame,
                text=text,
                font=("Segoe UI", 11),
                bg=self.colors['bg'],
                fg=self.colors['text']
            ).pack(side=tk.LEFT)
        
        # Comparisons
        tk.Label(
            legend_frame,
            text="─" * 22,
            bg=self.colors['bg'],
            fg=self.colors['separator']
        ).pack(pady=12)
        
        self.comparisons_label = tk.Label(
            legend_frame,
            text="Comparisons: 0",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        self.comparisons_label.pack(anchor="w")
        
        # Pseudocode (Right side)
        code_frame = tk.Frame(bottom_frame, bg=self.colors['bg'])
        code_frame.grid(row=0, column=1, padx=20, sticky="nsew")
        
        tk.Label(
            code_frame,
            text="PSEUDOCODE",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['muted_text']
        ).pack(anchor="w", pady=(0, 8))
        
        # Pseudocode text with border
        code_container = tk.Frame(code_frame, bg=self.colors['card_border'], bd=1)
        code_container.pack(fill=tk.BOTH, expand=True)
        
        self.pseudocode_text = tk.Text(
            code_container,
            width=60,
            height=12,
            font=("Consolas", 10),
            bg=self.colors['code_bg'],
            fg=self.colors['code_fg'],
            wrap=tk.NONE,
            state=tk.DISABLED,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.pseudocode_text.pack(fill=tk.BOTH, expand=True)
        
        bottom_frame.grid_columnconfigure(1, weight=1)
        
    def draw_array(self):
        """Draw array visualization"""
        self.canvas.delete("all")
        self.bars = []
        
        bar_width = 80
        bar_height = 60
        spacing = 20
        start_x = 50
        start_y = 100
        
        for i, value in enumerate(self.array):
            x = start_x + i * (bar_width + spacing)
            y = start_y
            
            # Bar
            bar = self.canvas.create_rectangle(
                x, y, x + bar_width, y + bar_height,
                fill=self.colors['default'],
                outline=self.colors['bar_outline'],
                width=2
            )
            
            # Value
            self.canvas.create_text(
                x + bar_width // 2, y + bar_height // 2,
                text=str(value),
                font=("Segoe UI", 16, "bold"),
                fill=self.colors['canvas_text']
            )
            
            # Index
            self.canvas.create_text(
                x + bar_width // 2, y - 15,
                text=str(i),
                font=("Segoe UI", 11),
                fill=self.colors['index_text']
            )
            
            self.bars.append(bar)
    
    def update_bar_color(self, index, state):
        """Update bar color based on state"""
        color_map = {
            'current': self.colors['current'],
            'visited': self.colors['visited'],
            'found': self.colors['found'],
            'default': self.colors['default']
        }
        self.canvas.itemconfig(self.bars[index], fill=color_map.get(state, self.colors['default']))
        self.canvas.update()
    
    def update_speed(self, value):
        """Update animation speed"""
        self.animation_speed = float(value)
        self.speed_label.config(text=f"{self.animation_speed:.1f}x")
    
    def sleep(self, milliseconds):
        """Sleep with speed adjustment"""
        time.sleep((milliseconds / 1000) / self.animation_speed)
    
    def update_comparisons(self):
        """Increment comparison counter"""
        self.comparisons += 1
        self.comparisons_label.config(text=f"Comparisons: {self.comparisons}")
    
    def update_pseudocode(self):
        """Update pseudocode display based on selected algorithm"""
        algorithm = self.algorithm_var.get()
        
        pseudocodes = {
            "Binary Search": """function binarySearch(arr, target):
    left = 0
    right = arr.length - 1

    while left <= right:
        mid = floor((left + right) / 2)

        if arr[mid] == target:
            return mid // Found!

        else if arr[mid] < target:
            left = mid + 1 // Search right

        else:
            right = mid - 1 // Search left

    return -1 // Not found""",
            
            "Linear Search": """function linearSearch(arr, target):
    for i = 0 to arr.length - 1:

        if arr[i] == target:
            return i // Found!

    return -1 // Not found"""
        }
        
        self.pseudocode_text.config(state=tk.NORMAL)
        self.pseudocode_text.delete(1.0, tk.END)
        self.pseudocode_text.insert(1.0, pseudocodes.get(algorithm, ""))
        self.pseudocode_text.config(state=tk.DISABLED)
    
    def start_visualization(self):
        """Start the search visualization"""
        if self.is_running:
            return
        
        target_str = self.target_entry.get().strip()
        if not target_str:
            messagebox.showwarning("Input Required", "Please enter a target number")
            return
        
        try:
            target = int(target_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")
            return
        
        self.reset_visualization()
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        
        # Run in thread to prevent UI freeze
        algorithm = self.algorithm_var.get()
        thread = Thread(target=self.run_algorithm, args=(algorithm, target))
        thread.daemon = True
        thread.start()
    
    def run_algorithm(self, algorithm, target):
        """Execute the selected algorithm"""
        try:
            if algorithm == "Binary Search":
                self.binary_search(target)
            elif algorithm == "Linear Search":
                self.linear_search(target)
        finally:
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL)
    
    def binary_search(self, target):
        """Binary Search Algorithm"""
        left = 0
        right = len(self.array) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            self.update_bar_color(mid, 'current')
            self.update_comparisons()
            self.sleep(800)
            
            if self.array[mid] == target:
                self.update_bar_color(mid, 'found')
                return
            elif self.array[mid] < target:
                self.update_bar_color(mid, 'visited')
                self.sleep(400)
                left = mid + 1
            else:
                self.update_bar_color(mid, 'visited')
                self.sleep(400)
                right = mid - 1
        
        self.sleep(500)
    
    def linear_search(self, target):
        """Linear Search Algorithm"""
        for i in range(len(self.array)):
            self.update_bar_color(i, 'current')
            self.update_comparisons()
            self.sleep(800)
            
            if self.array[i] == target:
                self.update_bar_color(i, 'found')
                return
            else:
                self.update_bar_color(i, 'visited')
                self.sleep(300)
        
        self.sleep(500)
    
    def reset_visualization(self):
        """Reset visualization to initial state"""
        self.comparisons = 0
        self.comparisons_label.config(text="Comparisons: 0")
        self.draw_array()


def main():
    root = tk.Tk()
    app = SearchVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()

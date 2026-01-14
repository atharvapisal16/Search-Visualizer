# 🔍 Search Visualizer - Python Edition #
A beautiful GUI application to visualize linear and binary search algorithms in real-time, built with Python and Tkinter. Features include live array rendering, pseudocode tracking, theme toggling, and adjustable animation speeds.

# 📚 About Search Algorithms #
Searching is a fundamental operation in computer science used to find the location of a specific element within a collection of data. This visualizer demonstrates two core approaches:

Linear Search: The simplest method that checks every element in the list sequentially until a match is found or the whole list has been searched.

Binary Search: An efficient algorithm that finds a target value within a sorted array. It works by repeatedly dividing the search interval in half. If the value of the search key is less than the item in the middle of the interval, the interval is narrowed to the lower half. Otherwise, it is narrowed to the upper half.

This tool allows users to observe how these algorithms traverse data, compare values, and manage indices in real-time.


# ✨ Features #
Real-time Visualization — Watch the algorithms traverse the array step-by-step

Dual Themes — Toggle between Dark Mode 🌙 and Light Mode ☀️

Pseudocode Display — Side-by-side view of code logic highlighting the active line

Speed Control — Adjustable animation speed from 0.5x to 3.0x

Comparison Tracking — Live counter for the number of comparisons made

Interactive UI — Clean, modern interface with color-coded legends

Input Validation — Ensures valid integer targets are entered


# 🧰 Technologies Used #
Python 3.x

Tkinter (Standard Python GUI Library)

Threading (For non-blocking visualizations)


# 📦 Installation & Setup #
Prerequisites
Python 3.x installed on your system.

Tkinter (Usually included with standard Python installations).

🔧 Run Instructions
Clone the repository (or download the file)

Bash

git clone https://github.com/[your-username]/search-visualizer.git
Navigate to project directory

Bash

cd search-visualizer
Run the application

Bash

python Visualizer.py


# 🎮 Usage #
Select Algorithm — Choose between "Binary Search" or "Linear Search" from the dropdown.

Enter Target — Input a number to find (e.g., 31 or 89) in the search box.

Start — Click the ▶ Start button to begin the animation.

Control Speed — Use the slider to speed up or slow down the visualization.

Toggle Theme — Click the Sun/Moon icon in the top right to switch themes.

# Color Legend #
<span style="color: #f39c12">■</span> Current: The element currently being compared.

<span style="color: #95a5a6">■</span> Visited: Elements that have been checked and eliminated.

<span style="color: #2ecc71">■</span> Found: The target element when successfully located.

<span style="color: #3498db">■</span> Default: Unexplored elements.

# ⚖️ License #
This project is licensed under the MIT License. You are free to use, modify, and distribute this software with proper attribution.

# 👨‍💻 Author #
Atharva Pisal

import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import re
import webbrowser
from collections import defaultdict


class CSVReaderGUI:
    def __init__(self, root):
        self.root = root
        self.data = self.read_csv_file()

    def read_csv_file(self):
        data = []
        with open('exploits.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        return data

    def show_trends_pie_chart(self):
        """Create a pie chart based on the monthly trends of recent exploits."""
        # Analyze the exploit data, categorize it by type, and plot the pie chart
        exploit_types = {}
        for exploit in self.data:
            exploit_type = exploit['Type']
            if exploit_type in exploit_types:
                exploit_types[exploit_type] += 1
            else:
                exploit_types[exploit_type] = 1

        print("Exploit Types:", exploit_types)  # Debug print statement
        print("Number of exploit types:", len(exploit_types))  # Debug print statement

        if not exploit_types:
            print("No exploit types found. Cannot create pie chart.")
            return

        # Create a new window for the pie chart
        pie_chart_window = tk.Toplevel(self.root)
        pie_chart_window.title("Exploit Trends Pie Chart")

        # Create the pie chart
        fig = plt.Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.pie(exploit_types.values(), labels=exploit_types.keys(), autopct='%1.1f%%')
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Add the pie chart to the new window
        canvas = FigureCanvasTkAgg(fig, master=pie_chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

        # Add a button to close the pie chart window
        close_button = ttk.Button(pie_chart_window, text="Close", command=pie_chart_window.destroy)
        close_button.pack(side='bottom', fill='x')

class SimpleDarkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Reader")
        self.root.geometry("1000x800")  # Extended dimensions
        
        # Set background color to dark
        self.root.config(bg='#2E2E2E')  # Dark gray background

        # Font and color settings
        self.font_style = ("Arial", 12)
        self.text_color = "#FFFFFF"  # White text

        # Text Area for displaying CSV data
        self.text_area = tk.Text(root, wrap='word', font=self.font_style, bg='#3E3E3E', fg=self.text_color, padx=10, pady=10)
        self.text_area.pack(expand=True, fill='both', padx=20, pady=20)

        # Control Frame
        control_frame = tk.Frame(root, bg='#2E2E2E')
        control_frame.pack(side='top', fill='x')

        # Previous Button
        self.prev_button = ttk.Button(control_frame, text="Previous", command=self.show_prev_chunk)
        self.prev_button.pack(side='left', padx=5)

        # Next Button
        self.next_button = ttk.Button(control_frame, text="Next", command=self.show_next_chunk)
        self.next_button.pack(side='left', padx=5)

        # Chunk Size Entry
        self.chunk_size_label = tk.Label(control_frame, text="Chunk Size:", bg='#2E2E2E', fg=self.text_color)
        self.chunk_size_label.pack(side='left', padx=5)
        self.chunk_size_entry = tk.Entry(control_frame, width=5)
        self.chunk_size_entry.insert(0, "5")
        self.chunk_size_entry.pack(side='left', padx=5)
        self.chunk_size_button = ttk.Button(control_frame, text="Set", command=self.set_chunk_size)
        self.chunk_size_button.pack(side='left', padx=5)

        # Pie Chart Button
        self.pie_chart_button = ttk.Button(control_frame, text="Show Trends Pie Chart", command=self.show_trends_pie_chart)
        self.pie_chart_button.pack(side='left', padx=5)

        # Status Bar
        self.status_bar = tk.Label(root, text="", bg='#2E2E2E', fg=self.text_color)
        self.status_bar.pack(side='bottom', fill='x')

        # Load CSV Data
        self.load_csv()

        # Initialize chunk index
        self.chunk_index = 0
        self.chunk_size = 5  # Default number of rows to display

        # Show the first chunk
        self.show_next_chunk()

    def load_csv(self):
        """Load the CSV file into memory."""
        self.data = []
        
        # Check for the existence of the CSV files
        if os.path.exists('zero_day_news.csv'):
            csv_file = 'zero_day_news.csv'
        elif os.path.exists('zero_day_news.csv'):
            csv_file = 'zero_day_news.csv'
        else:
            self.text_area.insert('end', "Neither CSV file found. Run the scraper first.\n")
            return

        try:
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.data.append(row)
        except Exception as e:
            self.text_area.insert('end', f"Error reading CSV file: {e}\n")

    def show_next_chunk(self):
        """Display the next chunk of rows in the text area."""
        if self.chunk_index >= len(self.data):
            self.text_area.insert('end', "\nNo more data to display.\n")
            return self.text_area.delete(1.0, 'end')  # Clear current text

        end_index = min(self.chunk_index + self.chunk_size, len(self.data))
        for i in range(self.chunk_index, end_index):
            exploit = self.data[i]
            display_text = (
                f"Title: {exploit['Title']}\n"
                f"URL: {exploit['URL']}\n"
                f"Date: {exploit.get('Date', 'N/A')}\n"  # Use 'N/A' if 'Date' is not present
                f"Description: {exploit['Description']}\n\n"
            )
            self.text_area.insert('end', display_text)

        self.chunk_index += self.chunk_size  # Move to the next chunk
        self.update_status_bar()

    def show_prev_chunk(self):
        """Display the previous chunk of rows in the text area."""
        if self.chunk_index <= 0:
            self.text_area.insert('end', "\nNo previous data to display.\n")
            return

        self.chunk_index -= self.chunk_size  # Move to the previous chunk
        if self.chunk_index < 0:
            self.chunk_index = 0

        self.show_next_chunk()

    def update_status_bar(self):
        """Update the status bar with current display information."""
        start_index = self.chunk_index + 1
        end_index = min(self.chunk_index + self.chunk_size, len(self.data))
        self.status_bar.config(text=f"Showing {start_index}-{end_index} of {len(self.data)}")

    def set_chunk_size(self):
        """Set the chunk size based on user input."""
        try:
            new_size = int(self.chunk_size_entry.get())
            if new_size > 0:
                self.chunk_size = new_size
                self.chunk_index = 0  # Reset to show the first chunk
                self.show_next_chunk()
            else:
                messagebox.showerror("Error", "Chunk size must be a positive integer.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def show_trends_pie_chart(self):
        """Create a pie chart based on the monthly trends of recent exploits."""
        # Categorize by type for pie chart
        exploit_types = defaultdict(int)
        for exploit in self.data:
            exploit_type = exploit.get('Type', 'Unknown')  # Default to 'Unknown' if type is missing
            exploit_types[exploit_type] += 1

        # Create a new window for the pie chart
        pie_chart_window = tk.Toplevel(self.root)
        pie_chart_window.title("Exploit Trends Pie Chart")

        # Create the pie chart
        fig = Figure(figsize=(6, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.pie(exploit_types.values(), labels=exploit_types.keys(), autopct='%1.1f%%')
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Add the pie chart to the new window
        canvas = FigureCanvasTkAgg(fig, master=pie_chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

        # Add a button to close the pie chart window
        close_button = ttk.Button(pie_chart_window, text="Close", command=pie_chart_window.destroy)
        close_button.pack(side='bottom', fill='x')

    def open_url(self, url):
        """Open the given URL in the default web browser."""
        webbrowser.open(url)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleDarkGUI(root)
    root.mainloop()

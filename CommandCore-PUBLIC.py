import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
import os
import subprocess
import sys
import threading
import time
import psutil
import platform
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import speedtest
from PIL import Image, ImageDraw, ImageTk
import re

# Create main application window
root = tk.Tk()
root.title("")
root.geometry("1500x700")  # Adjusted window size
root.configure(bg="#2c3e50")  # Set background color to dark blue
root.attributes('-toolwindow', True)  # Remove window corner symbols

# Function to create a rounded rectangle image
def create_rounded_rectangle(width, height, radius, color):
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, width, height), radius, fill=color)
    return ImageTk.PhotoImage(image)

# Function to open file explorer
def open_file_explorer():
    try:
        filename = filedialog.askopenfilename(initialdir="/", title="Select a File")
        if filename:
            messagebox.showinfo("File Selected", f"You selected:\n{filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file explorer: {str(e)}")

# Function to open a new text document
def open_new_text_document():
    try:
        subprocess.run(["notepad.exe", "new_document.txt"])  # Open with default text editor
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open new text document: {str(e)}")

def open_idle():
    try:
        subprocess.Popen([sys.executable, "-m", "idlelib.idle"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open IDLE: {str(e)}")

def open_vscode():
    try:
        # Get the current username
        username = os.getlogin()
        # Construct the path using the username
        vscode_path = f"C:\\Users\\{username}\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        # Check if the file exists
        if not os.path.isfile(vscode_path):
            raise FileNotFoundError(f"Visual Studio Code not found at {vscode_path}")

        # Open Visual Studio Code
        subprocess.Popen([vscode_path])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Visual Studio Code: {str(e)}")

def open_notepad_plus_plus():
    try:
        subprocess.Popen(["notepad++"])  # Ensure 'notepad++' command is available in PATH
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Notepad++: {str(e)}")

def open_thonny():
    try:
        subprocess.Popen(["thonny"])  # Ensure 'thonny' command is available in PATH
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Thonny: {str(e)}")

def open_arduino_ide():
    try:
        subprocess.Popen(["arduino"])  # Ensure 'arduino' command is available in PATH
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Arduino IDE: {str(e)}")

# Function to handle command execution
def execute_command():
    command = command_entry.get()
    if command:
        # Display command in the command output terminal
        text_terminal.config(state=tk.NORMAL)
        text_terminal.insert(tk.END, f"$ {command}\n")
        text_terminal.config(state=tk.DISABLED)
        # Redirect stdout to text terminal for command output
        sys.stdout = text_terminal_output
        try:
            # Implement command execution logic here
            if command.lower() == "help":
                show_help()
            else:
                execute_custom_command(command)
        except Exception as e:
            text_terminal.config(state=tk.NORMAL)
            text_terminal.insert(tk.END, f"Error executing command: {str(e)}\n")
            text_terminal.config(state=tk.DISABLED)
        finally:
            # Restore stdout back to default
            sys.stdout = sys.__stdout__
        command_entry.delete(0, tk.END)  # Clear command entry after execution

# Function to handle Enter key press in command entry
def on_enter_key(event):
    execute_command()

# Function to handle Enter key press in search entry
def on_search_enter_key(event):
    search_in_terminal()

# Function to execute custom commands
def execute_custom_command(command):
    # Display command in the command output terminal
    text_terminal.config(state=tk.NORMAL)
    text_terminal.insert(tk.END, f"Command: {command}\n")
    
    # Implement logic for custom commands here
    if command.lower() == "list":
        text_terminal.insert(tk.END, "Listing files...\n")
        list_files()
    elif command.lower() == "date":
        text_terminal.insert(tk.END, "Current date and time:\n")
        show_date()
    elif command.lower() == "cpu":
        text_terminal.insert(tk.END, "Current CPU Usage:\n")
        show_cpu_usage()
    elif command.lower() == "memory":
        text_terminal.insert(tk.END, "Current Memory Usage:\n")
        show_memory_usage()
    elif command.lower() == "disk":
        text_terminal.insert(tk.END, "Current Disk Usage:\n")
        show_disk_usage()
    elif command.lower() == "network":
        text_terminal.insert(tk.END, "Current Network Usage:\n")
        show_network_usage()
    elif command.lower().startswith("view "):
        filename = command[5:].strip()
        text_terminal.insert(tk.END, f"Viewing contents of {filename}:\n")
        view_file(filename)
    elif command.lower() == "powershell":
        open_powershell()
    elif command.lower() == "graph":
        show_graph()
    else:
        text_terminal.insert(tk.END, f"Command '{command}' not recognized. Type 'help' for list of commands.\n")
    
    text_terminal.config(state=tk.DISABLED)

# Function to view the contents of a file
def view_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            text_terminal.config(state=tk.NORMAL)
            text_terminal.insert(tk.END, content + "\n")
            text_terminal.config(state=tk.DISABLED)
    except FileNotFoundError:
        text_terminal.config(state=tk.NORMAL)
        text_terminal.insert(tk.END, f"Error: File '{filename}' not found.\n")
        text_terminal.config(state=tk.DISABLED)
    except PermissionError:
        text_terminal.config(state=tk.NORMAL)
        text_terminal.insert(tk.END, f"Error: Permission denied to read '{filename}'.\n")
        text_terminal.config(state=tk.DISABLED)
    except Exception as e:
        text_terminal.config(state=tk.NORMAL)
        text_terminal.insert(tk.END, f"Error viewing file: {str(e)}\n")
        text_terminal.config(state=tk.DISABLED)

# Function to create a dropdown menu for file selection
def create_file_dropdown():
    files = os.listdir()
    dropdown = ttk.Combobox(root, values=files)  # Use ttk.Combobox
    dropdown.set("Select a file")
    dropdown.pack()

    def on_select(event):
        selected_file = dropdown.get()
        execute_custom_command(f"view {selected_file}")

    dropdown.bind("<<ComboboxSelected>>", on_select)

# Function to list files in current directory
def list_files():
    files = os.listdir()
    text_terminal.config(state=tk.NORMAL)
    for file in files:
        text_terminal.insert(tk.END, f"- {file}\n")
    text_terminal.config(state=tk.DISABLED)

import logging

# Setup logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

from datetime import datetime

# Function to display current date and time using Python
def show_date():
    try:
        now = datetime.now()
        date_output = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Display the result in the text terminal
        text_terminal.config(state=tk.NORMAL)
        text_terminal.insert(tk.END, f"Current date and time: {date_output}\n")
        text_terminal.config(state=tk.DISABLED)
    except Exception as e:
        text_terminal.config(state=tk.NORMAL)
        text_terminal.insert(tk.END, f"Error retrieving date: {str(e)}\n")
        text_terminal.config(state=tk.DISABLED)

# Function to display CPU usage
def show_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)  # Get CPU usage percentage
    text_terminal.config(state=tk.NORMAL)
    text_terminal.insert(tk.END, f"CPU Usage: {cpu_usage}%\n")
    text_terminal.config(state=tk.DISABLED)

# Function to display memory usage
def show_memory_usage():
    memory_info = psutil.virtual_memory()  # Get memory usage information
    text_terminal.config(state=tk.NORMAL)
    text_terminal.insert(tk.END, f"Memory Usage: {memory_info.percent}%\n")
    text_terminal.config(state=tk.DISABLED)

# Function to display disk usage
def show_disk_usage():
    try:
        disk_usage = psutil.disk_usage('/')
        text_terminal.config(state=tk.NORMAL)
        text_terminal.insert(tk.END, f"Disk Usage: {disk_usage.percent}%\n")
        text_terminal.config(state=tk.DISABLED)
    except Exception as e:
        text_terminal.config(state=tk.NORMAL)
        text_terminal.insert(tk.END, f"Error retrieving disk usage: {str(e)}\n")
        text_terminal.config(state=tk.DISABLED)

# Function to display network usage
def show_network_usage():
    try:
        net_io = psutil.net_io_counters()
        text_terminal.config(state=tk.NORMAL)
        text_terminal.insert(tk.END, f"Bytes Sent: {net_io.bytes_sent}\nBytes Received: {net_io.bytes_recv}\n")
        text_terminal.config(state=tk.DISABLED)
    except Exception as e:
        text_terminal.config(state=tk.NORMAL)
        text_terminal.insert(tk.END, f"Error retrieving network usage: {str(e)}\n")
        text_terminal.config(state=tk.DISABLED)

# Function to show help information
def show_help():
    text_terminal.config(state=tk.NORMAL)
    text_terminal.insert(tk.END, "Available commands:\n")
    text_terminal.insert(tk.END, "- help: Display this help message\n")
    text_terminal.insert(tk.END, "- list: List files in current directory\n")
    text_terminal.insert(tk.END, "- date: Show current date and time\n")
    text_terminal.insert(tk.END, "- cpu: Show current CPU usage\n")
    text_terminal.insert(tk.END, "- memory: Show current memory usage\n")
    text_terminal.insert(tk.END, "- disk: Show current disk usage\n")
    text_terminal.insert(tk.END, "- network: Show current network usage\n")
    text_terminal.insert(tk.END, "- view <filename>: View contents of a file\n")
    text_terminal.insert(tk.END, "- powershell: Open PowerShell\n")
    text_terminal.insert(tk.END, "- graph: Show CPU and Memory usage graph\n")
    text_terminal.config(state=tk.DISABLED)

# Function to open PowerShell
def open_powershell():
    try:
        text_terminal.config(state=tk.NORMAL)
        text_terminal.insert(tk.END, "Opening PowerShell...\n")
        text_terminal.config(state=tk.DISABLED)
        subprocess.run(["powershell"], check=True)
    except FileNotFoundError:
        text_terminal.config(state=tk.NORMAL)
        text_terminal.insert(tk.END, "PowerShell is not installed.\n")
        text_terminal.config(state=tk.DISABLED)
    except Exception as e:
        text_terminal.config(state=tk.NORMAL)
        text_terminal.insert(tk.END, f"An error occurred: {str(e)}\n")
        text_terminal.config(state=tk.DISABLED)

# Function to launch Task Manager
def launch_task_manager():
    os.system("taskmgr")  # Launch Task Manager using os.system

# Placeholder functions for Button 1 to Button 6
def button1_function():
    try:
        subprocess.run(["lxterminal", "-e", "htop"], check=True)
    except FileNotFoundError:
        messagebox.showerror("Error", "lxterminal or htop is not installed.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def button2_function():
    try:
        subprocess.run(["powershell"], check=True)
    except FileNotFoundError:
        messagebox.showerror("Error", "PowerShell is not installed.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def button3_function():
    try:
        # Check the operating system
        if platform.system() == "Windows":
            # Open Windows Settings
            subprocess.Popen(["start", "ms-settings:"], shell=True)
        elif platform.system() == "Linux":
            # Open Settings on Linux (assuming GNOME environment)
            subprocess.Popen(["gnome-control-center"], shell=True)
        else:
            messagebox.showinfo("Unsupported OS", "This functionality is only supported on Windows or Linux.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def button4_function():
    try:
        script_name = sys.argv[0]
        python_executable = sys.executable
        command = [python_executable, script_name] + sys.argv[1:]
        messagebox.showinfo("Restarting", "The program will restart now.")
        subprocess.Popen(command, close_fds=True)
        os._exit(0)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def button5_function():
    try:
        if platform.system() == "Windows":
            # Open Task Scheduler on Windows
            subprocess.Popen(["taskschd.msc"], shell=True)
        elif platform.system() == "Linux":
            # Open Task Scheduler on Linux (commonly GNOME schedule manager)
            # Adjust this command based on the desktop environment and scheduler available
            subprocess.Popen(["gnome-schedule"], shell=True)
        else:
            messagebox.showinfo("Unsupported OS", "This functionality is only supported on Windows or Linux.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def button6_function():
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen("cmd.exe")
        elif os.name == 'posix':  # Linux
            subprocess.Popen(["gnome-terminal"])
        else:
            messagebox.showerror("Error", "Unsupported operating system")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open terminal: {str(e)}")

# New functions for additional buttons
def button7_function():
    # Display system information
    system_info = f"""
    OS: {platform.system()} {platform.release()}
    CPU: {platform.processor()}
    Memory: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB
    Disk: {psutil.disk_usage('/').total / (1024 ** 3):.2f} GB
    """
    messagebox.showinfo("System Information", system_info)

def button8_function():
    # Clear the command output terminal
    text_terminal.config(state=tk.NORMAL)
    text_terminal.delete(1.0, tk.END)
    text_terminal.config(state=tk.DISABLED)

def button9_function():
    try:
        st = speedtest.Speedtest()
        st.download()
        st.upload()
        results = st.results.dict()
        speed_test_results = f"""
        Download Speed: {results['download'] / 1_000_000:.2f} Mbps
        Upload Speed: {results['upload'] / 1_000_000:.2f} Mbps
        Ping: {results['ping']} ms
        """

        # Calculate packet loss
        packet_loss = calculate_packet_loss()
        speed_test_results += f"Packet Loss: {packet_loss}%\n"

        text_terminal.config(state=tk.NORMAL)
        text_terminal.insert(tk.END, speed_test_results + "\n")
        text_terminal.config(state=tk.DISABLED)
    except speedtest.ConfigRetrievalError:
        messagebox.showerror("Error", "Failed to retrieve speedtest configuration.")
    except speedtest.NoMatchedServers:
        messagebox.showerror("Error", "No matched speedtest servers.")
    except speedtest.SpeedtestException as e:
        messagebox.showerror("Error", f"Speedtest error: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to perform speed test: {str(e)}")

def calculate_packet_loss():
    try:
        # Use the ping command to calculate packet loss
        if platform.system() == "Windows":
            output = subprocess.check_output("ping -n 10 google.com", shell=True, text=True)
        else:
            output = subprocess.check_output("ping -c 10 google.com", shell=True, text=True)
        
        # Extract packet loss percentage from the output using regular expressions
        if platform.system() == "Windows":
            match = re.search(r"(\d+)% loss", output)
        else:
            match = re.search(r"(\d+)% packet loss", output)
        
        if match:
            packet_loss = int(match.group(1))
        else:
            packet_loss = 0

        return packet_loss
    except Exception as e:
        messagebox.showerror("Error", f"Failed to calculate packet loss: {str(e)}")
        return "N/A"

def button10_function():
    # Open system calculator
    try:
        if platform.system() == "Windows":
            subprocess.Popen("calc.exe")
        elif platform.system() == "Linux":
            subprocess.Popen(["gnome-calculator"])
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "Calculator"])
        else:
            messagebox.showerror("Error", "Unsupported operating system")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open calculator: {str(e)}")

def toggle_file_explorer():
    if file_explorer.winfo_viewable():
        file_explorer.pack_forget()
    else:
        file_explorer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 20), pady=10)

def toggle_info_terminal():
    if info_terminal.winfo_viewable():
        info_terminal.pack_forget()
    else:
        info_terminal.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 20), pady=10)

# Function to toggle fullscreen mode
def toggle_fullscreen():
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

# Function to minimize the window
def minimize_window():
    root.iconify()

# Create desktop frame with ARMADYNE branding colors
desktop_frame = tk.Frame(root, bg="#34495e")  # Set background color to dark blue
desktop_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create menu bar with ARMADYNE branding colors
menu_bar = tk.Menu(root, bg="#2c3e50", fg="white")  # Dark background with white text
root.config(menu=menu_bar)

# File menu with ARMADYNE branding colors
file_menu = tk.Menu(menu_bar, tearoff=0, bg="#2c3e50", fg="white")  # Dark background with white text
menu_bar.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="Open File Explorer", command=open_file_explorer)
file_menu.add_command(label="Open New Text Document", command=open_new_text_document)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

file_menu.add_separator()
file_menu.add_command(label="Open Python IDLE", command=open_idle)
file_menu.add_command(label="Open Visual Studio Code", command=open_vscode)
file_menu.add_command(label="Open Notepad++", command=open_notepad_plus_plus)
file_menu.add_command(label="Open Thonny", command=open_thonny)
file_menu.add_command(label="Open Arduino IDE", command=open_arduino_ide)

# View menu with ARMADYNE branding colors
view_menu = tk.Menu(menu_bar, tearoff=0, bg="#2c3e50", fg="white", activebackground="#34495e", activeforeground="white")  # Dark background with white text and active colors
menu_bar.add_cascade(label="View", menu=view_menu)

view_menu.add_command(label="Toggle File Explorer", command=toggle_file_explorer)
view_menu.add_command(label="Toggle Info Terminal", command=toggle_info_terminal)
view_menu.add_separator()
view_menu.add_command(label="Fullscreen", command=toggle_fullscreen)
view_menu.add_command(label="Minimize", command=minimize_window)

# Function to change theme to color code #2c3e50
def change_to_custom_theme():
    root.configure(bg="#2c3e50")
    desktop_frame.configure(bg="#2c3e50")
    file_explorer.configure(bg="#2c3e50")
    command_label.configure(bg="#2c3e50", fg="white")
    command_entry.configure(bg="white", fg="black", insertbackground="black")
    execute_button.configure(bg="#1abc9c", fg="white")
    output_text.configure(bg="white", fg="black", insertbackground="black")
    info_terminal.configure(bg="white", fg="black", insertbackground="black")
    info_terminal_label.configure(bg="#2c3e50", fg="white")
    button_frame.configure(bg="#2c3e50")
    task_manager_button.configure(bg="#1abc9c", fg="white")
    for button in buttons:
        button.configure(bg="#1abc9c", fg="white")
    static_text.configure(bg="white", fg="black")
    text_terminal.configure(bg="white", fg="black", insertbackground="black")
    command_output_label.configure(bg="#2c3e50", fg="white")

view_menu.add_command(label="Custom Theme", command=change_to_custom_theme)

# Create file explorer area with consistent background color and no border
file_explorer = tk.LabelFrame(desktop_frame, text="", width=180, height=520, bg="#34495e", bd=0)  # Set background color to dark blue
file_explorer.pack_propagate(0)
file_explorer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 20), pady=10)  # Updated pack options

# Create command input area with consistent background color
command_label = tk.Label(desktop_frame, text="Command:", bg="#34495e", fg="white", font=("Arial", 12))  # Set background color to dark blue
command_label.place(x=220, y=20)
command_entry = tk.Entry(desktop_frame, width=70, bg="white", fg="black", insertbackground="black")  # Ensure text entry is enabled
command_entry.place(x=300, y=20)
execute_button = tk.Button(desktop_frame, text="Execute", command=execute_command, bg="#21A6FF", fg="white", font=("Arial", 12, "bold"), relief="flat", bd=0, highlightthickness=0)
execute_button.place(x=780, y=18)

# Bind the Enter key to the command entry
command_entry.bind("<Return>", on_enter_key)

# Ensure the command entry field is enabled for user input
command_entry.config(state=tk.NORMAL)

# Create rounded rectangle images for terminals
rounded_rect_output = create_rounded_rectangle(800, 400, 20, "#ffffff")
rounded_rect_info = create_rounded_rectangle(800, 200, 20, "#ffffff")

# Create output console with rounded corners
output_text_bg = tk.Label(desktop_frame, image=rounded_rect_output, bg="#2c3e50")
output_text_bg.place(x=220, y=60)
output_text = scrolledtext.ScrolledText(output_text_bg, width=80, height=20, bg="white", bd=0)
output_text.pack()

# Create live info terminal with rounded corners
info_terminal_bg = tk.Label(desktop_frame, image=rounded_rect_info, bg="#2c3e50")
info_terminal_bg.place(x=220, y=490)
info_terminal = scrolledtext.ScrolledText(info_terminal_bg, width=80, height=10, bg="white", bd=0)
info_terminal.pack()

# Label for live info terminal
info_terminal_label = tk.Label(desktop_frame, text="Data Terminal", bg="#34495e", fg="white", font=("Arial", 12, "bold"))  # Set background color to dark blue
info_terminal_label.place(x=220, y=460)

# Surrounding frame for buttons
button_frame = tk.Frame(desktop_frame, bg="#34495e", bd=2, relief=tk.SOLID)  # Set background color to dark blue
button_frame.place(x=20, y=100, width=180, height=470)  # Adjusted height for better fit

# Button to launch Task Manager with themed background color
task_manager_button = tk.Button(button_frame, text="Task Manager", command=launch_task_manager, font=("Arial", 12, "bold"), relief="flat", bd=0, highlightthickness=0)
task_manager_button.pack(pady=10)
task_manager_button.configure(bg="#A604FF", fg="white")

# Buttons 1 to 10 below Task Manager button
button_functions = [button1_function, button2_function, button3_function, button4_function, button5_function, button6_function, button7_function, button8_function, button9_function, button10_function]
button_texts = ["Linux Task Manager", "Powershell", "Settings", "Program Reboot", "Task scheduler", "Open Terminal", "System Info", "Clear Terminal", "Speed Test", "Calculator"]
buttons = []
for i, text in enumerate(button_texts):
    button = tk.Button(button_frame, text=text, bg="#9A02FF", fg="white", font=("Arial", 12, "bold"), command=button_functions[i], relief="flat", bd=0, highlightthickness=0)
    button.pack(pady=5)
    buttons.append(button)

# Static text for main terminal centered in the frame
static_text = tk.Label(output_text, text="=== CommandCore ===", bg="white", font=("Arial", 14, "bold"))
static_text.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Centered in the main terminal

# Text terminal to display command input and output
text_terminal = scrolledtext.ScrolledText(desktop_frame, width=50, height=20, bg="white")
text_terminal.place(x=920, y=60)
text_terminal.config(state=tk.DISABLED)  # Disable editing

# Label for Command Output Terminal
command_output_label = tk.Label(desktop_frame, text="Command Output Terminal (Type 'help' for commands)", bg="#34495e", fg="white", font=("Arial", 12, "bold"))  # Set background color to dark blue
command_output_label.place(x=920, y=20)

# Redirect stdout to text terminal for displaying command outputs
class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, output_str):
        self.text_space.configure(state=tk.NORMAL)
        self.text_space.insert(tk.END, output_str)
        self.text_space.configure(state=tk.DISABLED)
        self.text_space.see(tk.END)  # Scroll to the end of the text
        self.text_space.update_idletasks()  # Update the text widget

    def flush(self):
        pass

# Redirect stdout to text terminal
text_terminal_output = StdoutRedirector(text_terminal)

# Function to update the info terminal with live data
def update_info_terminal():
    while True:
        try:
            info_terminal.config(state=tk.NORMAL)
            info_terminal.delete(1.0, tk.END)
            # Display running processes
            processes = subprocess.check_output("tasklist", shell=True, text=True)
            info_terminal.insert(tk.END, processes)
            info_terminal.config(state=tk.DISABLED)
        except subprocess.CalledProcessError as e:
            info_terminal.config(state=tk.NORMAL)
            info_terminal.insert(tk.END, f"Error retrieving process list: {str(e)}\n")
            info_terminal.config(state=tk.DISABLED)
        except Exception as e:
            info_terminal.config(state=tk.NORMAL)
            info_terminal.insert(tk.END, f"Error: {str(e)}\n")
            info_terminal.config(state=tk.DISABLED)
        time.sleep(20)  # Update every 20 seconds

# Function to perform search in the info terminal
def search_in_terminal():
    search_text = search_entry.get()
    if search_text:
        # Clear previous search highlight
        info_terminal.tag_remove("highlight", 1.0, tk.END)
        start_idx = '1.0'
        while True:
            start_idx = info_terminal.search(search_text, start_idx, stopindex=tk.END)
            if not start_idx:
                break
            end_idx = f"{start_idx}+{len(search_text)}c"
            info_terminal.tag_add("highlight", start_idx, end_idx)
            start_idx = end_idx
        info_terminal.tag_config("highlight", background="yellow")
    search_entry.delete(0, tk.END)  # Clear search entry after search

# Add search entry and button to the UI
search_label = tk.Label(desktop_frame, text="Search:", bg="#34495e", fg="white", font=("Arial", 12))
search_label.place(x=220, y=430)
search_entry = tk.Entry(desktop_frame, width=30)
search_entry.place(x=280, y=430)
search_button = tk.Button(desktop_frame, text="Search", command=search_in_terminal)
search_button.place(x=500, y=428)

# Bind the Enter key to the search entry
search_entry.bind("<Return>", on_search_enter_key)

# Start the thread to update the info terminal
threading.Thread(target=update_info_terminal, daemon=True).start()

# Function to toggle file explorer visibility
def toggle_file_explorer():
    if file_explorer.winfo_viewable():
        file_explorer.pack_forget()
    else:
        file_explorer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 20), pady=10)

# Function to toggle info terminal visibility
def toggle_info_terminal():
    if info_terminal.winfo_viewable():
        info_terminal.place_forget()
        info_terminal_label.place_forget()
    else:
        info_terminal.place(x=220, y=490)
        info_terminal_label.place(x=220, y=460)

# Function to set the original theme
def set_original_theme():
    root.configure(bg="#2c3e50")
    desktop_frame.configure(bg="#34495e")
    file_explorer.configure(bg="#34495e")
    command_label.configure(bg="#34495e", fg="white")
    command_entry.configure(bg="white", fg="black", insertbackground="black")
    execute_button.configure(bg="#1abc9c", fg="white")
    output_text.configure(bg="white", fg="black", insertbackground="black")
    info_terminal.configure(bg="white", fg="black", insertbackground="black")
    info_terminal_label.configure(bg="#34495e", fg="white")
    button_frame.configure(bg="#34495e")
    task_manager_button.configure(bg="#1abc9c", fg="white")
    for button in buttons:
        button.configure(bg="#1abc9c", fg="white")
    static_text.configure(bg="white", fg="black")
    text_terminal.configure(bg="white", fg="black", insertbackground="black")
    command_output_label.configure(bg="#34495e", fg="white")

# Function to change theme
def change_theme(theme):
    if theme == "Dark":
        root.configure(bg="#2e2e2e")
        desktop_frame.configure(bg="#2e2e2e")
        file_explorer.configure(bg="#2e2e2e")
        command_label.configure(bg="#2e2e2e", fg="white")
        command_entry.configure(bg="#3e3e3e", fg="white", insertbackground="white")
        execute_button.configure(bg="#5e5e5e", fg="white")
        output_text.configure(bg="#3e3e3e", fg="white", insertbackground="white")
        info_terminal.configure(bg="#3e3e3e", fg="white", insertbackground="white")
        info_terminal_label.configure(bg="#2e2e2e", fg="white")
        button_frame.configure(bg="#2e2e2e")
        task_manager_button.configure(bg="#5e5e5e", fg="white")
        for button in buttons:
            button.configure(bg="#5e5e5e", fg="white")
        static_text.configure(bg="#3e3e3e", fg="white")
        text_terminal.configure(bg="#3e3e3e", fg="white", insertbackground="white")
        command_output_label.configure(bg="#2e2e2e", fg="white")
    elif theme == "Light":
        root.configure(bg="silver")
        desktop_frame.configure(bg="silver")
        file_explorer.configure(bg="silver")
        command_label.configure(bg="silver", fg="black")
        command_entry.configure(bg="white", fg="black", insertbackground="black")
        execute_button.configure(bg="#009688", fg="white")
        output_text.configure(bg="white", fg="black", insertbackground="black")
        info_terminal.configure(bg="white", fg="black", insertbackground="black")
        info_terminal_label.configure(bg="silver", fg="black")
        button_frame.configure(bg="silver")
        task_manager_button.configure(bg="#009688", fg="white")
        for button in buttons:
            button.configure(bg="#009688", fg="white")
        static_text.configure(bg="white", fg="black")
        text_terminal.configure(bg="white", fg="black", insertbackground="black")
        command_output_label.configure(bg="silver", fg="black")
    else:
        set_original_theme()

# Apply the original theme when the software boots up
set_original_theme()

# Function to show CPU and Memory usage graph
def show_graph(dark_mode=False):
    # Create a new window for the graph
    graph_window = tk.Toplevel(root)
    graph_window.title("CPU and Memory Usage Graph")
    graph_window.geometry("800x600")

    # Create a figure and axis for the graph
    fig, ax = plt.subplots()
    ax.set_title("CPU and Memory Usage Over Time")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Usage (%)")

    # Apply dark mode if selected
    if dark_mode:
        fig.patch.set_facecolor('#2e2e2e')
        ax.set_facecolor('#2e2e2e')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.legend(facecolor='#2e2e2e', edgecolor='white')

    # Create lists to store CPU and Memory usage data
    cpu_usage_data = []
    memory_usage_data = []
    time_data = []

    # Function to update the graph
    def update_graph():
        while True:
            # Get current CPU and Memory usage
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory().percent

            # Append data to the lists
            cpu_usage_data.append(cpu_usage)
            memory_usage_data.append(memory_usage)
            time_data.append(len(time_data))

            # Clear the axis and plot the updated data
            ax.clear()
            ax.plot(time_data, cpu_usage_data, label="CPU Usage", color='blue')
            ax.plot(time_data, memory_usage_data, label="Memory Usage", color='orange')
            ax.legend()

            # Apply dark mode if selected
            if dark_mode:
                ax.set_facecolor('#2e2e2e')
                ax.spines['bottom'].set_color('white')
                ax.spines['top'].set_color('white')
                ax.spines['right'].set_color('white')
                ax.spines['left'].set_color('white')
                ax.yaxis.label.set_color('white')
                ax.title.set_color('white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                ax.legend(facecolor='#2e2e2e', edgecolor='white')

            # Draw the updated graph
            canvas.draw()

            # Sleep for a short interval before updating again
            time.sleep(1)

    # Create a canvas to display the graph
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Add info text at the bottom of the window
    info_text = tk.Label(graph_window, text="This graph shows the CPU and Memory usage over time.\nCPU usage is shown in blue and Memory usage is shown in orange.", bg="white", fg="black", font=("Arial", 10))
    info_text.pack(side=tk.BOTTOM, pady=10)

    # Start a thread to update the graph
    threading.Thread(target=update_graph, daemon=True).start()

# Create fullscreen and minimize buttons
fullscreen_button = tk.Button(root, text="🗖", command=toggle_fullscreen, bg="#2c3e50", fg="white", font=("Arial", 12, "bold"), relief="flat", bd=0, highlightthickness=0)
fullscreen_button.place(relx=1.0, rely=0, anchor="ne")

minimize_button = tk.Button(root, text="🗕", command=minimize_window, bg="#2c3e50", fg="white", font=("Arial", 12, "bold"), relief="flat", bd=0, highlightthickness=0)
minimize_button.place(relx=0.98, rely=0, anchor="ne")

# Start the GUI event loop
root.mainloop()
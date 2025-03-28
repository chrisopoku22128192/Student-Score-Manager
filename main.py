import tkinter as tk
from tkinter import ttk, messagebox
from student_manager import StudentManager
from score_manager import ScoreManager
import atexit

# Tooltip helper function
def create_tooltip(widget, text):
    tooltip = tk.Toplevel(widget)
    tooltip.withdraw()  # Hide the tooltip initially
    tooltip.overrideredirect(True)  # Remove window decorations
    tooltip_label = ttk.Label(tooltip, text=text, background="yellow", relief="solid", borderwidth=1)
    tooltip_label.pack()

    def on_enter(event):
        tooltip.geometry(f"+{widget.winfo_rootx() + 20}+{widget.winfo_rooty() + 20}")
        tooltip.deiconify()  # Show the tooltip

    def on_leave(event):
        tooltip.withdraw()  # Hide the tooltip

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

# Initialize Managers
student_manager = StudentManager(host="localhost", user="root", password="mercyopk712", database="student_management")
score_manager = ScoreManager(host="localhost", user="root", password="mercyopk712", database="student_management")

# Ensure database connections are closed when the program exits
atexit.register(student_manager.close_connection)
atexit.register(score_manager.close_connection)

# Main Window
root = tk.Tk()
root.title("Student Score Manager")
root.geometry("500x400")

# Apply a theme
style = ttk.Style()
style.theme_use("clam")  # Use the "clam" theme (you can try other themes like "alt", "default", or "classic")

# Customize the Notebook (Tabbed Interface)
style.configure("TNotebook", background="lightblue")  # Background color of the notebook
style.configure("TNotebook.Tab", background="lightgray", foreground="black")  # Tab background and text color
style.map("TNotebook.Tab", background=[("selected", "white")])  # Background color of the selected tab

# Customize Buttons
style.configure("TButton", font=("Arial", 10), padding=5)  # Button font and padding

# Create Notebook (Tabbed Interface)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Tabs
student_tab = ttk.Frame(notebook)
score_tab = ttk.Frame(notebook)
stats_tab = ttk.Frame(notebook)

# Add Tabs to Notebook
notebook.add(student_tab, text="Student Management")
notebook.add(score_tab, text="Score Management")
notebook.add(stats_tab, text="Statistics & Visualization")

# Add a status bar
status_bar = ttk.Label(root, text="Ready", relief="sunken", anchor="w")
status_bar.pack(side="bottom", fill="x")

# Helper function to update the status bar
def update_status(message):
    status_bar.config(text=message)


# ================== STUDENT MANAGEMENT TAB ==================
def register_student():
    name = student_name_entry.get().strip()
    if name:
        student_manager.register_student(name)
        messagebox.showinfo("Success", f"Student '{name}' registered!")
        update_status(f"Student '{name}' registered successfully.")
    else:
        messagebox.showerror("Error", "Please enter a student name.")
        update_status("Failed to register student.")


def register_subject():
    subject = subject_entry.get().strip()
    if subject:
        student_manager.register_subject(subject)
        messagebox.showinfo("Success", f"Subject '{subject}' registered!")
        update_status(f"Subject '{subject}' registered successfully.")
    else:
        messagebox.showerror("Error", "Please enter a subject name.")
        update_status("Failed to register subject.")

# Create a frame to center the widgets
student_frame = ttk.Frame(student_tab)
student_frame.pack(expand=True, anchor="center")  # Center the frame in the tab

# Register Student Section
ttk.Label(student_frame, text="Student Name").grid(row=0, column=0, padx=10, pady=10, sticky="w")
student_name_entry = ttk.Entry(student_frame, width=30)
student_name_entry.grid(row=0, column=1, padx=10, pady=10)

register_student_button = ttk.Button(student_frame, text="Register Student", command=register_student)
register_student_button.grid(row=0, column=2, padx=10, pady=10)
create_tooltip(register_student_button, "Click to register a new student.")

# Register Subject Section
ttk.Label(student_frame, text="Subject Name").grid(row=1, column=0, padx=10, pady=10, sticky="w")
subject_entry = ttk.Entry(student_frame, width=30)
subject_entry.grid(row=1, column=1, padx=10, pady=10)

register_subject_button = ttk.Button(student_frame, text="Register Subject", command=register_subject)
register_subject_button.grid(row=1, column=2, padx=10, pady=10)
create_tooltip(register_subject_button, "Click to register a new subject.")


# ================== SCORE MANAGEMENT TAB ==================
def add_score():
    student = student_entry.get().strip()
    subject = subject_score_entry.get().strip()
    try:
        score = float(score_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid score.")
        update_status("Invalid score entered.")
        return

    success = score_manager.add_score(student, subject, score)
    if success:
        messagebox.showinfo("Success", f"Score added: {student} - {subject} : {score}")
        update_status(f"Score added for {student} in {subject}.")
    else:
        messagebox.showerror("Error", "Failed to add score. Ensure the student and subject are registered.")
        update_status("Failed to add score.")


def view_scores():
    scores = score_manager.get_scores()
    if not scores:
        messagebox.showinfo("Scores", "No scores available.")
        update_status("No scores available.")
    else:
        scores_text = "\n".join([f"Student: {row[0]}, Subject: {row[1]}, Score: {row[2]}" for row in scores])
        messagebox.showinfo("Scores", scores_text)
        update_status("Displayed all scores.")

# Create a frame to center the widgets
score_frame = ttk.Frame(score_tab)
score_frame.pack(expand=True, anchor="center")  # Center the frame in the tab

# Add Score Section
ttk.Label(score_frame, text="Student Name").grid(row=0, column=0, padx=10, pady=10, sticky="w")
student_entry = ttk.Entry(score_frame, width=30)
student_entry.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(score_frame, text="Subject Name").grid(row=1, column=0, padx=10, pady=10, sticky="w")
subject_score_entry = ttk.Entry(score_frame, width=30)
subject_score_entry.grid(row=1, column=1, padx=10, pady=10)

ttk.Label(score_frame, text="Score").grid(row=2, column=0, padx=10, pady=10, sticky="w")
score_entry = ttk.Entry(score_frame, width=30)
score_entry.grid(row=2, column=1, padx=10, pady=10)

add_score_button = ttk.Button(score_frame, text="Add Score", command=add_score)
add_score_button.grid(row=2, column=2, padx=10, pady=10)
create_tooltip(add_score_button, "Click to add a score for a student.")

view_scores_button = ttk.Button(score_frame, text="View Scores", command=view_scores)
view_scores_button.grid(row=3, column=1, padx=10, pady=10)
create_tooltip(view_scores_button, "Click to view all scores.")


# ================== STATISTICS & VISUALIZATION TAB ==================
stats_result_label = ttk.Label(stats_tab, text="", foreground="blue")

def calculate_statistics():
    subject = stats_entry.get().strip()
    if subject:
        stats = score_manager.calculate_statistics(subject)
        if stats:
            mean, median, mode, std_dev = stats
            stats_result_label.config(
                text=f"Subject: {subject}\nMean: {mean:.2f}\nMedian: {median:.2f}\nMode: {mode}\nStd Dev: {std_dev:.2f}"
            )
            update_status(f"Statistics calculated for {subject}.")
        else:
            stats_result_label.config(text="No data for this subject!")
            update_status(f"No data available for {subject}.")
    else:
        messagebox.showerror("Error", "Enter a subject to analyze.")
        update_status("Failed to calculate statistics. No subject entered.")


def visualize_scores():
    subject = subject_viz_entry.get().strip()
    if subject:
        score_manager.visualize_scores(subject)
        update_status(f"Visualized scores for {subject}.")
    else:
        messagebox.showerror("Error", "Enter a subject to visualize.")
        update_status("Failed to visualize scores. No subject entered.")


def show_available_subjects():
    subjects = student_manager.get_subjects()
    if subjects:
        messagebox.showinfo("Available Subjects", "Subjects:\n" + "\n".join(subjects))
        update_status("Displayed available subjects.")
    else:
        messagebox.showinfo("Available Subjects", "No subjects available.")
        update_status("No subjects available.")

# Create a frame to center the widgets
stats_frame = ttk.Frame(stats_tab)
stats_frame.pack(expand=True, anchor="center")  # Center the frame in the tab

# UI for Statistics & Visualization
ttk.Label(stats_frame, text="Enter Subject for Statistics").grid(row=0, column=0, padx=10, pady=10, sticky="w")
stats_entry = ttk.Entry(stats_frame, width=30)
stats_entry.grid(row=0, column=1, padx=10, pady=10)

calculate_statistics_button = ttk.Button(stats_frame, text="Calculate Statistics", command=calculate_statistics)
calculate_statistics_button.grid(row=0, column=2, padx=10, pady=10)
create_tooltip(calculate_statistics_button, "Click to calculate statistics for a subject.")

ttk.Label(stats_frame, text="Enter Subject for Visualization").grid(row=1, column=0, padx=10, pady=10, sticky="w")
subject_viz_entry = ttk.Entry(stats_frame, width=30)
subject_viz_entry.grid(row=1, column=1, padx=10, pady=10)

visualize_scores_button = ttk.Button(stats_frame, text="Visualize Scores", command=visualize_scores)
visualize_scores_button.grid(row=1, column=2, padx=10, pady=10)
create_tooltip(visualize_scores_button, "Click to visualize scores for a subject.")

show_subjects_button = ttk.Button(stats_frame, text="Show Available Subjects", command=show_available_subjects)
show_subjects_button.grid(row=2, column=1, padx=10, pady=10)
create_tooltip(show_subjects_button, "Click to view all available subjects.")

# Exit Button
exit_button = ttk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=10)
create_tooltip(exit_button, "Click to exit the application.")

# Run the application
root.mainloop()
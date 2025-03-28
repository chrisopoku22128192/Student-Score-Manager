
# Visualize Scores
def visualize_scores():
    subject = subject_viz_entry.get()
    if subject:
        score_manager.visualize_scores(subject)
    else:
        messagebox.showerror("Error", "Enter a subject to visualize.")

# UI Layout
tk.Label(root, text="Register Student").pack()
student_name_entry = tk.Entry(root)
student_name_entry.pack()
tk.Button(root, text="Register Student", command=register_student).pack()

tk.Label(root, text="Register Subject").pack()
subject_entry = tk.Entry(root)
subject_entry.pack()
tk.Button(root, text="Register Subject", command=register_subject).pack()

tk.Label(root, text="Add Score").pack()
student_entry = tk.Entry(root)
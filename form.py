import tkinter as tk
from tkinter import messagebox

def get_values():
    # Retrieve values from the input fields
    voronoi_area = entry_voronoi_area.get()
    rect_width = entry_rect_width.get()
    rect_height = entry_rect_height.get()
    elasticity_1 = entry_elasticity_1.get()
    young_modulus_1 = entry_young_modulus_1.get()
    elasticity_2 = entry_elasticity_2.get()
    young_modulus_2 = entry_young_modulus_2.get()
    
    # Display the values in a message box
    messagebox.showinfo("Input Values", 
                        f"Average Area of Voronoi Cells: {voronoi_area}\n"
                        f"Rectangle Width: {rect_width}\n"
                        f"Rectangle Height: {rect_height}\n"
                        f"Elasticity of First Material: {elasticity_1}\n"
                        f"Young's Modulus of First Material: {young_modulus_1}\n"
                        f"Elasticity of Second Material: {elasticity_2}\n"
                        f"Young's Modulus of Second Material: {young_modulus_2}")

# Create the main window
root = tk.Tk()
root.title("Material Properties Form")

# Set default font for labels
default_font = ("Segoe UI", 10)

# Create a frame to hold the form fields in two columns
form_frame = tk.Frame(root)
form_frame.pack(padx=20, pady=20)

# Create input fields with labels in two columns
label_voronoi_area = tk.Label(form_frame, text="Average Area of Voronoi Cells:", font=default_font)
label_voronoi_area.grid(row=0, column=0, sticky='e', padx=5, pady=5)
entry_voronoi_area = tk.Entry(form_frame)
entry_voronoi_area.grid(row=0, column=1, padx=5, pady=5)

label_rect_width = tk.Label(form_frame, text="Rectangle Width:", font=default_font)
label_rect_width.grid(row=1, column=0, sticky='e', padx=5, pady=5)
entry_rect_width = tk.Entry(form_frame)
entry_rect_width.grid(row=1, column=1, padx=5, pady=5)

label_rect_height = tk.Label(form_frame, text="Rectangle Height:", font=default_font)
label_rect_height.grid(row=2, column=0, sticky='e', padx=5, pady=5)
entry_rect_height = tk.Entry(form_frame)
entry_rect_height.grid(row=2, column=1, padx=5, pady=5)

label_elasticity_1 = tk.Label(form_frame, text="Elasticity of First Material:", font=default_font)
label_elasticity_1.grid(row=3, column=0, sticky='e', padx=5, pady=5)
entry_elasticity_1 = tk.Entry(form_frame)
entry_elasticity_1.grid(row=3, column=1, padx=5, pady=5)

label_young_modulus_1 = tk.Label(form_frame, text="Young's Modulus of First Material:", font=default_font)
label_young_modulus_1.grid(row=4, column=0, sticky='e', padx=5, pady=5)
entry_young_modulus_1 = tk.Entry(form_frame)
entry_young_modulus_1.grid(row=4, column=1, padx=5, pady=5)

label_elasticity_2 = tk.Label(form_frame, text="Elasticity of Second Material:", font=default_font)
label_elasticity_2.grid(row=5, column=0, sticky='e', padx=5, pady=5)
entry_elasticity_2 = tk.Entry(form_frame)
entry_elasticity_2.grid(row=5, column=1, padx=5, pady=5)

label_young_modulus_2 = tk.Label(form_frame, text="Young's Modulus of Second Material:", font=default_font)
label_young_modulus_2.grid(row=6, column=0, sticky='e', padx=5, pady=5)
entry_young_modulus_2 = tk.Entry(form_frame)
entry_young_modulus_2.grid(row=6, column=1, padx=5, pady=5)

# Create a button at the bottom
submit_button = tk.Button(root, text="Submit", command=get_values)
submit_button.pack(pady=10)

# Run the main loop
root.mainloop()

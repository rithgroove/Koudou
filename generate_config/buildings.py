import tkinter as tk
from tkinter import ttk
from RangeSlider.RangeSlider import RangeSliderH

# root window
root = tk.Tk()
# root.geometry("240x100")
root.title('Login')
root.resizable(0, 0)

# configure the grid
row_n = 0
# building_type, min_workhour, max_workhour, min_start_hour, max_start_hour, day, min_activity_per_week, max_activity_per_week, open_24_hours_chance


# username
name_label = ttk.Label(root, text="Name")
name_label.grid(column=0, row=row_n, sticky="w", padx=5, pady=5)
name_entry = ttk.Entry(root)
name_entry.grid(column=1, row=row_n, sticky="e", padx=5, pady=5)
row_n += 1

working_hours_label = ttk.Label(root, text="Work Hours")
working_hours_label.grid(column=0, row=row_n, sticky="w", padx=5, pady=5)
working_hours_entry = tk.Scale(root, from_= 0, to=24, orient=tk.HORIZONTAL, variable=int, showvalue=True)
working_hours_entry.grid(column=1, row=row_n, sticky="ew", padx=5, pady=0)
row_n += 1

start_hour_label = ttk.Label(root, text="Start Hour")
start_hour_label.grid(column=0, row=row_n, sticky="w", padx=5, pady=5)
start_hour_entry = ttk.Combobox(root, textvariable=tk.StringVar(), values= [m for m in range(24)], state="readonly")
start_hour_entry.grid(column=1, row=row_n, sticky="ew", padx=5, pady=5)
start_hour_max_entry = ttk.Combobox(root, textvariable=tk.StringVar(), values= [m for m in range(24)], state="readonly")
start_hour_max_entry.grid(column=2, row=row_n, sticky="ew", padx=5, pady=5)


row_n += 1

open_days_label = ttk.Label(root, text="Schedule")
open_days_label.grid(column=0, row=row_n, sticky="w", padx=5, pady=5)
open_days_entry = ttk.Entry(root)
open_days_entry.grid(column=1, row=row_n, sticky="e", padx=5, pady=5)
row_n += 1

activity_per_week_label = ttk.Label(root, text="# of days open per week")
activity_per_week_label.grid(column=0, row=row_n, sticky="w", padx=5, pady=5)
activity_per_week_entry = ttk.Entry(root)
activity_per_week_entry.grid(column=1, row=row_n, sticky="e", padx=5, pady=5)
row_n += 1

open_24h_label = ttk.Label(root, text="Chance of being 24h")
open_24h_label.grid(column=0, row=row_n, sticky="w", padx=5, pady=5)
open_24h_entry = ttk.Entry(root)
open_24h_entry.grid(column=1, row=row_n, sticky="e", padx=5, pady=5)
row_n += 1




# login button
login_button = ttk.Button(root, text="Login")
login_button.grid(column=1, row=row_n, sticky="e", padx=5, pady=5)


root.mainloop()

# -*- coding: utf-8 -*-
"""


@author: Michael Call 
"""

import tkinter as tk
from tkinter import ttk

def calculate_firing_solution():
    try:
        caliber = caliber_var.get()
        distance = int(distance_var.get())
        wind_speed = float(wind_speed_var.get())
        wind_angle = float(wind_angle_var.get())
        latitude = float(latitude_var.get())
        shooting_angle = float(shooting_angle_var.get())
        temperature = float(temperature_var.get())
        altitude = float(altitude_var.get())
        bullet_weight = float(bullet_weight_var.get())
        muzzle_velocity = float(muzzle_velocity_var.get())

        bullet_path_inches = get_bullet_path_data(caliber, distance)
        if bullet_path_inches is None:
            result_var.set("No data available for the selected distance and caliber.")
            return
        
        adjusted_bullet_path_inches = adjust_for_environmental_factors(distance, bullet_path_inches, temperature, altitude)
        elevation_mils, clicks = calculate_elevation_knob_setting(distance, adjusted_bullet_path_inches)
        windage_mils = calculate_windage_adjustment(distance, wind_speed, wind_angle, muzzle_velocity)
        coriolis_mils = calculate_coriolis_effect(latitude, distance, shooting_angle)
        
        result_var.set(
            f"Distance: {distance} yards\n"
            f"Bullet Path: {bullet_path_inches:.2f} inches\n"
            f"Mil Equivalent: {calculate_mil_equivalent(distance):.2f} inches\n"
            f"Elevation: {elevation_mils:.2f} mils ({clicks} clicks)\n"
            f"Windage: {windage_mils:.2f} mils\n"
            f"Coriolis Effect: {coriolis_mils:.2f} mils"
        )
    except ValueError:
        result_var.set("Please enter valid numerical values.")

def true_firing_solution():
    try:
        observed_impact_inches = float(observed_impact_var.get())
        distance = int(distance_var.get())
        
        mil_equivalent = calculate_mil_equivalent(distance)
        correction_mils = observed_impact_inches / mil_equivalent
        correction_clicks = round(correction_mils * 10)
        
        result_var.set(
            f"Truing Correction:\n"
            f"Correction: {correction_mils:.2f} mils ({correction_clicks} clicks)"
        )
    except ValueError:
        result_var.set("Please enter valid numerical values for truing.")

# Create the main application window
root = tk.Tk()
root.title("Ballistic Firing Solution Calculator")
root.geometry("500x600")
root.resizable(False, False)

# Variables for user input
caliber_var = tk.StringVar()
distance_var = tk.StringVar()
wind_speed_var = tk.StringVar()
wind_angle_var = tk.StringVar()
latitude_var = tk.StringVar()
shooting_angle_var = tk.StringVar()
temperature_var = tk.StringVar()
altitude_var = tk.StringVar()
bullet_weight_var = tk.StringVar()
muzzle_velocity_var = tk.StringVar()
observed_impact_var = tk.StringVar()
result_var = tk.StringVar()

# Styling
style = ttk.Style()
style.configure("TLabel", font=("Arial", 10))
style.configure("TButton", font=("Arial", 10))

# Create and place the input fields and labels
fields = [
    ("Caliber", caliber_var, ["", ".308 Winchester", ".243 Winchester", "6.5 Creedmoor", ".223 Remington", ".30-06 Springfield", 
                             ".300 Win Mag", ".338 Lapua Magnum", ".22 LR", "7mm Rem Mag", ".270 Winchester", 
                             ".300 AAC Blackout", "6.5 PRC", "7.62x39mm", ".450 Bushmaster", "6mm Creedmoor", 
                             "7.62x54mmR", ".458 SOCOM", ".50 BMG", ".224 Valkyrie", ".45-70 Govt", 
                             ".350 Legend", ".300 RUM", ".375 H&H", ".30-30 Winchester"]),
    ("Distance (yards)", distance_var),
    ("Wind Speed (mph)", wind_speed_var),
    ("Wind Angle (degrees)", wind_angle_var),
    ("Latitude (degrees)", latitude_var),
    ("Shooting Angle (degrees)", shooting_angle_var),
    ("Temperature (F)", temperature_var),
    ("Altitude (feet)", altitude_var),
    ("Bullet Weight (grains)", bullet_weight_var),
    ("Muzzle Velocity (fps)", muzzle_velocity_var),
    ("Observed Impact (inches)", observed_impact_var)
]

row = 0
for label_text, var, *combobox_options in fields:
    ttk.Label(root, text=f"{label_text}:").grid(column=0, row=row, padx=10, pady=5, sticky=tk.W)
    if combobox_options:
        ttk.Combobox(root, textvariable=var, values=combobox_options[0]).grid(column=1, row=row, padx=10, pady=5)
    else:
        ttk.Entry(root, textvariable=var).grid(column=1, row=row, padx=10, pady=5)
    row += 1

# Button to calculate the firing solution
ttk.Button(root, text="Calculate", command=calculate_firing_solution).grid(column=0, row=row, columnspan=2, padx=10, pady=10)

# Button to true the firing solution
row += 1
ttk.Button(root, text="True Solution", command=true_firing_solution).grid(column=0, row=row, columnspan=2, padx=10, pady=10)

# Label to display the results
row += 1
ttk.Label(root, textvariable=result_var, justify="left", font=("Arial", 10, "bold"), wraplength=450).grid(column=0, row=row, columnspan=2, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()

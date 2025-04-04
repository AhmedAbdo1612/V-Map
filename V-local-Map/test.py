import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import flet as ft
import numpy as np
import io
import base64
import time  # For simulating a delay during app startup

def draw_line_matplotlib(distance1, distance2, direction1, direction2, scale=1.0):
    # Your existing matplotlib plotting code here
    parameter_separate = 2.23
    radius_km = 50
    fig, ax = plt.subplots(figsize=(14, 14))
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, alpha=1)
    circle = plt.Circle((0, 0), radius_km, edgecolor='blue', facecolor='lightblue', lw=2)
    ax.add_patch(circle)
    plt.scatter(0, 0, color="red", label='Point', s=100, zorder=5)
    rad1 = np.radians(direction1)
    x1 = distance1 * np.cos(rad1)
    y1 = distance1 * np.sin(rad1)
    plt.scatter(x1, y1, s=50, zorder=5, color="green", marker="x")
    rad2 = np.radians(direction2)
    x2 = distance2 * np.cos(rad2)
    y2 = distance2 * np.sin(rad2)
    a = y2 - y1
    b = x1 - x2
    c = (x2 * y1) - (x1 * y2)
    p = abs(round(2 * ((x2 * y1) - (x1 * y2)) / (np.sqrt(a**2 + b**2)) / 2.23))
    plt.title(f"The Parameter is {p}", fontsize=30, color="red", fontweight='bold')
    plt.scatter(x2, y2, s=50, zorder=5, color="green", marker="x")
    plt.plot([x1, x2], [y1, y2], color="red", linewidth=2, label="Horizontal Line")
    limit = radius_km * 1.1
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_xlabel("Distance (Km)")
    ax.set_ylabel("Distance (Km)")
    for angle in range(0, 360, 10):
        rad = np.radians(angle)
        x_text = (radius_km + 3) * np.cos(rad)
        y_text = (radius_km + 3) * np.sin(rad)
        ax.text(x_text, y_text, f"{angle}°", ha='center', va='center', fontsize=12, color="red")
    line_slope = (y2 - y1) / (x2 - x1)
    angle = np.arctan(line_slope) - np.radians(90)
    for i in range(1, 13):
        x = i * parameter_separate * np.cos(angle)
        y = i * parameter_separate * np.sin(angle)
        intercept = y - line_slope * x
        x1 = 80 + parameter_separate * i
        x2 = -80 - parameter_separate * i
        y1 = line_slope * x1 + intercept
        y2 = line_slope * x2 + intercept
        x_parameter_label = 5
        y_parameter_label = line_slope * x_parameter_label + intercept
        ax.text(x, y, f"{i*2}", ha='center', va='center', fontsize=12, color="blue")
        ax.text(-x, -y, f"{i*2}", ha='center', va='center', fontsize=12, color="blue")
        plt.plot([x1, x2], [y1, y2], color="orange", linewidth=1, label="Horizontal Line")
        plt.plot([-x1, -x2], [-y1, -y2], color="orange", linewidth=1, label="Horizontal Line")
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.read()
    plt.close(fig)
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    return base64_image, p

def main(page: ft.Page):
    # Set up the page
    page.title = "Volga Map"
    page.theme_mode = ft.ThemeMode.DARK

    # Add a loading bar and a loading message
    loading_bar = ft.ProgressBar(width=400, value=0, visible=True)
    loading_text = ft.Text("Loading app...", size=20, color="white")
    page.add(ft.Column([loading_text, loading_bar], alignment=ft.MainAxisAlignment.CENTER))

    # Simulate a delay (e.g., loading resources or initializing the app)
    for i in range(101):
        time.sleep(0.05)  # Simulate a delay
        loading_bar.value = i / 100  # Update the progress bar
        page.update()
        
    def update_chart(e=None):
        try:
            dist1 = float(distance1.value)
            dist2 = float(distance2.value)
            dir1 = float(direction1.value)
            dir2 = float(direction2.value)

            base64_image, parameter = draw_line_matplotlib(dist1, dist2, dir1, dir2)
            chart_image.src_base64 = base64_image
            parameter_label.value = f"The Parameters is: {parameter}"
            page.update()

        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid input. Please enter numbers."))
            page.snack_bar.open = True
            page.update()

    # Once the app is loaded, remove the loading bar and add the main UI
    page.clean()  # Clear the loading screen
    page.add(
        ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(controls=[
                        ft.TextField(label="The First Distance", width=200, keyboard_type="number", expand=True, value="20", text_style=ft.TextStyle(color="#FFFF00"), border_color="#FFFFFF"),
                        ft.TextField(label="The First Direction", width=200, keyboard_type="number", expand=True, value="35", text_style=ft.TextStyle(color="#FFFF00"), border_color="#FFFFFF"),
                    ]),
                    padding=ft.padding.only(top=65, left=10, right=10),
                ),
                ft.Container(
                    content=ft.Row(controls=[
                        ft.TextField(label="The Second Distance", width=200, keyboard_type="number", expand=True, value="30", text_style=ft.TextStyle(color="#FFFF00"), border_color="#FFFFFF"),
                        ft.TextField(label="The Second Direction", width=200, keyboard_type="number", expand=True, value="315", text_style=ft.TextStyle(color="#FFFF00"), border_color="#FFFFFF"),
                    ]),
                    padding=ft.padding.only(left=10, right=10, top=20),
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.ElevatedButton("Update Chart", on_click=update_chart, bgcolor="#FFFFFF", color="#000000"),
                        ft.Text("The Parameters is: 16", weight=ft.FontWeight.BOLD, color="#00FF00", size=16, expand_loose=True),
                    ],
                ),
                ft.Container(
                    content=ft.InteractiveViewer(ft.Image(src="./assets/initial.png"), max_scale=5),
                    padding=ft.padding.only(top=10),
                ),
            ],
            expand=True,
        )
    )

    
# Run the app
ft.app(target=main)
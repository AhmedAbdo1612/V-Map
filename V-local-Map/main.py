import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import flet as ft
import numpy as np
import io
import base64 # Import the base64 module
def draw_line_matplotlib(distance1, distance2, direction1, direction2, scale=1.0):
   
    # fig, ax = plt.subplots(figsize=(10,10))
    parameter_separate = 2.23
    radius_km = 50
    fig, ax = plt.subplots(figsize = (14,14))
    ax.set_aspect('equal', adjustable='box')
    # Set the grid for reference
    ax.grid(True, alpha=1)
    # Draw the circle using the scaled radius
    circle = plt.Circle((0, 0), radius_km , edgecolor='blue', facecolor='lightblue', lw=2)
    ax.add_patch(circle)
    plt.scatter(0,0, color="red", label='Point', s=100, zorder=5)
    rad1 = np.radians(direction1)
    x1 = distance1*np.cos(rad1)
    y1 = distance1*np.sin(rad1)
    plt.scatter(x1,y1, s=50, zorder=5,color="green",marker="x")
    rad2 = np.radians(direction2)
    x2 = distance2*np.cos(rad2)
    y2 = distance2*np.sin(rad2)
    a = y2 -y1 
    b = x1 -x2
    c = (x2*y1) - (x1*y2)
    p = abs(round(2*((x2*y1) - (x1*y2))/(np.sqrt(a**2 + b**2))/2.23))
   
    plt.title(f"The Parameter is {p}",fontsize=30,color = "red",fontweight='bold')
    plt.scatter(x2,y2, s=50, zorder=5,color="green",marker="x")
    plt.plot([x1,x2], [y1,y2], color="red", linewidth=2, label="Horizontal Line")
    limit = radius_km *1.1  # 10% padding for better view
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    
    ax.set_xlabel("Distance (Km)")
    ax.set_ylabel("Distance (Km)")
    
    for angle in range(0, 360, 10):
        rad = np.radians(angle)
        x_text = (radius_km+3 ) * np.cos(rad)
        y_text = (radius_km+3 ) * np.sin(rad)
        ax.text(x_text, y_text, f"{angle}°", ha='center', va='center', fontsize=12, color="red")

    line_slope = (y2-y1)/(x2-x1)
    angle = np.arctan(line_slope)-np.radians(90)
    for i in range(1,13):
  
        x = i*parameter_separate*np.cos(angle)
        y = i*parameter_separate*np.sin(angle)
        intercept = y - line_slope*x
        #         plt.scatter(x,y, color="blue", label='Point', s=50, zorder=5)
        
        x1 = 80+parameter_separate*i
        x2 = -80-parameter_separate*i
        y1 = line_slope*x1 + intercept
        y2 = line_slope*x2 + intercept
        x_parameter_label = 5
        y_parameter_label = line_slope*x_parameter_label + intercept
        ax.text(x,y , f"{i*2}", ha='center', va='center', fontsize=12, color="blue")
        ax.text(-x, -y , f"{i*2}", ha='center', va='center', fontsize=12, color="blue")
        plt.plot([x1,x2], [y1,y2], color="orange", linewidth=1, label="Horizontal Line")
        plt.plot([-x1,-x2], [-y1,-y2], color="orange", linewidth=1, label="Horizontal Line")

    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.read()
    plt.close(fig)

    # Base64 encode the image bytes and decode to UTF-8 string
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    return base64_image,p

def main(page: ft.Page):
    # Set the title of the app
    page.title = "Volga Map"
    page.theme_mode = ft.ThemeMode.DARK
    distance1 = ft.TextField(label="The First Distance",
                             width=200,
                             keyboard_type="number",
                             expand=True,value="20",
                             text_style=ft.TextStyle(color="#FFFF00"),
                             border_color="#FFFFFF")
    
    direction1 = ft.TextField(label="The First Direction",
                              width=200, keyboard_type="number",
                              expand=True,value="35",
                             text_style=ft.TextStyle(color="#FFFF00"),
                             border_color="#FFFFFF")
    
    distance2 = ft.TextField(label="The Second Distance",
                             width=200, keyboard_type="number",
                             expand=True,value="30",
                             text_style=ft.TextStyle(color="#FFFF00"),
                             border_color="#FFFFFF")
    direction2 = ft.TextField(label="The Second Direction",
                              width=200, keyboard_type="number",
                              expand=True,value="315",
                             text_style=ft.TextStyle(color="#FFFF00"),
                             border_color="#FFFFFF")
    
    chart_image = ft.Image(src="./assets/initial.png")
    parameter_label = ft.Text("The Parameters is: 16", weight=ft.FontWeight.BOLD, color="#00FF00",size=16,expand_loose=True)
    def update_chart(e =None):
        try:
           
            dist1 = float(distance1.value)
            dist2 = float(distance2.value)
            dir1 = float(direction1.value)
            dir2 = float(direction2.value)

            base64_image, parameter = draw_line_matplotlib(dist1, dist2, dir1, dir2) # Get base64 encoded image string
            chart_image.src_base64 = base64_image # Set image source to base64 string
            parameter_label.value = f"The Parameters is: {parameter}"
            page.update()

        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid input. Please enter numbers."))
            page.snack_bar.open = True
            page.update()
            
    # update_chart()
    update_button = ft.ElevatedButton("Update Chart",
                                      on_click=update_chart,
                                      bgcolor="#FFFFFF",
                                      color="#000000"
                                     )
    
    page.add(
        ft.Column(expand=True,
            controls=[
                ft.Container(  # First Row Container - Padding for the first row
                    content=ft.Row(
                        controls=[
                            distance1,
                            direction1,
                        ],
                    ),
                    padding=ft.padding.only(top=65,left=10,right=10),  # Padding for row 1
                ),
                ft.Container(  # Second Row Container - Padding for the second row (modified here)
                    content=ft.Row(
                        controls=[
                            distance2,
                            direction2,
                        ],
                    ),
                    padding=ft.padding.only(left=10,right=10,top=20),  # Different padding for row 2
                ),
                ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[update_button,parameter_label]),
                 ft.Container(    content=ft.InteractiveViewer(chart_image,max_scale=5,),padding=ft.padding.only(top=10),),
                 ])
    )
# Run the app
ft.app(target=main,)
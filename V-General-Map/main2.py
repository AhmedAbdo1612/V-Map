import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import flet as ft
import numpy as np
import io
import base64 # Import the base64 module
def plot_map(bat_loc:str,tar_loc:str):
    
    fig, ax = plt.subplots(figsize=(10,8))
    plt.axis("off")
    x_axis =["R","P","O","N",]
    x_axis.reverse()
    y_axis = ["U","T","S","R","Q"]
    y_axis.reverse()

    for i in range(0,len(x_axis)):
        x = i+1
        plt.plot([x*96,x*96],[0,550],color= "red",linewidth = 2)
        # plt.plot([0,450],[96*i,96*i],color= "red")
        plt.text(x*96-54,560 , f"{x_axis[i]}", fontsize=18, color="blue",fontweight="bold")
        
    for i in range(0,len(y_axis)):
        x = i+1
        plt.plot([0,400],[108*x,108*x],color= "red",linewidth = 2)
        plt.text(-20,x*108-48 , f"{y_axis[i]}", fontsize=18, color="blue",fontweight="bold")
        
    for i in range(25):
        plt.plot([i*16,i*16],[0,550],color= "green",zorder=1)
        
    for i in range(1,31):
        plt.plot([0,400],[18*i,18*i],color= "green",zorder=1)

    #the test point is SS444
    def get_coordinates(o:str):
        o = o.upper() 
        x = x_axis.index(o[1])
        y = y_axis.index(o[0])
        
        y = y*108 +18*(int(o[2]))
        x = x*96 + 16*(int(o[3]))
        v = int(o[-1])
        if v in [4,9,8]:
            x = x+5.3
        if v in [5,6,7]:
            x = x+2*5.3
        if(v in [2,9,6]):
            y  = y+6
        if v in [3,4,5]:
            y = y+2*6
        return x,y 
    x1,y1 =get_coordinates(bat_loc)
    x2,y2= get_coordinates(tar_loc)
    distance =np.sqrt((x1-x2)**2 + (y1-y2)**2)
    
    plt.text(x1-9,y1-10,s ="O",color = "blue",zorder=4,fontsize = 28,fontweight = "bold")
    plt.scatter(x2,y2,color = "blue",s=100,zorder=4,marker="x")
    plt.plot([x1,x2],[y1,y2],linewidth = 3)
 
    angles_loc = []
    for angle in range(0, 360, 10):
        rad = np.radians(abs(360-angle+90))
        x_text = (distance ) * np.cos(rad)+x1
        y_text = (distance) * np.sin(rad)+y1
        angles_loc.append((abs(x_text-x2)+abs(y_text-y2)))
        # ax.text(x_text, y_text, f"{angle}°", ha='center', va='center', fontsize=10, color="red",)

    angle = angles_loc.index(min(angles_loc))*10
    plt.title(f"The Distance is {int(distance)}km with Direction {angle}°\n",fontsize = 16,fontweight = "bold")
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    plt.tight_layout()
    plt.savefig("./assets/initial.png")
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.read()
    plt.close(fig)
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    return base64_image

def main(page: ft.Page):
    # Set the title of the app
    page.title = "Volga General Map"
    page.theme_mode = ft.ThemeMode.DARK
    init_loc = "so414"
    try:
        with open("./assets/cache.txt","r") as f:
            init_loc = f.readlines()[0]
            f.close()
    except Exception:pass
    bat_loc = ft.TextField(label="The Battalion Location",
                             width=200,
                             keyboard_type="string",
                             expand=True,value=init_loc,
                             text_style=ft.TextStyle(color="#FFFF00"),
                             border_color="#FFFFFF")
    
    target_loc = ft.TextField(label="The Target Location",
                              width=200, keyboard_type="string",
                              expand=True,value="un338",
                             text_style=ft.TextStyle(color="#FFFF00"),
                             border_color="#FFFFFF")
    
    
    chart_image = ft.Image(src="./assets/initial.png")
    # parameter_label = ft.Text("The Parameters is: 16", weight=ft.FontWeight.BOLD, color="#00FF00",size=16,expand_loose=True)
    def update_chart(e =None):
        try:
            loc1 = str(bat_loc.value)
            loc2 = str(target_loc.value)
            base64_image = plot_map(loc1,loc2) # Get base64 encoded image string
            with open("./assets/cache.txt","w") as f:
                f.writelines([loc1])
                f.close()
            chart_image.src_base64 = base64_image # Set image source to base64 string
            page.update()

        except ValueError as e:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid input. Please enter valid inputs"))
            page.snack_bar.open = True
            page.update()
            
    # update_chart()
    update_button = ft.ElevatedButton("Update Chart",
                                      on_click=update_chart,
                                      bgcolor="#FFFFFF",
                                      color="#000000",
                                      expand=True,
                                      height=40
                                     )
    page.add(
        ft.Column(expand=True,
            controls=[
                ft.Container(  # First Row Container - Padding for the first row
                    content=ft.Row(controls=[bat_loc,target_loc],),
                    padding=ft.padding.only(top=65,left=10,right=10),  # Padding for row 1
                     ),
                ft.Container(content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[update_button]),
                             padding=ft.padding.only(top=15,left=10,right=10)),
                 ft.Container(    content=ft.InteractiveViewer(chart_image,max_scale=5,),padding=ft.padding.only(top=10),),
                 ])
    )
# Run the app
ft.app(target=main,)
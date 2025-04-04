import matplotlib.pyplot as plt
import numpy as np
import math
def plot_map(bat_loc:str,tar_loc:str):
    
    fig, ax = plt.subplots(figsize = (6,8))
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
    x1,y1 =get_coordinates("rn435")
    x2,y2= get_coordinates("so414")
    distance =np.sqrt((x1-x2)**2 + (y1-y2)**2)
    plt.title(f"The Distance is {int(distance)}")
    plt.scatter(x1,y1,color = "blue",s=25,zorder=4)
    plt.scatter(x2,y2,color = "blue",s=25,zorder=4)
    plt.plot([x1,x2],[y1,y2],linewidth = 3)
    circle = plt.Circle((x2, y2), distance , edgecolor='blue', facecolor='lightblue', lw=2,fill=False)
    ax.add_patch(circle)
    for angle in range(0, 360, 10):
        rad = np.radians(abs(360-angle+90))
        x_text = (distance+10 ) * np.cos(rad)+x2
        y_text = (distance+10) * np.sin(rad)+y2
        ax.text(x_text, y_text, f"{angle}°", ha='center', va='center', fontsize=10, color="red",)
    buf = io.BytesIO()
    
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_bytes = buf.read()
    plt.close(fig)
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    return base64_image,int(distance)
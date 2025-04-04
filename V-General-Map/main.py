import flet as ft
import numpy as np
import io
import base64  # Import the base64 module
from datetime import date

def plot_map(bat_loc: str, tar_loc: str,x_axis:list,y_axis:list):
    
    def get_coordinates(o: str):
        o = o.upper()
        x = x_axis.index(o[1])
        y = y_axis.index(o[0])
        y = y * 108 + 18 * (int(o[2]))
        x = x * 96 + 16 * (int(o[3]))
        v = int(o[-1])
        if v in [4, 9, 8]:
            x = x + 5.3
        if v in [5, 6, 7]:
            x = x + 2 * 5.3
        if v in [2, 9, 6]:
            y = y + 6
        if v in [3, 4, 5]:
            y = y + 2 * 6
        return x, y

    x1, y1 = get_coordinates(bat_loc)
    x2, y2 = get_coordinates(tar_loc)
    distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    angles_loc = []
    for angle in range(0, 360, 10):
        rad = np.radians(abs(360 - angle + 90))
        x_text = (distance) * np.cos(rad) + x1
        y_text = (distance) * np.sin(rad) + y1
        angles_loc.append((abs(x_text - x2) + abs(y_text - y2)))

    angle = angles_loc.index(min(angles_loc)) * 10

    return int(distance), angle


def main(page: ft.Page):
    page.title = "Volga General Map"
    page.theme_mode = ft.ThemeMode.DARK
    if(date.today()>date(2025,5,20)):
        return page.add(ft.Text(
        "Application Expired",
        weight=ft.FontWeight.BOLD,
        color="Red",
        size=18,
        expand_loose=True,
             ))
    bat_loc_init = page.client_storage.get("bat-location") or "so414"
    target_loc_init = page.client_storage.get("target-location") or "tp555"
    # page.client_storage.set("x-axis","".join("".join(["N", "O", "P", "R"])))
    # page.client_storage.set("y-axis","".join("".join(["Q","R","S","T","U"])))
    x_axis_values = page.client_storage.get("x-axis") or "".join(["N", "O", "P", "R"])
    y_axis_values = page.client_storage.get("y-axis") or "".join(["Q","R","S","T","U"])
    
    bat_loc_input = ft.TextField(
        label="The Battalion Location",
        width=200,
        keyboard_type="string",
        expand=True,
        value=bat_loc_init,
        text_style=ft.TextStyle(color="#FFFF00"),
        border_color="#FFFFFF",
    )

    target_loc_input = ft.TextField(
        label="The Target Location",
        width=200,
        keyboard_type="string",
        expand=True,
        value=target_loc_init,
        text_style=ft.TextStyle(color="#FFFF00"),
        border_color="#FFFFFF",
    )

    x_labels_input = ft.TextField(
        label="The X Axis Labels",
        width=200,
        keyboard_type="string",
        expand=True,
        value=x_axis_values,
        text_style=ft.TextStyle(color="#FFFF00"),
        border_color="#FFFFFF",
    )

    y_labels_input = ft.TextField(
        label="The Y Axis Labels",
        width=200,
        keyboard_type="string",
        expand=True,
        value=y_axis_values,
        text_style=ft.TextStyle(color="#FFFF00"),
        border_color="#FFFFFF",
    )

    def close_error_dialog(e):
        page.dialog.open = False
        page.update()

    error_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Input Error"),
        content=ft.Text("Please enter valid Inputs"),
        actions=[
            ft.TextButton("OK", on_click=close_error_dialog),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    target_loc_label = ft.Text(
        "",
        weight=ft.FontWeight.BOLD,
        color="#00FF00",
        size=16,
        expand_loose=True,
    )

    def update_chart(e=None):
        try:
            loc1 = str(bat_loc_input.value)
            loc2 = str(target_loc_input.value)
            x_axis_values = list(x_labels_input.value.upper())
            y_axis_values = list(y_labels_input.value.upper())
            y_axis_values.reverse()
            distance, direction = plot_map(loc1, loc2,x_axis_values,y_axis_values)
            page.client_storage.set("bat-location", loc1)
            page.client_storage.set("target-location", loc2)
            target_loc_label.value = (
                f" Distance  {distance}km and direction  {direction}°"
                    )
            page.update()
            y_axis_values.reverse()
            if(x_axis_values != page.client_storage.get("x-axis") and y_axis_values != page.client_storage.get("y-axis") ):
                page.client_storage.set("x-axis" , "".join(x_axis_values))
                page.client_storage.set("y-axis" , "".join(y_axis_values))
        except ValueError as e:
            page.dialog = error_dialog
            page.dialog.open = True
            page.update()

    # update_chart()
    update_button = ft.ElevatedButton(
        "Update Chart",
        on_click=update_chart,
        bgcolor="#FFFFFF",
        color="#000000",
        expand=True,
        height=40,
    )
    page.add(
        ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[bat_loc_input, target_loc_input, error_dialog],
                    ),
                    padding=ft.padding.only(
                        top=65, left=10, right=10
                    ),  # Padding for row 1
                ),
                ft.Container(
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER, controls=[update_button]
                    ),
                    padding=ft.padding.only(top=15, left=10, right=10),
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[target_loc_label],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.only(top=10),
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[x_labels_input, y_labels_input],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.only(top=10),
                ),
            ],
        )
    )


# Run the app
ft.app(
    target=main,
)

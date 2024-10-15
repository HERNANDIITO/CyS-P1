from pathlib import Path
from tkinter import PhotoImage, Button, Canvas


# Definir el path base relativo a la ubicación del archivo actual
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "imgs" / "subir_archivo"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def subir_archivo(app):
    canvas = Canvas(
        app,
        bg="#000000",
        height=400,
        width=600,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)

    # Cargar la imagen utilizando el path relativo
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    
    image_1 = canvas.create_image(
        300.0,
        200.0,
        image=image_image_1
    )

    canvas.create_rectangle(
        17.0,
        10.0,
        577.0,
        390.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_text(
        180.0,
        75.0,
        anchor="nw",
        text="Sube tus archivos y encriptalos aquí",
        fill="#606060",
        font=("KantumruyPro Medium", 15 * -1)
    )

    # Cargar los botones utilizando el path relativo
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))

    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )

    button_1.place(
        x=182.0,
        y=129.0,
        width=237.0,
        height=38.0
    )

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))

    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_2 clicked"),
        relief="flat"
    )

    button_2.place(
        x=181.0,
        y=233.0,
        width=237.0,
        height=38.0
    )

    canvas.create_text(
        65.0,
        39.0,
        anchor="nw",
        text="ENCRIPTACIÓN DE ARCHIVOS",
        fill="#601E88",
        font=("KantumruyPro Medium", 32 * -1)
    )
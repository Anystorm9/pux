import time
import random
from sikuli import *

similarity = 0.8

# 🔹 Patrón especial
click4_pattern = Pattern("7.png").similar(similarity)

templates = [
    {"name": "img0", "buscar": "18.png", "click": "19.png"},
    {"name": "img1", "buscar": "1.png", "click": "2.png"},
    {"name": "img2", "buscar": "3.png", "click": "4.png"},
    {"name": "img3", "buscar": "5.png", "click": "6.png"},
    {"name": "img5", "buscar": "8.png", "click": "8.png"},
    {"name": "img6", "buscar": "9.png", "click": "10.png"}
]

# 🔹 Movimiento humano REAL (sin romper clicks)
def move_mouse_human(match):
    loc = match.getCenter()
    mouse_location = Env.getMouseLocation()  # Obtener la ubicación actual del ratón
    x1, y1 = mouse_location.getX(), mouse_location.getY()  # Extraer las coordenadas x e y
    x2, y2 = loc.getX(), loc.getY()

    steps = random.randint(18, 28)

    for i in range(steps):
        t = i / float(steps)

        # Curva suave + pequeña desviación
        offset_x = random.randint(-2, 2) * (1 - t)
        offset_y = random.randint(-2, 2) * (1 - t)

        x = int(x1 + (x2 - x1) * t + offset_x)
        y = int(y1 + (y2 - y1) * t + offset_y)

        Mouse.move(Location(x, y))  # Usar Mouse.move para mover el ratón a la nueva ubicación
        wait(random.uniform(0.008, 0.02))

# 🔹 micro-movimientos antes del click
def micro_pause():
    wait(random.uniform(0.2, 0.5))

# 🔹 espera humana
def wait_human(a=1, b=3):
    wait(random.uniform(a, b))

# 🔹 scroll humano (sin mover mouse lejos)
def scroll_human():
    type(Key.DOWN)
    wait(random.uniform(0.3, 0.6))

# 🔁 LOOP PRINCIPAL
while True:
    encontrado = False

    # 🔥 LÓGICA INICIAL (INTACTA)
    try:
        pattern_16 = Pattern("16.png").similar(similarity)
        match_16 = exists(pattern_16, 2)

        if match_16:
            move_mouse_human(match_16)
            micro_pause()
            click(match_16)
            print("✅ Click en 16.png")

            wait_human(2, 4)

            pattern_17 = Pattern("17.png").similar(similarity)
            match_17 = exists(pattern_17, 2)

            if match_17:
                move_mouse_human(match_17)
                micro_pause()
                click(match_17)
                print("✅ Click en 17.png")
            else:
                print("⚠️ No apareció 17.png")
        else:
            print("⚠️ No apareció 16.png")

    except:
        print("⚠️ Error en lógica inicial, continuando...")

    # 🔹 LÓGICA PRINCIPAL
    start_time_total = time.time()
    timeout_total = 16

    while time.time() - start_time_total < timeout_total and not encontrado:

        for temp in templates:
            pattern_buscar = Pattern(temp["buscar"]).similar(similarity)
            match_buscar = exists(pattern_buscar, 0.5)

            if match_buscar:
                pattern_click = Pattern(temp["click"]).similar(similarity)

                # 🔹 Scroll
                if temp["name"] in ["img0", "img1", "img2", "img3", "img5", "img6"]:
                    start_time_scroll = time.time()
                    timeout_scroll = 8

                    while True:
                        match_click = exists(pattern_click, 0)
                        if match_click:
                            break

                        scroll_human()

                        if time.time() - start_time_scroll > timeout_scroll:
                            print("⏱️ Tiempo de scroll agotado para {}".format(temp["name"]))
                            break

                # 🔹 Click principal
                match_click = exists(pattern_click, 2)

                if match_click:

                    move_mouse_human(match_click)
                    micro_pause()

                    # 🔥 CASO ESPECIAL img0
                    if temp["name"] == "img0":
                        click(match_click)
                        print("Se encontró img0 y se hizo click en 19.png")

                        wait_human(2.5, 4)

                        pattern_20 = Pattern("20.png").similar(similarity)
                        match_20 = exists(pattern_20, 2)

                        if match_20:
                            move_mouse_human(match_20)
                            micro_pause()
                            click(match_20)
                            print("👉 Click en 20.png después de esperar")
                        else:
                            print("⚠️ 20.png no apareció")

                        encontrado = True
                        break

                    # 🔹 LÓGICA NORMAL
                    click(match_click)
                    print("Se encontró {} y se hizo click en {}".format(temp["name"], temp["click"]))

                    # 🔥 CASO img3
                    if temp["name"] == "img3":
                        wait_human(2.5, 4)

                        match_c4 = exists(click4_pattern, 2)
                        if match_c4:
                            move_mouse_human(match_c4)
                            micro_pause()
                            click(match_c4)
                            print("👉 Click en click4 después de esperar")
                        else:
                            print("⚠️ click4 no apareció")

                        wait_human(1.5, 2.5)
                    else:
                        wait_human(1.5, 2.5)

                    encontrado = True
                    break

            wait(random.uniform(0.4, 0.6))

    # 🔁 REINTENTO
    if not encontrado:
        print("🔁 Reintentando escaneo antes de abrir URL...")

        reintento_encontrado = False
        start_retry = time.time()
        timeout_retry = 6

        while time.time() - start_retry < timeout_retry and not reintento_encontrado:

            for temp in templates:
                pattern_buscar = Pattern(temp["buscar"]).similar(similarity)
                match_buscar = exists(pattern_buscar, 0.5)

                if match_buscar:
                    pattern_click = Pattern(temp["click"]).similar(similarity)

                    start_time_scroll = time.time()
                    timeout_scroll = 5

                    while True:
                        match_click = exists(pattern_click, 0)
                        if match_click:
                            break

                        scroll_human()

                        if time.time() - start_time_scroll > timeout_scroll:
                            break

                    match_click = exists(pattern_click, 1)

                    if match_click:
                        move_mouse_human(match_click)
                        micro_pause()

                        # 🔥 Reintento img0
                        if temp["name"] == "img0":
                            click(match_click)
                            print("✅ Reintento exitoso con img0")

                            wait_human(2.5, 4)

                            pattern_20 = Pattern("20.png").similar(similarity)
                            match_20 = exists(pattern_20, 2)

                            if match_20:
                                move_mouse_human(match_20)
                                micro_pause()
                                click(match_20)
                                print("👉 Click en 20.png después del reintento")
                            else:
                                print("⚠️ 20.png no apareció en reintento")

                            reintento_encontrado = True
                            encontrado = True
                            break

                        click(match_click)
                        print("✅ Reintento exitoso con {}".format(temp["name"]))

                        reintento_encontrado = True
                        encontrado = True
                        break

                wait(random.uniform(0.3, 0.5))

    # 🌐 FALLBACK URL
    if not encontrado:
        print("🌐 No se encontró ninguna imagen, abriendo nueva pestaña")

        type("t", Key.CTRL)
        wait_human(0.8, 1.2)

        paste("https://link-target.net/3995761/bgPZqtt3wH5e")
        wait_human(0.8, 1.2)

        type(Key.ENTER)
        wait_human(2.5, 3.5)

    wait_human(0.8, 1.5)

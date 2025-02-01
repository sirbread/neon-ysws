import displayio
import board
import framebufferio
import rgbmatrix
import time

displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=64,
    height=32,
    bit_depth=2,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13,
    latch_pin=board.D0,
    output_enable_pin=board.D1,
)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

logo_width = 11
logo_height = 8

logo_bitmap = displayio.Bitmap(logo_width, logo_height, 2)

color_palette = [
    0xbe00ff,
    0x00feff,
    0xff8300,
    0x0026ff,
    0xfffa01,
    0xff2600,
    0xff008b,
    0x25ff01,
]

logo_palette = displayio.Palette(2)
logo_palette[0] = 0x000000
logo_palette[1] = color_palette[0]

logo_pixels = [
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0]
]

for y in range(logo_height):
    for x in range(logo_width):
        logo_bitmap[x, y] = logo_pixels[y][x]

logo_tile = displayio.TileGrid(logo_bitmap, pixel_shader=logo_palette)

main_group = displayio.Group()

x_pos = 0
y_pos = 0
x_velocity = 1
y_velocity = 1

main_group.append(logo_tile)
display.root_group = main_group

display_width = display.width
display_height = display.height

color_index = 0

edge_hit = False

while True:
    x_pos += x_velocity
    y_pos += y_velocity

    if x_pos <= 0 or x_pos + logo_width > display_width or y_pos <= 0 or y_pos + logo_height > display_height:
        edge_hit = True
    else:
        edge_hit = False

    if edge_hit:
        color_index = (color_index + 1) % len(color_palette)
        logo_palette[1] = color_palette[color_index]

        if x_pos <= 0 or x_pos + logo_width > display_width:
            x_velocity = -x_velocity

        if y_pos <= 0 or y_pos + logo_height > display_height:
            y_velocity = -y_velocity

    logo_tile.x = x_pos
    logo_tile.y = y_pos

    display.refresh()

    time.sleep(0.08)

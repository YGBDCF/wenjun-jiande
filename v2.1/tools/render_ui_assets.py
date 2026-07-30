from pathlib import Path
from random import Random
from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parents[1] / "game/images/chapter01/ui"
OUT.mkdir(parents=True, exist_ok=True)
rng = Random(1937)


def paper(size, alpha=248):
    w, h = size
    im = Image.new("RGBA", size, (216, 201, 166, alpha))
    px = im.load()
    for y in range(h):
        edge = min(x := y, h - 1 - y)
        for x in range(w):
            e = min(x, w - 1 - x, edge)
            shade = -int(max(0, 18 - e) * 0.55) + rng.randint(-5, 5)
            px[x, y] = (max(0, 216 + shade), max(0, 201 + shade), max(0, 166 + shade), alpha)
    return im.filter(ImageFilter.GaussianBlur(0.22))


def ink(size, alpha=238):
    w, h = size
    im = Image.new("RGBA", size, (8, 13, 13, alpha))
    px = im.load()
    for y in range(h):
        for x in range(w):
            n = rng.randint(-7, 8)
            px[x, y] = (max(0, 12+n), max(0, 17+n), max(0, 16+n), alpha)
    return im.filter(ImageFilter.GaussianBlur(0.3))


def ornament(draw, box, color, light=False):
    x0, y0, x1, y1 = box
    c = color
    draw.rectangle(box, outline=c, width=2)
    draw.rectangle((x0+10, y0+10, x1-10, y1-10), outline=(*c[:3], 120), width=1)
    d = 26
    for sx, sy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        ix = 1 if sx == x0 else -1
        iy = 1 if sy == y0 else -1
        points = [(sx+ix*4, sy+iy*20), (sx+ix*4, sy+iy*4), (sx+ix*20, sy+iy*4),
                  (sx+ix*d, sy+iy*11), (sx+ix*11, sy+iy*d)]
        draw.line(points, fill=c, width=2, joint="curve")
        draw.ellipse((sx+ix*16-3, sy+iy*16-3, sx+ix*16+3, sy+iy*16+3), fill=c)


def save_dialogue():
    im = paper((1130, 300), 246)
    d = ImageDraw.Draw(im, "RGBA")
    ornament(d, (5, 5, 1124, 294), (116, 83, 38, 225))
    d.line((52, 62, 1078, 62), fill=(127, 93, 48, 85), width=1)
    d.ellipse((870, 90, 1050, 270), outline=(111, 79, 38, 25), width=3)
    d.ellipse((902, 122, 1018, 238), outline=(111, 79, 38, 22), width=2)
    im.save(OUT / "dialogue_panel.png")


def save_dark(name, size, alpha=238, divider=None):
    im = ink(size, alpha)
    d = ImageDraw.Draw(im, "RGBA")
    ornament(d, (4, 4, size[0]-5, size[1]-5), (151, 116, 56, 220))
    if divider:
        d.line((24, divider, size[0]-24, divider), fill=(157, 121, 62, 100), width=1)
    im.save(OUT / name)


def save_button(name, size, active=False):
    im = ink(size, 225)
    d = ImageDraw.Draw(im, "RGBA")
    if active:
        d.rectangle((1, 1, size[0]-2, size[1]-2), fill=(91, 67, 35, 205), outline=(195, 151, 75, 230), width=2)
    else:
        d.line((7, size[1]-3, size[0]-7, size[1]-3), fill=(134, 102, 51, 170), width=1)
    im.save(OUT / name)


save_dialogue()
save_dark("task_panel.png", (356, 560), divider=104)
save_dark("inventory_panel.png", (356, 310), divider=58)
save_button("top_button.png", (78, 52))
save_button("tab_idle.png", (104, 44))
save_button("tab_active.png", (104, 44), True)


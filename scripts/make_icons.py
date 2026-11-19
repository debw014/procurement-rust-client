"""生成 Tauri 应用图标：蓝色渐变圆角底 + 白色清单剪贴板图形。"""
from PIL import Image, ImageDraw
import os

SIZE = 1024
img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))

# 渐变底
grad = Image.new("RGBA", (SIZE, SIZE))
gd = grad.load()
c1 = (37, 99, 235)    # #2563eb
c2 = (15, 23, 42)     # #0f172a
for y in range(SIZE):
    for x in range(SIZE):
        t = (x * 0.35 + y * 0.65) / (SIZE - 1)
        gd[x, y] = (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t),
            255,
        )

# 圆角遮罩
mask = Image.new("L", (SIZE, SIZE), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=int(SIZE * 0.22), fill=255)
img.paste(grad, (0, 0), mask)

d = ImageDraw.Draw(img)

# 剪贴板板身
pad = int(SIZE * 0.20)
board = [pad, int(SIZE * 0.24), SIZE - pad, SIZE - int(SIZE * 0.16)]
d.rounded_rectangle(board, radius=int(SIZE * 0.05), fill=(255, 255, 255, 255))

# 顶部夹子
cw, ch = int(SIZE * 0.26), int(SIZE * 0.10)
cx = SIZE // 2
cy = int(SIZE * 0.235)
d.rounded_rectangle(
    [cx - cw // 2, cy - ch // 2, cx + cw // 2, cy + ch // 2],
    radius=ch // 2,
    fill=(37, 99, 235, 255),
)

# 内容线条（蓝色）
line_color = (37, 99, 235, 255)
lx0 = pad + int(SIZE * 0.08)
lx1 = SIZE - pad - int(SIZE * 0.08)
ly = int(SIZE * 0.40)
lh = int(SIZE * 0.045)
gap = int(SIZE * 0.115)
for i in range(4):
    width = lx1 if i % 2 == 0 else lx1 - int(SIZE * 0.14)
    d.rounded_rectangle([lx0, ly, width, ly + lh], radius=lh // 2, fill=line_color)
    ly += gap

os.makedirs("src-tauri/icons", exist_ok=True)
img.save("src-tauri/icons/icon.png")
for name, size in [("32x32.png", 32), ("128x128.png", 128), ("128x128@2x.png", 256), ("icon-512.png", 512)]:
    img.resize((size, size), Image.LANCZOS).save(f"src-tauri/icons/{name}")
img.save("src-tauri/icons/icon.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print("icons generated")

#!/usr/bin/env python3
"""Boss-facing poster v2, drawn with PIL so Chinese text is exact (no AI text garbling).
Redesign vs v1: left-aligned, print-flyer feel, serif headline, numbered service rows,
pilot badge instead of a big flat colour block. Prices are the real service prices
(499/899); contact line is left blank on purpose — fill it before sending."""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SERIF = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"

def font(path, size):
    for idx in (2, 0):
        try:
            return ImageFont.truetype(path, size, index=idx)
        except Exception:
            continue
    return ImageFont.load_default()

img = Image.new("RGB", (W, H), "#FBF3E4")
d = ImageDraw.Draw(img)
# faint paper grain
px = img.load()
rnd = random.Random(7)
for _ in range(9000):
    x, y = rnd.randrange(W), rnd.randrange(H)
    r, g, b = px[x, y]
    v = rnd.randint(-8, 8)
    px[x, y] = (max(0, min(255, r + v)), max(0, min(255, g + v)), max(0, min(255, b + v)))
d = ImageDraw.Draw(img)

M = 84  # left margin
# top rule + eyebrow
d.rectangle([M, 64, M + 72, 72], fill="#D9551F")
d.text((M, 88), "龙潭寺周边 · 只做小餐饮", font=font(BOLD, 34), fill="#D9551F")
d.text((M, 140), "先免费做一条，有效果再谈钱", font=font(REG, 32), fill="#7A6A58")

# headline, serif, left-aligned
y = 208
for line in ["你只管做好菜，", "流量和团购我来弄。"]:
    d.text((M, y), line, font=font(SERIF, 76), fill="#2B2118")
    y += 100
d.text((M, y + 4), "我是住在附近的小蔡，能上门，不是网上接单跑路的。",
       font=font(REG, 32), fill="#7A6A58")

# numbered service rows
rows = [
    ("01", "短视频", "把菜拍成视频，挂上店位置和团购"),
    ("02", "团购", "套餐设计、上架、每周维护一次"),
    ("03", "直播", "老板出镜 15 分钟，剩下 AI 兜底，全程挂 AI 标识"),
]
y = 508
for num, title, desc in rows:
    d.text((M, y), num, font=font(BOLD, 34), fill="#D9551F")
    d.text((M + 78, y - 2), title, font=font(BOLD, 40), fill="#2B2118")
    d.text((M + 78, y + 50), desc, font=font(REG, 32), fill="#5A4A38")
    y += 120
    d.line([(M, y - 16), (W - M, y - 16)], fill="#E8DCC8", width=2)

# pilot badge
d.rounded_rectangle([M, y + 4, W - M, y + 88], radius=42, outline="#D9551F", width=3)
d.text((M + 36, y + 26), "试点免费：1 条菜品视频 + 1 场直播 · 不达标不收费",
       font=font(BOLD, 30), fill="#D9551F")

# price cards
box_y = y + 116
for x0, title, detail, price, hot in [
    (M, "基础版", "8 条视频 + 1 场直播", "499 元 / 月", False),
    (560, "标准版 · 主推", "12 条视频 + 2 场直播 + 周复盘", "899 元 / 月", True),
]:
    fill = "#FFF1E6" if hot else "#FFFFFF"
    d.rounded_rectangle([x0, box_y, x0 + 428, box_y + 158], radius=20,
                        fill=fill, outline="#D9551F" if hot else "#E8DCC8",
                        width=4 if hot else 2)
    d.text((x0 + 28, box_y + 18), title, font=font(BOLD, 36),
           fill="#D9551F" if hot else "#2B2118")
    d.text((x0 + 28, box_y + 66), detail, font=font(REG, 28), fill="#5A4A38")
    d.text((x0 + 28, box_y + 102), price, font=font(BOLD, 40), fill="#2B2118")

fy = box_y + 190
d.line([(M, fy), (W - M, fy)], fill="#E8DCC8", width=2)
d.text((M, fy + 22), "小蔡 · 本地商家 AI 提效助手", font=font(BOLD, 36), fill="#2B2118")
d.text((M, fy + 72), "按月付，随时停 · 开户费 299 元（试点店免）",
       font=font(REG, 30), fill="#7A6A58")
d.text((M, fy + 116), "微信 / 电话：______________（发之前先填上）",
       font=font(REG, 30), fill="#7A6A58")

out = "/home/hatch/workspace/goals/ai/files/本地生活AI代运营/宣传图.png"
img.save(out)
print(out)

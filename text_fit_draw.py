# filename: text_fit_draw.py
from io import BytesIO
from typing import Tuple, Union, Literal
from PIL import Image, ImageDraw, ImageFont
import os

Align = Literal["left", "center", "right"]
VAlign = Literal["top", "middle", "bottom"]

def draw_text_auto(
    image_source: Union[str, Image.Image],
    top_left: Tuple[int, int],
    bottom_right: Tuple[int, int],
    text: str,
    color: Tuple[int, int, int] = (0, 0, 0),
    max_font_height: int | None = None,
    font_path: str | None = None,
    align: Align = "center",      # 新增：水平对齐（逐行生效）
    valign: VAlign = "middle",       # 新增：垂直对齐
    line_spacing: float = 0.15,   # 新增：额外行距比例
) -> bytes:
    """
    在指定矩形内自适应字号绘制文本；逐行居中/对齐可控，返回 PNG 字节。
    """

    # --- 1. 打开图像 ---
    if isinstance(image_source, Image.Image):
        img = image_source.copy()
    else:
        img = Image.open(image_source).convert("RGBA")
    draw = ImageDraw.Draw(img)

    x1, y1 = top_left
    x2, y2 = bottom_right
    if not (x2 > x1 and y2 > y1):
        raise ValueError("无效的文字区域。")
    region_w, region_h = x2 - x1, y2 - y1

    # --- 2. 字体加载 ---
    def _load_font(size: int) -> ImageFont.FreeTypeFont:
        if font_path and os.path.exists(font_path):
            return ImageFont.truetype(font_path, size=size)
        try:
            return ImageFont.truetype("DejaVuSans.ttf", size=size)
        except Exception:
            return ImageFont.load_default()

    # --- 3. 文本包行（给定字号、最大宽）---
    def wrap_lines(txt: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
        lines: list[str] = []
        for para in txt.splitlines() or [""]:
            # 有空格则按词，否则按字符（适配中文）
            has_space = (" " in para)
            units = para.split(" ") if has_space else list(para)
            buf = ""
            def unit_join(a: str, b: str) -> str:
                if not a: return b
                return (a + " " + b) if has_space else (a + b)

            for u in units:
                trial = unit_join(buf, u)
                w = draw.textlength(trial, font=font)  # 更稳的宽度估计
                if w <= max_w:
                    buf = trial
                else:
                    if buf:
                        lines.append(buf)  # 已满，先收一行
                    if has_space and len(u) > 1:
                        # 过长单词按字符强拆（你的原逻辑保留）
                        tmp = ""
                        for ch in u:
                            if draw.textlength(tmp + ch, font=font) <= max_w:
                                tmp += ch
                            else:
                                if tmp:
                                    lines.append(tmp)
                                tmp = ch
                        buf = tmp
                    else:
                        # ✅ 不要把 u 直接 append 成一整行；把它作为新行的开始
                        if draw.textlength(u, font=font) <= max_w:
                            buf = u
                        else:
                            # 只有在字符本身都比行宽还宽时，才单独成行
                            lines.append(u)
                            buf = ""
            if buf != "":
                lines.append(buf)
            if para == "" and (not lines or lines[-1] != ""):
                lines.append("")  # 保留显式空行
        return lines

    # --- 4. 测量一组行的整体尺寸 ---
    def measure_block(lines: list[str], font: ImageFont.FreeTypeFont) -> tuple[int, int, int]:
        ascent, descent = font.getmetrics()
        line_h = int((ascent + descent) * (1 + line_spacing))
        max_w = 0
        for ln in lines:
            max_w = max(max_w, int(draw.textlength(ln, font=font)))
        total_h = max(line_h * max(1, len(lines)), 1)
        return max_w, total_h, line_h

    # --- 5. 搜索最大字号 ---
    hi = min(region_h, max_font_height) if max_font_height else region_h
    lo, best_size, best_lines, best_line_h, best_block_h = 1, 0, [], 0, 0

    while lo <= hi:
        mid = (lo + hi) // 2
        font = _load_font(mid)
        lines = wrap_lines(text, font, region_w)
        w, h, lh = measure_block(lines, font)
        if w <= region_w and h <= region_h:
            best_size, best_lines, best_line_h, best_block_h = mid, lines, lh, h
            lo = mid + 1
        else:
            hi = mid - 1

    if best_size == 0:
        # 极端情况下退化：1 像素字体
        font = _load_font(1)
        best_lines = wrap_lines(text, font, region_w)
        _, best_block_h, best_line_h = 0, 1, 1
        best_size = 1
    else:
        font = _load_font(best_size)

    # --- 6. 计算块的起始 y（垂直对齐） ---
    if valign == "top":
        y_start = y1
    elif valign == "middle":
        y_start = y1 + (region_h - best_block_h) // 2
    else:  # bottom
        y_start = y2 - best_block_h

    # --- 7. 逐行绘制（关键：每行单独水平对齐） ---
    y = y_start
    for ln in best_lines:
        line_w = int(draw.textlength(ln, font=font))
        if align == "left":
            x = x1
        elif align == "center":
            x = x1 + (region_w - line_w) // 2
        else:  # right
            x = x2 - line_w
        draw.text((x, y), ln, font=font, fill=color)
        y += best_line_h
        if y - y_start > region_h:
            break

    # --- 8. 导出 PNG 字节 ---
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

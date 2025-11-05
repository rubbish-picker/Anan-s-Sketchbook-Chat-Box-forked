# hotkey_demo.py
import keyboard
import time
import pyperclip
from text_fit_draw import draw_text_auto
import io
from PIL import Image
import win32clipboard

DELAY= 0.1

def copy_png_bytes_to_clipboard(png_bytes: bytes):
    # 打开 PNG 字节为 Image
    image = Image.open(io.BytesIO(png_bytes))
    # 转换成 BMP 字节流（去掉 BMP 文件头的前 14 个字节）
    with io.BytesIO() as output:
        image.convert("RGB").save(output, "BMP")
        bmp_data = output.getvalue()[14:]

    # 打开剪贴板并写入 DIB 格式
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, bmp_data)
    win32clipboard.CloseClipboard()


def cut_all_and_get_text() -> str:
    """
    模拟 Ctrl+A / Ctrl+X 剪切全部文本，并返回剪切得到的内容。
    delay: 每步之间的延时（秒），默认0.1秒。
    """
    # 备份原剪贴板
    old_clip = pyperclip.paste()

    # 清空剪贴板，防止读到旧数据
    pyperclip.copy("")

    # 发送 Ctrl+A 和 Ctrl+X
    keyboard.send('ctrl+a')
    keyboard.send('ctrl+x')
    time.sleep(DELAY)

    # 获取剪切后的内容
    new_clip = pyperclip.paste()

    return new_clip

def Start():
    print("Start generate...")

    text=cut_all_and_get_text()
    if text == "":
        print("no text")
        return
    print("Get text: "+text)

    png_bytes = draw_text_auto(
    image_source="base.png",
    top_left=(119, 450),
    bottom_right=(119+279, 450+175),
    text=text,
    color=(0, 0, 0),
    max_font_height=64,        # 例如限制最大字号高度为 64 像素
    font_path="font.ttf"
)
    copy_png_bytes_to_clipboard(png_bytes)
    
    keyboard.send('ctrl+v')

    time.sleep(DELAY)
    keyboard.send('enter')


    

# 绑定 Ctrl+Alt+H 作为全局热键
ok=keyboard.add_hotkey('enter', Start, suppress=True)

print("Starting...")
print("Hot key bind: "+str(bool(ok)))

# 保持程序运行
keyboard.wait()

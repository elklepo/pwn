import pytesseract
import PIL
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

url = 'https://hidden-island-93990.squarectf.com/ea6c95c6d0ff24545cad'
img_path = "image.png"
browser = webdriver.Chrome()
browser.fullscreen_window()
browser.get(url)
browser.execute_script("document.body.style.zoom='500%'")
browser.save_screenshot(img_path)
pytesseract.pytesseract.tesseract_cmd = 'tesseract.exe'  # must be in path

img = PIL.Image.open(img_path)
w, h = img.size
img.crop((0, 300, w-20, h-150)).save(img_path)
tesseract_config = r"--oem 0 -c tessedit_char_whitelist=0123456789()x+- -psm 6"
content = pytesseract.image_to_string(PIL.Image.open(img_path), config=tesseract_config)
content = content.replace("x", "*")
print(content)
try:
    res = eval(content)
    print("evaluated = " + str(res))
    inputElement = browser.find_element_by_name("answer")
    inputElement.send_keys(res)
    inputElement.send_keys(Keys.ENTER)
except Exception as ex:
    print(ex)
    browser.quit()



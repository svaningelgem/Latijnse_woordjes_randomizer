from pathlib import Path

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"E:\Latijnse_woordjes_randomizer\exe\tesseract.exe"
)


def get_languages():
    return pytesseract.get_languages(config="")


def image2str(img: str | Path, language: str | None = None) -> str:
    return pytesseract.image_to_string(image=Image.open(img), lang=language)


def image2data(img: str | Path, language: str | None = None) -> str:
    return pytesseract.image_to_data(image=Image.open(img), lang=language)

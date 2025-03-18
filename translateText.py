from manga_ocr import MangaOcr

def frame_ocr(image):
    mocr = MangaOcr()
    text = mocr(image)
    print(text)
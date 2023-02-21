import glob
import img2pdf


class PdfMaker:
    def __init__(self, path):
        self.path = path

    def create_pdf(self):
        file_names = glob.glob(f"{self.path}/*.png")
        sorted_file_names = sorted(file_names)
        with open("name.pdf", "wb") as f:
            f.write(img2pdf.convert(sorted_file_names))

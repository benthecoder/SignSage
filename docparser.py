from pathlib import Path
from typing import Dict


class PDFParser:
    """PDF parser."""

    def __init__(self):
        self.parser = self._init_parser()

    def _init_parser(self) -> Dict:
        """Init parser."""
        return {}

    def parse_file(self, file: Path, errors: str = "ignore") -> str:
        """Parse file."""
        try:
            import PyPDF2
        except ImportError:
            raise ImportError("PyPDF2 is required to read PDF files.")

        text_list = []
        with open(file, "rb") as fp:
            # Create a PDF object
            pdf = PyPDF2.PdfReader(fp)

            # Get the number of pages in the PDF document
            num_pages = len(pdf.pages)

            # Iterate over every page
            for page in range(num_pages):
                # Extract the text from the page
                page_text = pdf.pages[page].extract_text()
                text_list.append(page_text)

        text = "\n".join(text_list)

        return text


def get_text(path):
    """Get text from PDF file."""
    parser = PDFParser()
    pdf_path = Path(path)
    text_content = parser.parse_file(pdf_path)
    return text_content

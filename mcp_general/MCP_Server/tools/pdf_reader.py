import pymupdf

from ._paths import get_path


def read_pdf(file_path: str, start_page: int = 1, max_pages: int = 10) -> str:
    """Extract PDF text within the workspace; page numbers start at 1. No OCR."""
    if start_page < 1 or max_pages < 1:
        raise ValueError("start_page and max_pages must be positive.")
    with pymupdf.open(get_path(file_path)) as document:
        if not document.is_pdf:
            raise ValueError("File must be a PDF.")
        if document.needs_pass:
            raise ValueError("Password-protected PDFs are not supported.")
        if start_page > len(document):
            raise ValueError("start_page exceeds PDF length.")
        end_page = min(start_page - 1 + max_pages, len(document))
        return "\n\n".join(
            f"Page {number + 1}\n{document[number].get_text()}"
            for number in range(start_page - 1, end_page)
        )

# ============================================================
# EIRA — File Processing Tool
# ============================================================

import os

def extract_text_from_pdf(path: str) -> str:
    from pypdf import PdfReader
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    return text.strip()

def extract_text_from_docx(path: str) -> str:
    import docx
    doc = docx.Document(path)
    return "\n".join(p.text for p in doc.paragraphs).strip()

def extract_text_from_plain(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()

def describe_image(path: str, model: str = "llava:7b") -> str:
    return "Image description not available — vision model not configured."

TEXT_EXTENSIONS = {
    "txt", "md", "py", "java", "js", "ts", "jsx", "tsx",
    "cpp", "c", "h", "html", "css", "json", "csv", "yaml", "yml"
}
IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}

def process_uploaded_file(path: str, filename: str) -> dict:
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    try:
        if ext == "pdf":
            return {"type": "text", "content": extract_text_from_pdf(path)}
        elif ext == "docx":
            return {"type": "text", "content": extract_text_from_docx(path)}
        elif ext in TEXT_EXTENSIONS:
            return {"type": "text", "content": extract_text_from_plain(path)}
        elif ext in IMAGE_EXTENSIONS:
            return {"type": "image", "content": describe_image(path)}
        else:
            return {"type": "unsupported", "content": ""}
    except Exception as e:
        return {"type": "error", "content": str(e)}
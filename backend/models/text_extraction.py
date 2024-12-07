import pdfplumber
import chardet

def extract_text_from_file(file_path, file_type):
    """
    Extract text from a file, either PDF or plain text.
    """
    try:
        print(f"Extracting text from file: {file_path}, file type: {file_type}")
        if file_type == "pdf":
            with pdfplumber.open(file_path) as pdf:
                text = "".join(page.extract_text() or "" for page in pdf.pages)
                print(f"Extracted {len(text)} characters from PDF.")
        else:
            with open(file_path, "rb") as file:
                detected_encoding = chardet.detect(file.read()).get("encoding", "utf-8")
                print(f"Detected file encoding: {detected_encoding}")
                file.seek(0)
                text = file.read().decode(detected_encoding, errors="replace")
                print(f"Extracted {len(text)} characters from text file.")

        if not text.strip():
            raise ValueError("The file is empty or unreadable.")
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        raise ValueError(f"Failed to extract text: {e}")

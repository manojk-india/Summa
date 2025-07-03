import fitz  # PyMuPDF
import os

def extract_pdf_structured(pdf_path, image_output_folder="pdf_images"):
    os.makedirs(image_output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    structured_output = []

    for page_num, page in enumerate(doc, start=1):
        structured_output.append(f"\n--- Page {page_num} ---\n")
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if block["type"] == 0:  # Text
                for line in block["lines"]:
                    spans = line["spans"]
                    line_text = " ".join(span["text"].strip() for span in spans if span["text"].strip())

                    if not line_text:
                        continue

                    avg_font_size = sum(span["size"] for span in spans) / len(spans)

                    if avg_font_size > 15:  # heuristic for headings
                        structured_output.append(f"\n# {line_text}")
                    elif avg_font_size > 12:  # subheadings
                        structured_output.append(f"\n## {line_text}")
                    else:
                        structured_output.append(line_text)

            elif block["type"] == 1:  # Image
                try:
                    img_index = block["number"]
                    pix = page.get_image_pixmap(img_index, matrix=fitz.Matrix(2, 2))
                    image_filename = os.path.join(image_output_folder, f"page{page_num}_img{img_index}.png")
                    pix.save(image_filename)
                    structured_output.append(f"\n![Image](./{image_output_folder}/page{page_num}_img{img_index}.png)")
                except Exception as e:
                    structured_output.append(f"\n[Image extraction failed on page {page_num}]")

    return "\n".join(structured_output)

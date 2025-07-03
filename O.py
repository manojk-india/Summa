import os
import queue
from spire.doc import *
from spire.doc.common import *

def extract_images(doc, image_dir):
    os.makedirs(image_dir, exist_ok=True)
    nodes = queue.Queue()
    nodes.put(doc)
    images = []
    while nodes.qsize() > 0:
        node = nodes.get()
        for i in range(node.ChildObjects.Count):
            child = node.ChildObjects.get_Item(i)
            # Check if child is an image
            if child.DocumentObjectType == DocumentObjectType.Picture:
                picture = child if isinstance(child, DocPicture) else None
                if picture:
                    dataBytes = picture.ImageBytes
                    img_filename = f"image_{len(images)+1}.png"
                    img_path = os.path.join(image_dir, img_filename)
                    with open(img_path, 'wb') as img_file:
                        img_file.write(dataBytes)
                    images.append(img_filename)
            elif isinstance(child, ICompositeObject):
                nodes.put(child)
    return images

def extract_text_and_tables(doc):
    content_lines = []
    for section in doc.Sections:
        # Section Heading
        content_lines.append(f"# Section")
        # Paragraphs
        for para in section.Paragraphs:
            text = para.Text.strip()
            if text:
                content_lines.append(f"\n{para.StyleName if para.StyleName else 'Paragraph'}: {text}")
        # Tables
        for table_idx, table in enumerate(section.Tables):
            content_lines.append(f"\n## Table {table_idx+1}")
            for row in table.Rows:
                row_cells = []
                for cell in row.Cells:
                    cell_text = " | ".join([p.Text.strip() for p in cell.Paragraphs if p.Text.strip()])
                    row_cells.append(cell_text)
                content_lines.append(" | ".join(row_cells))
    return "\n".join(content_lines)

def main(doc_path, image_dir, text_output_path):
    doc = Document()
    doc.LoadFromFile(doc_path)
    # Extract images
    images = extract_images(doc, image_dir)
    print(f"Extracted {len(images)} images to {image_dir}")
    # Extract text and tables
    structured_text = extract_text_and_tables(doc)
    with open(text_output_path, "w", encoding="utf-8") as f:
        f.write(structured_text)
    print(f"Structured text saved to {text_output_path}")
    doc.Close()

# Usage
doc_path = "your_file.doc"  # Path to your .doc file
image_dir = "extracted_images"
text_output_path = "structured_content.txt"
main(doc_path, image_dir, text_output_path)

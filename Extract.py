from bs4 import BeautifulSoup

def format_table_plain(headers, rows):
    all_rows = [headers] + rows
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*all_rows)]
    def fmt_row(row):
        return "| " + " | ".join(str(cell).ljust(width) for cell, width in zip(row, col_widths)) + " |"
    lines = []
    lines.append("+" + "+".join("-" * (w + 2) for w in col_widths) + "+")
    lines.append(fmt_row(headers))
    lines.append("+" + "+".join("-" * (w + 2) for w in col_widths) + "+")
    for row in rows:
        row += [""] * (len(headers) - len(row))
        lines.append(fmt_row(row))
    lines.append("+" + "+".join("-" * (w + 2) for w in col_widths) + "+")
    return "\n".join(lines)

def conf_html_to_text(html_content: str) -> str:
    """
    Converts Confluence REST API HTML content to a readable plain text string,
    preserving tables in a visually aligned format.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    output = []
    # Walk through all top-level elements in order
    for elem in (soup.body or soup).children:
        if getattr(elem, "name", None) == "table":
            rows = elem.find_all("tr")
            if not rows:
                continue
            headers = [th.get_text(strip=True) for th in rows[0].find_all(["th", "td"])]
            data_rows = []
            for tr in rows[1:]:
                data_rows.append([td.get_text(strip=True) for td in tr.find_all(["td", "th"])])
            output.append(format_table_plain(headers, data_rows))
        elif getattr(elem, "name", None) in ["p", "h1", "h2", "h3", "h4", "h5", "h6"]:
            text = elem.get_text(strip=True)
            if text:
                output.append(text)
        elif getattr(elem, "name", None) == "ul":
            for li in elem.find_all("li"):
                text = li.get_text(strip=True)
                if text:
                    output.append(f"- {text}")
        elif getattr(elem, "name", None) == "ol":
            for i, li in enumerate(elem.find_all("li"), 1):
                text = li.get_text(strip=True)
                if text:
                    output.append(f"{i}. {text}")
        # Add more tag handlers as needed
    return "\n\n".join(output)
    

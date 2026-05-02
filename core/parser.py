#core/parser
def parser(raw_text: str):
    if not raw_text:
        return None
    text = raw_text.strip()
    if not text.startswith("/"):
        return {
            "command": None,
            "args": [],
            "raw": text
        }
    part = text.split()
    return {
        "command": part[0],
        "args": part[1:],
        "raw":  text
    }
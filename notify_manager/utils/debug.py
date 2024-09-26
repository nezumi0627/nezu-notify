from requests import Response


def save_html(r: Response, path: str = "index.html") -> None:
    with open(path, "wt") as f:
        f.write(r.text)

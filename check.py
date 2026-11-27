#!/usr/bin/env python3
"""Check generated navigation, fragments, and assets at both Pages URL layouts."""

from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

from build import SITE, pages


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.references = []
        self.ids = set()
        self.headings = 0
        self.feed(path.read_text(encoding="utf-8"))
        self.close()

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        if tag in {"a", "link"} and "href" in attributes:
            self.references.append(attributes["href"])
        if "id" in attributes:
            self.ids.add(attributes["id"])
        if tag == "h1":
            self.headings += 1


def verify(prefix, documents):
    for path, document in documents.items():
        relative = path.relative_to(SITE).as_posix().removesuffix("index.html")
        assert document.headings == 1, path
        for reference in document.references:
            if urlsplit(reference).netloc:
                continue
            target = urlsplit(urljoin(f"https://example.test{prefix}{relative}", reference))
            assert target.path.startswith(prefix), (path, reference)
            target_path = target.path.removeprefix(prefix)
            if target.path.endswith("/"):
                target_path += "index.html"
            destination = SITE / target_path
            assert destination.is_file(), (path, reference)
            if target.fragment:
                assert target.fragment in documents[destination].ids, (path, reference)


def main():
    documents = {path: Document(path) for path in SITE.rglob("*.html")}
    assert documents.keys() == {SITE / slug / "index.html" for slug in pages()}
    for prefix in ("/", "/heritageware.dev/"):
        verify(prefix, documents)
    print(f"Checked {len(documents)} pages at the domain root and the Pages project path.")


if __name__ == "__main__":
    main()

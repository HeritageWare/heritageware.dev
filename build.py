#!/usr/bin/env python3
"""Build the HeritageWare static site with the Python standard library."""

import json
import shutil
from collections import Counter
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "_site"
ORG = "https://github.com/heritageware"
FOUNDATION = f"{ORG}/foundation"
STATUSES = ("pass", "fail", "skip", "untested")


def compatibility():
    report = json.loads((ROOT / "compatibility-results.json").read_text(encoding="utf-8"))
    source = report["source"]
    if source and not source.startswith(f"{ORG}/compatibility-suite/actions/runs/"):
        raise ValueError("The source must be a run in the public compatibility suite.")
    rows = []
    for profile in report["profiles"]:
        counts = Counter(profile["cases"])
        if counts.keys() - set(STATUSES):
            raise ValueError(f"Invalid case status for {profile['name']}.")
        if counts and not source:
            raise ValueError("Published compatibility cases require a CI results URL.")
        cells = [str(counts[status]) for status in STATUSES] if counts else ["—"] * len(STATUSES)
        cells.append(str(len(profile["cases"])) if counts else "—")
        row = "".join(f"<td>{cell}</td>" for cell in cells)
        rows.append(
            f'<tr><th scope="row">{escape(profile["name"])}</th>'
            f'<td>{escape(profile["target"])}</td>{row}</tr>'
        )
    evidence = (
        f'<p><a href="{escape(source, quote=True)}">View the source CI run</a>.</p>'
        if source
        else "<p>There are no published conformance runs. An em dash marks a profile without case results.</p>"
    )
    return evidence + """
<div class="table-wrap" tabindex="0" role="region" aria-label="Compatibility results">
<table>
  <caption>Conformance cases by reference profile</caption>
  <thead><tr><th scope="col">Product</th><th scope="col">Reference target</th>
  <th scope="col">Pass</th><th scope="col">Fail</th><th scope="col">Skip</th>
  <th scope="col">Untested</th><th scope="col">Total cases</th></tr></thead>
  <tbody>
""" + "\n".join(rows) + """
  </tbody>
</table>
</div>
<p>Results apply to the listed cases. Skipped and untested cases contribute no passes.</p>
"""


def pages():
    return {
        "": ("Home", """
<p class="lead">Preserving software heritage. Rebuilding for the future.</p>
<p>HeritageWare develops faithful, independent, open-source reimplementations of classic software for modern platforms. We preserve original source-level behavior, data formats, interfaces, and workflows through reproducible testing.</p>
<p>Visual FoxPro 9.0 SP2 is our flagship reference target. <a href="projects/">Explore the projects</a> or <a href="compatibility/">see the state of compatibility evidence</a>.</p>
"""),
        "projects": ("Projects", f"""
<dl>
<dt><a href="{ORG}/heritage-foxpro">Visual FoxPro</a></dt><dd>Flagship. Visual FoxPro 9.0 SP2 language, data engine, object model, project assets, and graphical workflows.</dd>
<dt><a href="{ORG}/heritage-dbase">dBASE</a></dt><dd>Separate dBASE II and dBASE III dialect and file-format profiles.</dd>
<dt><a href="{ORG}/heritage-clipper">Clipper</a></dt><dd>Source, compiler and runtime behavior, with the first DOS release to be selected through research.</dd>
<dt><a href="{ORG}/heritage-lotus123">Lotus 1-2-3</a></dt><dd>Spreadsheet formats, calculation and historical keyboard workflows. The first DOS release is under research.</dd>
</dl>
<p>Each project is in setup or research. See the <a href="../compatibility/">compatibility evidence</a> for measured results as they become available.</p>
"""),
        "compatibility": ("Compatibility", compatibility()),
        "documentation": ("Documentation", f"""
<ul>
<li><a href="{FOUNDATION}/blob/main/COMPATIBILITY.md">Compatibility and evidence policy</a></li>
<li><a href="{FOUNDATION}/tree/main/research">Historical reference inventory</a></li>
<li><a href="{FOUNDATION}/tree/main/adr">Architecture decisions</a></li>
<li><a href="{FOUNDATION}/blob/main/CONFORMANCE.md">Conformance and CI plan</a></li>
</ul>
"""),
        "roadmap": ("Roadmap", f"""
<ol>
<li>Set up the Foundation, public repositories, and website.</li>
<li>Establish research references and a reproducible conformance system.</li>
<li>Run the first Visual FoxPro PRG and read-only DBF vertical slice.</li>
<li>Develop the data engine, object model, and forms, and advance the other profiles as capacity permits.</li>
</ol>
<p><a href="{FOUNDATION}/blob/main/ROADMAP.md">Read the full roadmap and its completion criteria</a>.</p>
"""),
        "contribute": ("Contribute", f"""
<p>Open an issue in the relevant project for a reproducible behavior or a proposed change. Use English for public contributions. Record the reference release, environment, evidence, and fixture provenance when reporting compatibility.</p>
<p><a href="{ORG}/.github/blob/main/CONTRIBUTING.md">Read the contribution guidelines</a>.</p>
"""),
        "governance": ("Governance", f"""
<p>The founder maintains the organization initially. Sustained contributors can become maintainers through the public decision process.</p>
<ul><li><a href="{FOUNDATION}/blob/main/CHARTER.md">Charter</a></li>
<li><a href="{FOUNDATION}/blob/main/GOVERNANCE.md">Governance and maintainer roles</a></li>
<li><a href="{ORG}/.github/blob/main/CODE_OF_CONDUCT.md">Code of conduct</a></li></ul>
"""),
        "legal": ("Legal", f"""
<p>HeritageWare Foundation is a community identity. HeritageWare is independent of the original software vendors. Product names identify historical reference targets.</p>
<p>Original contributions follow the terms published in their repositories. Third-party materials retain their own terms and require a provenance and rights review before redistribution.</p>
<p><a href="{FOUNDATION}/blob/main/COMPATIBILITY.md">Read the evidence and redistribution policy</a>.</p>
"""),
        "security": ("Security", f"""
<p>Use the affected repository's private vulnerability reporting option where available. Until a private channel is available, request one through the Foundation issue tracker without posting the vulnerability, sample inputs, or private information.</p>
<p><a href="{ORG}/.github/blob/main/SECURITY.md">Read the security policy</a>.</p>
"""),
    }


def render(slug, title, content, documents):
    base = "../" if slug else "./"
    nav = []
    for destination, (label, _) in documents.items():
        path = f"{base}{destination}/" if destination else base
        current = ' aria-current="page"' if destination == slug else ""
        nav.append(f'<li><a href="{path}"{current}>{escape(label)}</a></li>')
    heading = title if slug else "HeritageWare Foundation"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} | HeritageWare Foundation</title>
  <link rel="stylesheet" href="{base}style.css">
</head>
<body>
  <a class="skip" href="#content">Skip to content</a>
  <header>
    <a class="brand" href="{base}">HeritageWare Foundation</a>
    <nav aria-label="Primary"><ul>{"".join(nav)}</ul></nav>
  </header>
  <main id="content" tabindex="-1">
    <h1>{escape(heading)}</h1>
    {content}
  </main>
  <footer><a href="{ORG}">HeritageWare on GitHub</a></footer>
</body>
</html>
"""


def main():
    documents = pages()
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    for slug, (title, content) in documents.items():
        destination = SITE / slug
        destination.mkdir(exist_ok=True)
        (destination / "index.html").write_text(render(slug, title, content, documents), encoding="utf-8")
    shutil.copyfile(ROOT / "style.css", SITE / "style.css")
    (SITE / ".nojekyll").touch()


if __name__ == "__main__":
    main()

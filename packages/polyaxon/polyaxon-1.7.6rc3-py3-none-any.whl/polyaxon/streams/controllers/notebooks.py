import os

import nbformat
from nbconvert import HTMLExporter


def render_notebook(archived_path):
    with open(os.path.abspath(archived_path)) as f:
        read_data = f.read()
        notebook = nbformat.reads(read_data, as_version=4)
        html_exporter = HTMLExporter()
        html_exporter.template_file = "basic"
        (body, resources) = html_exporter.from_notebook_node(notebook)
        html_file = "<style>" + resources["inlining"]["css"][0] + "</style>" + body
        html_path = archived_path.split('.ipynb')[0] + '.html'
        with open(html_path, "w") as destination:
            destination.write(html_file)
        return html_file

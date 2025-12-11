import pathlib

import jinja2

BASE_DIR = pathlib.Path(__file__).parent.parent
FILE_PATH = BASE_DIR / "templates"


def get_render_template(template_dir: pathlib.Path):
    templates = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

    def render_template(template_name: str, **kwargs):
        template = templates.get_template(template_name)
        return template.render(**kwargs)

    return render_template


render_template = get_render_template(BASE_DIR / "templates")

from pathlib import Path


class EmailHelper:
    @staticmethod
    def fill_template(template: str, **kwargs) -> str:
        for key, value in kwargs.items():
            template = template.replace("{{ " + key + " }}", value)
        return template

    @staticmethod
    def read_email_templates(file_path: Path) -> str:
        html_file_template = Path(__file__).parent / "templates" / file_path
        return html_file_template.read_text(encoding="utf-8")

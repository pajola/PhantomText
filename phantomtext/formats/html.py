class HTMLHandler:
    def read_html(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def write_html(self, file_path, content, html_title="Document", create_html=True):
        """
        Saves the given text as an HTML file.

        Args:
            text (str): The text to save.
            file_path (str): The path to save the HTML file.
            create_html (bool): Whether the text is already a html or raw. If raw, it creates a custom structure.
        """

        if create_html:
            html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{html_title}</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Roboto', sans-serif;
            }}
        </style>
    </head>
    <body>
        <p>{content}</p>
    </body>
    </html>
            """
        else:
            html_content = content 

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)

class TXTHandler:
    def read_txt(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def write_txt(self, file_path, content):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
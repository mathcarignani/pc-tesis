class TextFileWriter:
    def __init__(self, folder, filename, mode="w"):
        self.filename = filename
        self.written_lines = 0
        self.file = open(folder + "/" + filename, mode)

    def write_line(self, line):
        self.file.write(line + '\n')
        self.written_lines += 1

    def close(self):
        self.file.close()

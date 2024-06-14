class File:
    def __init__(self, file_path):
        self.file_path = file_path

    def write_one_line(self, line):
        with open(self.file_path, 'w') as file:
            file.write(line + '\n')

    def write_multiple_lines(self, lines):
        with open(self.file_path, 'w') as file:
            for l in lines:
                file.write(l + '\n')

    def append_one_line(self, line):
        with open(self.file_path, 'a') as file:
            file.write(line + '\n')

    def append_list(self, list, item_to_line_convert_function, open_once = True):
        if open_once:
            with open(self.file_path, 'a') as file:
                for item in list:
                    line = item_to_line_convert_function(item)
                    file.write(line + '\n')
        else:
            for item in list:
                with open(self.file_path, 'a') as file:
                    line = item_to_line_convert_function(item)
                    file.write(line + '\n')
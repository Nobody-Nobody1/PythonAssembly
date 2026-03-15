class Reader:
    def read_file_lines(file_path): #reads lines from a file and returns them as a nested list
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return [line.strip().split(' ') for line in lines]

    def find_in_nested_list(nested_list): #finds positions of all values in a nested list
        if not isinstance(nested_list, list):
            raise TypeError("nested_list must be a list of lists")

        positions = []
        for row_index, row in enumerate(nested_list):
            if not isinstance(row, list):
                continue  # Skip non-list elements
            for col_index, value in enumerate(row):
                    positions.append((row_index, col_index,value))
        return positions
    
    def string_to_bool(string): #converts string to boolean
        if string.lower() in ['true', '1', 'yes']:
            return True
        elif string.lower() in ['false', '0', 'no']:
            return False
        else:
            raise ValueError(f"Cannot convert '{string}' to boolean.")
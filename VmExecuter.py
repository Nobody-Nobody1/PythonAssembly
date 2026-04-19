from src.ByteCodeReader import Reader
from src.VMPython import VMPython

bytecode = Reader.read_file_lines('ByteCode.txt')
output = Reader.find_in_nested_list(bytecode)

execution = VMPython.execute()
from src.utils import Parser, read_txt_file


input_data = read_txt_file('data/input.txt')
parser = Parser(input_data)
assigner = parser.parse_to_assigner()
assigner.assign_home_buyers()
print(assigner.format_results())
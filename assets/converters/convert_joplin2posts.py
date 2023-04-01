import argparse
from tqdm import tqdm
from pathlib import Path
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Convert Joplin markdown to posts')
parser.add_argument('--input', type=str, default="./joplin_mds", help='Path to dir')
parser.add_argument('--output', type=str, default="./output", help='Path to output dir')
parser.add_argument('--debug', default=False, action='store_true', help='Debug')

class Converter():
    def __init__(self, path_input_dir, path_output_dir, is_debug=False) -> None:
        self.path_input_dir = Path(path_input_dir)
        self.path_output_dir = Path(path_output_dir)
        self.path_output_dir.mkdir(parents=True, exist_ok=True)
        self.is_debug = is_debug

    def read_file(self, path_file):
        with open(path_file, 'r') as fp:
            contents = fp.read()
            # print(contents)
        return contents

    def write_file(self, path_file, contents):
        with open(path_file, 'w') as fp:
            fp.write(contents)
            # print(contents)
        # return contents
    
    def convert(self):
        self.paths_input = list(self.path_input_dir .rglob("*.md"))
        post_template = '---\nlayout: post\ntitle:  "{}"\ndate:   {} 00:00:00 +0530\ncategories: deep-learning\n---\n'
        for path_input in tqdm(self.paths_input):
            file_name = path_input.stem
            if "-" not in str(file_name):
                continue
            date = file_name.split("-")[0].strip()
            title_name = file_name.replace(date, "").replace("-", "").strip()
            date = "{}-{}-{}".format(date[0:4], date[4:6], date[6:8])
            post_header = post_template.format(title_name, date)
            post_contents = self.read_file(path_file=path_input)
            post_contents = post_header + post_contents
            file_name = "{}-{}.markdown".format(date, title_name)
            path_output = self.path_output_dir.joinpath(file_name)
            self.write_file(path_file=path_output, contents=post_contents)

        import pdb; pdb.set_trace()

if __name__ == "__main__":
    args = parser.parse_args()
    Converter(path_input_dir=args.input, path_output_dir=args.output, is_debug=args.debug).convert()
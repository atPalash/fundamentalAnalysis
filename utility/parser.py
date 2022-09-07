import re


def parse(input_str: str):
    try:
        args = re.findall(r'--([^ ]+)', input_str)

        parsed = {}
        for i in range(len(args)):
            start = input_str.find(args[i])
            if i+1 < len(args):
                end = input_str.find(args[i+1])
                sub_string = input_str[start + len(args[i]):end - 2].strip()
            else:
                end = len(input_str)
                sub_string = input_str[start + len(args[i]):end].strip()
            parsed[args[i]] = sub_string

        return parsed
    except Exception:
        raise


if __name__ == "__main__":
    print(parse("--name palash --sur  halder  --class software developer"))
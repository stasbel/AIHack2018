import re

def normalize_attribute(attr, keys):
    attr = str(attr)
    attr = attr.lower()
    for key in keys:
        if key in attr:
            return "NaN"
    return attr


def df_normalize_allergies(df):
    keys = ["nan", "отрицает", "не отягощен", "без дополнений"]
    df.allergies = df.allergies.map(lambda x: normalize_attribute(x, keys))
    return df


def parse_diag_code(diag_code,
                    dc_pattern=re.compile('([A-Z])?([0-9][0-9])?(\.([0-9]))?')):
    m = dc_pattern.match(diag_code)
    letter, code, subcode = m.group(1), m.group(2), m.group(4)
    code = int(code) if code is not None else None
    subcode = int(subcode) if subcode is not None else None
    return letter, code, subcode


def get_disease_class(diag_code):
    letter, code, subcode = parse_diag_code(diag_code)
    letter = str(letter)
    code = int(code)

    class_ranges = [
        ("A", 0),      #1
        ("C", 0),      #2
        ("D", 50),     #3
        ("E", 0),      #4
        ("F", 0),      #5
        ("G", 0),      #6
        ("H", 0),      #7
        ("H", 60),     #8
        ("I", 0),      #9
        ("J", 0),      #10
        ("K", 0),      #11
        ("L", 0),      #12
        ("M", 0),      #13
        ("N", 0),      #14
        ("O", 0),      #15
        ("P", 0),      #16
        ("Q", 0),      #17
        ("R", 0),      #18
        ("S", 0),      #19
        ("V", 1),      #20
        ("Z", 0),      #21
        ("Z", 100)     #fake
    ]

    special_code_ranges = [(("U", 0), ("U", 50)), (("U", 80), ("U", 90))] #22

    for special_range in special_code_ranges:
        if (letter, code) >= special_range[0] and (letter, code) < special_range[1]:
            return 22

    for i in range(len(class_ranges)):
        if (letter, code) < class_ranges[i]:
            return i

    return "NaN"


def df_normalize_state(df):
    def normalize_state_helper(state):
        state = str(state)
        state = state.lower()
        if "удовлетворит" in state:
            return "Уд."
        if "nan" in state:
            return "Уд."
        return state

    df.state = df.state.map(lambda x: normalize_state_helper(x))
    return df

def normalize_attribute(attr, keys):
    attr = str(attr)
    attr = attr.lower()
    for key in keys:
        if key in attr:
            return "NaN"
    return attr

def df_normalize_allergies(df):
    keys = ["nan", "отрицает", "не отягощен", "без дополнений"]
    new_data = df
    new_data.allergies = new_data.allergies.map(lambda x: normalize_attribute(x, keys))
    return new_data

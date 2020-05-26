class SafeDict(dict):
    def __missing__(self, key):
        return ''

def insert_tags(template, key_val):
    inserted = template.format_map(SafeDict(**key_val))
    return inserted
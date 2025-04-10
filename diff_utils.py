import difflib

def get_diff(text1, text2):
    d = difflib.Differ()
    diff = list(d.compare(text1.split(), text2.split()))
    return diff

def highlight_diff(diff):
    result = []
    for word in diff:
        if word.startswith("+ "):
            result.append(f'<span style="background-color: lightgreen;">{word[2:]}</span>')
        elif word.startswith("- "):
            result.append(f'<span style="background-color: lightcoral;">{word[2:]}</span>')
        elif word.startswith("? "):
            result.append(f'<span style="background-color: lightyellow;">{word[2:]}</span>')
        else:
            result.append(word[2:])
    return ' '.join(result)

def summarize_diff(diff):
    added = sum(1 for word in diff if word.startswith('+ '))
    removed = sum(1 for word in diff if word.startswith('- '))
    modified = sum(1 for word in diff if word.startswith('? '))
    return {
        'Added': added,
        'Removed': removed,
        'Modified': modified
    }

def check_phone(s):
    if len(s) > 30:
        return False
    n = 0
    for i in s:
        if i in '0123456789':
            n += 1
    return n == 10
from annotator.name.check_name import check_name
from annotator.position.check_position import check_position
from annotator.phone.check_phone import check_phone
from annotator.research.check_research import check_research

def check_email(s):
    s = s.lower()
    if '@' in s and ('.edu' in s or '.com' in s):
        return True
    return False

def annotate(s):
    if check_position(s):
        return 'Position'
    if check_email(s):
        return 'Email'
    if check_phone(s):
        return 'Phone number'
    if check_name(s):
        return 'Name'
    if check_research(s):
        return 'Research Interest'
    return 'None'
    
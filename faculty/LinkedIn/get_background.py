import json

# extract experience from the parsed html
def get_experience(html):
    res = []
    tag_stack = []
    education_area = False
    cur_education = []
    hidden = ''
    for line in html:
        # sign of experience field
        if 'pv-entity__position-group-pager pv-profile-section__list-item ember-view' in line:
            education_area = True

        if education_area:
            if line[:4] == '<img' or line[:3] == '<br' or line[:2] == '<!':
                continue
            if len(line) > 2 and line[:2] == '</':
                tag_stack.pop()
                if not tag_stack:
                    res.append(cur_education)
                    cur_education = []
                    education_area = False
            elif len(line) > 2 and line[:1] == '<' and line[1] != '!':
                if 'visually-hidden' in line:
                    tag_stack.append('<span class="visually-hidden">')
                else:
                    tag_stack.append(line.split()[0] + '>')
            else:
                tmp = line.strip()
                if not tmp or line[:2] == '<!' or 'visually-hidden' in tag_stack[-1]:
                    if 'visually-hidden' in tag_stack[-1]:
                        hidden = tmp
                    continue
                if hidden:
                    cur_education.append([hidden, line.strip()])
                    hidden = ''
                else:
                    cur_education.append(line.strip())
    return res


def get_education(html):
    res = []
    tag_stack = []
    education_area = False
    cur_education = []
    hidden = ''
    dates = False
    for line in html:
        if 'pv-profile-section__list-item pv-education-entity pv-profile-section__card-item ember-view' in line:
            education_area = True
        if education_area:
            if line[:4] == '<img' or line[:3] == '<br' or line[:2] == '<!':
                continue
            if len(line) > 2 and line[:2] == '</':
                tag_stack.pop()
                if not tag_stack:
                    res.append(cur_education)
                    cur_education = []
                    education_area = False
            elif len(line) > 2 and line[:1] == '<' and line[1] != '!':
                if 'visually-hidden' in line:
                    tag_stack.append('<span class="visually-hidden">')
                else:
                    tag_stack.append(line.split()[0] + '>')
            else:
                tmp = line.strip()
                if not tmp or line[:2] == '<!' or 'visually-hidden' in tag_stack[-1]:
                    if 'visually-hidden' in tag_stack[-1]:
                        hidden = tmp
                    continue
                if hidden:
                    cur_education.append([hidden, line.strip()])
                    hidden = ''
                else:
                    line = line.strip()
                    if line == '–':
                        cur_education[-1][-1] += ' - '
                        dates = True
                    elif dates:
                        cur_education[-1][-1] += line
                        dates = False
                    else:
                        line = line.replace('–', '-')
                        cur_education.append(line)
    return res

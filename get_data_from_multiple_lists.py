import time
import urllib.request
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ECg
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from collections import defaultdict
import string
from find_possible_list import find_possible_list
from find_possible_list import find_info_in_grandchildren
import os
import pathlib
from annotator.annotator import annotate


abs_path = str(pathlib.Path(__file__).parent.absolute()) + '/'

# given an url, store the html into a list. Each element of this list is either a tag or a text element. Return this list.
def get_html(url, scrape_option):
    # flag = False
    faculty_image = []
    the_page = ''
    if scrape_option == 'urllib':
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                the_page = response.read()
            the_page = (str(the_page))
        except:
            # print("cannot crawl")
            # flag = True
            return []
    else:
        try:
            option = webdriver.ChromeOptions()
            option.add_argument(' — incognito')
            option.add_argument('--no - sandbox')
            option.add_argument('--window - size = 1420, 1080')
            option.add_argument('--headless')
            option.add_argument('--disable - gpu')
            driver1 = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver',
                                       chrome_options=option)
            driver1.get(url)
            time.sleep(1)
            the_page = str(driver1.page_source)
            # print(the_page)
            time.sleep(2)
        except:
            return []

    result = []
    line = ""
    for i in the_page:
        if i == '<':
            if len(line) != 0:
                result.append(line)
            line = "<"
        elif i == '>':
            line += '>'
            result.append(line)
            line = ""
        else:
            line += i
    result.append(line)
    return result


# given a url and a scrape_option (urllib or selenium), return faculty's info
def view_html_structure(url, scrape_option, known_html=[], wrong_words=[]):
    html = []
    if len(known_html) == 0:
        html = get_html(url, scrape_option)
    else:
        html = known_html
    if not html:
        return {}

    # html_structure.txt is for debuging purpose, displaying each tag with its corespoing index in raw_html (see below)
    f = open(abs_path + 'html_structure.txt', 'w')

    # raw_html.txt is for debuging purpose, if a text element has no tag, we will give it a tag called <no_tag>
    f1 = open(abs_path + 'raw_html.txt', 'w')

    # raw_html is corresponding to raw_html.txt
    raw_html = []

    for j in range(len(html)):
        i = html[j]
        i = i.replace('\\n', '')
        i = i.replace('\\t', '')
        i = i.replace('\\r', '')
        i = i.replace('&nbsp;', '')
        while '  ' in i:
            i = i.replace('  ', ' ')
        if len(i) == 0 or i == ';':
            i = ' '
        if i != ' ' and i[0] != '<' and 0 < j < len(html) - 1 and (
                html[j + 1][:2] != '</' or html[j - 1][:2] == '</' or html[j - 1][:3] == '<br'):
            a = i.strip()
            if a in string.punctuation:
                continue
            raw_html.append('<no_tag>')
            raw_html.append(i)
            raw_html.append('</no_tag>')
            f1.write('<no_tag>\n')
            f1.write(i + '\n')
            f1.write('</no_tag>\n')
        else:
            raw_html.append(i)
            f1.write(i + '\n')
    
    # html_structure is corresponding to html_structure.txt
    html_structure = []

    body_found = False
    count = 0
    for i in raw_html:
        count += 1
        if not body_found:
            if '<body' in i:
                body_found = True
            else:
                continue
        if len(i) == 0 or i[0] != '<':
            continue
        if ' ' in i:
            i = i[:i.index(' ')] + '>'
        if '\\n' in i:
            i = i[:i.index('\\n')] + '>'
        if '%' in i:
            i = i[:i.index('%')] + '>'
        f.write(i + str(count - 1) + '\n')
        html_structure.append([i, count - 1])
    f.close()

    # html_structure is a list, stroing the tree strucuture of raw_html
    # each element in html_structure contains all nodes (tags) at certain level of the html tree
    # each level is also a list, and each element in a level represent a node (tag)
    # each node element has 4 fields
    #   the first field is the index of its parent node in the level above
    #   the second field is the name of its tag
    #   the third and fourth field represent its range (the line it covers) in raw_html (also corresponding to raw_html.txt)
    #   e.g. a html tree with the following structure:
    # 0   <div>
    # 1      <li>
    # 2          an
    # 3      </li>
    # 4      <li>
    # 5          example
    # 6      </li>
    # 7   </div>
    #   then html_structure would be:
    #   [
    #       [[0, '<div>', 0, 7]],                       # level 0
    #       [[0, '<li>', 1, 3], [0, '<li>', 4, 6]]      # level 1
    #   ]
    #   meanwhile, raw_html is [<div>, <li>, an, </li>, <li>, example, </li>, </div>]
    #   and therefore, we can get the text element of each leaf node
    #   e.g. leaf nod [0, '<li>', 1, 3] indicates that this node is spanning from idx 1 to idx 3, so its text element should has idx 2 in raw_html, which is 'an'
    root = [0]
    root.extend(html_structure[0])
    html_tree = [[root]]
    level = 0
    for i in html_structure[1: -1]:
        if '<!--' in i[0] or 'br' in i[0] or '\\' in i[0] or '<img' in i[0] or '<input' in i[0] or '<meta' in i[0] or '<hr>' in i[0]:
            continue
        if '/' != i[0][1]:
            level += 1
            if level > len(html_tree) - 1:
                html_tree.append([])
            html_tree[level].append([len(html_tree[level - 1]) - 1, i[0], i[1]])
        else:
            l = level
            try:
                while html_tree[level][-1][1] != '<' + i[0][2:]:
                    level -= 1
                    assert (level >= 0)
            except:
                level = l
                continue
            html_tree[level][-1].append(i[1])
            level -= 1
    
    # uncomment the following code to see the content of html_tree
    # for i in html_tree:
    #     print(len(i), i)

    # path_dict: keys are text types we are looking for such as names and positions, values are lists of corresponding tag path that lead to each target field
    #            we use a list of index of tags in html_structure to represent each tag path
    #            e.g. a tag path, [0, 1], in the example above would represent <div><li(2)> (the second <li> in level 1), and this tag path is leading to text element 'example'
    path_dict = {}

    # parent_nodes stores the idx of the nodes in the current level that are not leaf
    parent_nodes = []
    
    for level in range(len(html_tree) - 1, -1, -1):
        # print(parent_nodes)
        grandparents = []
        for i in range(len(html_tree[level])):
            if html_tree[level][i][0] not in grandparents:
                grandparents.append(html_tree[level][i][0])
            
            # if a node is a leaf, than it must be the direct parent to a text element
            if i not in parent_nodes:
                if raw_html[html_tree[level][i][2] + 1][0] == '<' or raw_html[html_tree[level][i][2] + 1] == ' ':
                    continue

                r = annotate(raw_html[html_tree[level][i][2] + 1])

                # print the (type, text) tuples if type is not None (None type means noise)
                # if r != 'None':
                #     print(r, '---', raw_html[html_tree[level][i][2] + 1])

                if r != 'None':
                    path = []
                    cur_level = level
                    node_idx = html_tree[cur_level][i][0]

                    # this while loop finds the tag path leading to the text element
                    while cur_level >= 1:
                        path.append(node_idx)
                        cur_level -= 1
                        node_idx = html_tree[cur_level][node_idx][0]
                    
                    if r not in path_dict.keys():
                        path_dict[r] = []
                    path = path[::-1]
                    path.append(i)
                    path_dict[r].append(list(path))

        parent_nodes = grandparents
    
    # print path_dict
    # for i in path_dict:
    #     print(i)
    #     for j in path_dict[i]:
    #         print(j)
    #     print()

    # for i in path_dict.keys():
    #     for j in path_dict[i]:
    #         t = []
    #         n = 0
    #         for k in j:
    #             t.append(html_tree[n][k][1])
    #             n += 1
            # print(i, j, raw_html[html_tree[n - 1][k][2] + 1], t, html_tree[n - 1][k])
            # print(i, raw_html[html_tree[n - 1][k][2] + 1])

    candidate_num = sum([len(path_dict[i]) for i in path_dict.keys()])

    # common_structure is the tag path leading to the target cluster, a sub html-tree whose leaf nodes covers all target data
    common_structure = []

    # find the cluster in HTML that is most likely to contain a list faculty info
    while True:
        # count remembers the occurance of each node
        count = {}

        for text_type in path_dict.keys():
            for path in path_dict[text_type]:
                if len(common_structure) >= len(path) or path[: len(common_structure)] != common_structure:
                    continue
                node = path[len(common_structure)]
                if node not in count.keys():
                    count[node] = 0
                count[node] += 1
        candidate_nodes = []
        for i in count.keys():
            candidate_nodes.append([i, count[i]])
        # print(t)
        candidate_nodes = sorted(candidate_nodes, key=lambda x: x[1], reverse=True)
        if candidate_nodes and candidate_nodes[0][1] > 0.2 * candidate_num:
            common_structure.append(candidate_nodes[0][0])
        else:
            break
    # print(common_structure)

    final_result = []

    # find names, positions, emails, phones, and research interests under the cluster, which is represented by common_structure
    def find_all_target_data(common_structure, correct_subtree_path={}):
        # print(common_structure)
        l = len(common_structure)

        # all tag path in accurate_path_dict would share the same common_structure
        accurate_path_dict = {}
        for text_type in path_dict.keys():
            accurate_path = []
            for tag_path in path_dict[text_type]:
                if tag_path[:l] == common_structure:
                    accurate_path.append(tag_path.copy())
            accurate_path_dict[text_type] = accurate_path
        # print('\n', accurate_path_dict, '\n')

        # each root is the root of a subtree containing information of a single faculty member
        subtree_roots = []

        for i in range(len(html_tree[len(common_structure)])):
            if html_tree[len(common_structure)][i][0] == common_structure[-1]:
                t = html_tree[len(common_structure)][i].copy()
                t.append(i)
                subtree_roots.append(t)
        # print(subtree_roots)

        # return a list of subtrees rooted at the children of the root node
        def get_subtree(n):
            root = []
            for i in subtree_roots:
                try:
                    if i[4] == n:
                        root = i.copy()
                except:
                    return []
            if len(root) == 0:
                return []
            result = [root.copy()]
            level = len(common_structure) + 1
            pre = [root.copy()]
            while True:
                cur = []
                for i in pre:
                    if level > len(html_tree) - 1:
                        continue
                    for j in range(len(html_tree[level])):
                        # print(j, i)
                        if len(i) != 5:
                            continue
                        if html_tree[level][j][0] == i[4]:
                            tmp = html_tree[level][j].copy()
                            tmp.append(j)
                            cur.append(tmp)
                if len(cur) == 0:
                    break
                pre = cur
                level += 1
                result.append(cur.copy())
            return result

        # keys are roots, values are trees with the same structures as html_structure
        subtree_dict = {}

        for i in subtree_roots:
            if get_subtree(i[-1]) != []:
                subtree_dict[i[-1]] = get_subtree(i[-1])

        # the following for-loop converts tag of each node into tag-path leading to each node
        for i in subtree_dict.keys():
            # print(i, subtree_dict[i])
            subtree_dict[i][0].append(str(subtree_dict[i][0][-1]) + '-')
            subtree_dict[i][0] = [subtree_dict[i][0].copy()]
            for j in range(1, len(subtree_dict[i])):
                seen_tag = set()
                for node in subtree_dict[i][j]:
                    tag = node[1]
                    for k in subtree_dict[i][j - 1]:
                        if k[-2] == node[0]:
                            tag = k[1] + tag
                            node.append(k[-1] + str(node[-1]) + '-')
                    a = raw_html[node[2]]
                    if 'class="' in a:
                        a = a[a.index('class="') + 7:]
                        a = a[:a.index('"')]
                        if ' ' in a and any(char.isdigit() for char in a[a.index(' '):]):
                            a = a[:a.index(' ')]
                        tag = tag[:-1] + ' ' + a[:a.find(' ')] + '>'
                    
                    # making each tag unique
                    while tag in seen_tag:
                        tag = tag[:-1] + '@' + '>'
                    seen_tag.add(tag)

                    node[1] = tag
        
        # for i in subtree_dict.keys():
        #     print(i, subtree_dict[i])

        translation = {}
        for i in subtree_dict:
            for j in subtree_dict[i]:
                for k in j:
                    # print(k)
                    translation[k[-1]] = k[1]

        # find tag path leading to each field of interest
        subtree_path = {}
        if len(correct_subtree_path.keys()) > 0:
            subtree_path = correct_subtree_path
        else:
            for i in accurate_path_dict.keys():
                subtree_path[i] = {}
                for j in accurate_path_dict[i]:
                    a = ''
                    for k in range(len(common_structure), len(j)):
                        a += str(j[k]) + '-'
                    try:
                        if translation[a] not in subtree_path[i].keys():
                            subtree_path[i][translation[a]] = 0
                        subtree_path[i][translation[a]] += 1
                    except:
                        continue

            # print(subtree_path)

            # solve conficts caused by the bad performance of the classifier, which may cause 2 target fields (such as position or research) have the same tag path
            for x in range(3):
                for i in subtree_path.keys():
                    for j in subtree_path.keys():
                        if i != j:
                            try:
                                a, b = max(subtree_path[i], key=subtree_path[i].get), max(subtree_path[j],
                                                                                          key=subtree_path[j].get)
                            except:
                                continue
                            if a == b:
                                a1 = subtree_path[i][a]
                                b1 = subtree_path[j][b]
                                if a1 > b1:
                                    subtree_path[j][a] = 0
                                else:
                                    subtree_path[i][a] = 0
            # print(subtree_path)
            
            # find the best tag path leading to each target field
            # common_subtree_path: keys are target types, values are tag path
            common_subtree_path = {}
            for i in subtree_path.keys():
                if len(subtree_path[i].keys()) == 0 or subtree_path[i][max(subtree_path[i], key=subtree_path[i].get)] == 0:
                    common_subtree_path[i] = 'None'
                else:
                    common_subtree_path[i] = max(subtree_path[i], key=subtree_path[i].get)
            # print(common_subtree_path)

            # resolve conflicts when two target fields are assigned with the same tag path in mistake
            final_subtree_path = {}
            for i in subtree_path.keys():
                if common_subtree_path[i] == 'None':
                    final_subtree_path[i] = 'None'
                else:
                    # print(i)
                    t1 = defaultdict(int)
                    for j in subtree_path[i].keys():
                        t1[j[:j.rfind('<')]] += subtree_path[i][j]
                    a1 = max(t1, key=t1.get)
                    flag1 = True
                    s = set([])
                    for j in common_subtree_path.keys():
                        if j != i:
                            s.add(common_subtree_path[j])
                    t_max = 0
                    t_sum = 0
                    for j in subtree_path[i].keys():
                        if j[:j.rfind('<')] == a1:
                            if j in s:
                                flag1 = False
                            else:
                                t_max = max(t_max, subtree_path[i][j])
                                t_sum += subtree_path[i][j]
                    if flag1 and t_sum / t_max > 1.85:
                        final_subtree_path[i] = a1
                    else:
                        final_subtree_path[i] = common_subtree_path[i]

            for i in subtree_path.keys():
                subtree_path[i] = final_subtree_path[i]

        # for each tag path in a subtree, store its corresponding text element
        path_to_result = {}
        for i in subtree_dict.keys():
            path_to_result[i] = {}
            for j in subtree_dict[i]:
                for k in j:
                    path_to_result[i][k[1]] = [k[2], k[3]]
        # print(path_to_result)

        # apply "anchor point" technique
        # if we used anchor point to locate data, tag path won't be string
        if len(correct_subtree_path) == 0:
            for i in subtree_path.keys():
                if subtree_path[i] == 'None' or ' ' in subtree_path[i][subtree_path[i].rfind('<'):]:
                    continue
                case_of_single_child = 0
                for j in path_to_result.keys():
                    if (subtree_path[i][:-1] + '@' + '>') not in path_to_result[j].keys():
                        case_of_single_child += 1
                if case_of_single_child == len(path_to_result):
                    continue
                parent = subtree_path[i][:subtree_path[i].rfind('<')]
                stem = subtree_path[i][len(parent):]
                stem = stem.replace('@', '')
                stem = parent + stem
                stem = stem[:-1]
                anchor_points = {'start': {}, 'end': {}}
                candidates = {}
                for j in path_to_result.keys():
                    for k in path_to_result[j].keys():
                        if len(k) > len(parent) and parent in k and k[len(parent):].rfind('<') == 0:
                            tmp = k[len(parent):]
                            if ' ' in tmp or ('@' not in tmp and k[:-1] + '@>' not in path_to_result[j].keys()):
                                if k not in candidates.keys():
                                    candidates[k] = 0
                                candidates[k] += 1
                for j in candidates.keys():
                    if candidates[j] >= 0.95 * len(path_to_result):
                        anchor_points[j] = {}
                # print(i, anchor_points)
                for j in accurate_path_dict[i]:
                    path_in_subtree = j[len(common_structure):]
                    subtree_dict_key = path_in_subtree[0]
                    string_path = ''
                    for k in path_in_subtree:
                        string_path += str(k) + '-'
                    parent_string_path = string_path[:string_path[:-1].rfind('-') + 1]
                    parent_name = -1
                    # print(subtree_dict_key)
                    # print(parent_string_path.count('-'))
                    try:
                        for k in subtree_dict[subtree_dict_key][parent_string_path.count('-') - 1]:
                            if k[-1] == parent_string_path:
                                parent_name = k[-2]
                        siblings = []
                        for k in subtree_dict[subtree_dict_key][string_path.count('-') - 1]:
                            if k[0] == parent_name:
                                siblings.append(k.copy())
                        target_index = -1
                    except:
                        continue
                    for k in range(len(siblings)):
                        if siblings[k][-1] == string_path:
                            if siblings[k][1][:len(stem)] != stem:
                                break
                            target_index = k
                    if target_index == -1:
                        continue
                    if target_index not in anchor_points['start'].keys():
                        anchor_points['start'][target_index] = 0
                    anchor_points['start'][target_index] += 1
                    if -1 * (len(siblings) - target_index - 1) not in anchor_points['end'].keys():
                        anchor_points['end'][-1 * (len(siblings) - target_index - 1)] = 0
                    anchor_points['end'][-1 * (len(siblings) - target_index - 1)] += 1
                    for k in anchor_points.keys():
                        if k != 'start' and k != 'end':
                            anchor_index = -1
                            for kk in range(len(siblings)):
                                if siblings[kk][1] == k:
                                    anchor_index = kk
                            if anchor_index == -1:
                                continue
                            anchor_index = target_index - anchor_index
                            if anchor_index not in anchor_points[k].keys():
                                anchor_points[k][anchor_index] = 0
                            anchor_points[k][anchor_index] += 1

                # print(anchor_points)
                best_anchor_point = []
                for j in anchor_points.keys():
                    best_anchor_point.append([j, max(anchor_points[j].values()) / sum(anchor_points[j].values())])
                best_anchor_point = sorted(best_anchor_point, key=lambda x: x[1], reverse=True)
                best_anchor_point = [best_anchor_point[0][0], best_anchor_point[0][1]]
                best_anchor_point[1] = max(anchor_points[best_anchor_point[0]], key=anchor_points[best_anchor_point[0]].get)
                if best_anchor_point[0] == 'start' or best_anchor_point[0] == 'end':
                    best_anchor_point.append(parent)
                # print(best_anchor_point)
                # print()
                subtree_path[i] = best_anchor_point.copy()

        # print(subtree_path)

        # extracting all target text elements 
        result = []
        total_miss, total_num, total_match = 0, 1, 0
        for i in path_to_result.keys():
            d = {}
            missing = 0
            match = 0
            for j in subtree_path.keys():
                p = subtree_path[j]
                # check if anchor points are used
                if isinstance(p, str):
                    if p not in path_to_result[i].keys():
                        p = p[:p.rfind('<')]
                        if p in path_to_result[i].keys() and path_to_result[i][p][1] - path_to_result[i][p][0] > 2:
                            p = subtree_path[j]
                    if p not in path_to_result[i].keys():
                        p = p[:p.rfind('<')]
                        if p in path_to_result[i].keys() and path_to_result[i][p][1] - path_to_result[i][p][0] > 2:
                            p = subtree_path[j]
                    if p in path_to_result[i].keys():
                        a = ''
                        for k in range(path_to_result[i][p][0], path_to_result[i][p][1]):
                            if raw_html[k][0] != '<':
                                a += raw_html[k] + ' '
                        a = a.replace('\n', ' ')
                        if ' ' in a:
                            a = a[:-1]
                        # print(j + ': ' + a)
                        d[j] = a
                        total_match += 1
                    else:
                        # print(j + ': missing')
                        d[j] = 'Missing'
                        missing += 1
                else:
                    try:
                        parent = ''
                        if p[0] == 'start' or p[0] == 'end':
                            parent = p[-1]
                        else:
                            parent = p[0][:p[0].rfind('<')]
                        siblings = []
                        for kk in subtree_dict[i][parent.count('<')]:
                            if kk[1][:len(parent)] == parent:
                                siblings.append(kk.copy())
                        position = -1
                        if p[0] == 'start':
                            position = p[1]
                        elif p[0] == 'end':
                            position = len(siblings) - 1 + p[1]
                        else:
                            for k in range(len(siblings)):
                                if siblings[k][1] == p[0]:
                                    position = k + p[1]
                        if 0 <= position < len(siblings):
                            a = ''
                            for k in range(siblings[position][2], siblings[position][3]):
                                if raw_html[k][0] != '<':
                                    a += raw_html[k] + ' '
                            a = a.replace('\n', ' ')
                            if ' ' in a:
                                a = a[:-1]
                            # print(j + ': ' + a)
                            d[j] = a
                            total_match += 1
                        else:
                            # print(j + ': missing')
                            d[j] = 'Missing'
                            missing += 1
                    except:
                        # print(j + ': missing')
                        d[j] = 'Missing'
                        missing += 1

            # print()
            if missing < 4:
                result.append(d.copy())
            total_miss += missing
            total_num += 5
        # print(subtree_path)
        # print('--------------------------------------------------------------------')

        try:
            # handle the case when each cell of faculty info is not the direct decendent of the root
            a_num, a = find_info_in_grandchildren(subtree_dict, subtree_path, raw_html)
            # print(a_num, a, total_match)

            non_empty_name_num, total_name_num = 0, len(a)
            for i in a:
                if 'Name' in a and a['Name'] != '':
                    non_empty_name_num += 1

            if a_num > total_match and non_empty_name_num / total_name_num > 0.6:
                for r in a:
                    if 'Name' in r.keys() and r['Name'] != 'Missing':
                        tmp_name = r['Name']
                        tmp_name = tmp_name.replace(',', ' ')
                        tmp_name = tmp_name.split()
                        final_result.append(r.copy())
                return subtree_path
        except:
            pass
        if total_miss / total_num > 0.8:
            # print('Warning----------Total Miss:', total_miss, '  Num: ', total_num)
            # print()
            return {}

        for r in result:
            if 'Name' in r.keys() and r['Name'] != 'Missing':
                tmp_name = r['Name']
                tmp_name = tmp_name.replace(',', ' ')
                tmp_name = tmp_name.split()
                final_result.append(r.copy())
        return subtree_path

    common_structures = find_possible_list(path_dict)
    true_path = {}
    for i in common_structures:
        # print(true_path)
        try:
            r = find_all_target_data(i, true_path)
            # print('r', r)
            if 'Name' in r.keys() and r['Name'] != 'None':
                for j in r.keys():
                    true_path[j] = r[j]
        except:
            continue

    noise = []
    for i in ['Name', 'Position', 'Research Interest', 'Email', 'Phone number']:
        m = {}
        t = 0.01
        for j in final_result:
            if i in j.keys() and j[i] != 'Missing':
                if j[i] not in m.keys():
                    m[j[i]] = 0
                m[j[i]] += 1
                t += 1
        if len(m) > 0 and max(m.values()) / t > 0.93:
            noise.append(max(m, key=m.get))
    # print(wrong_words)
    # print(final_result)
    if len(noise) > 0:

        # avoid infinite loop
        for i in noise:
            if i in wrong_words:
                return final_result
        for i in wrong_words:
            noise.append(i)
        final_result = []
        return view_html_structure(url, scrape_option, html, noise)

    return final_result


# example
# a = view_html_structure('https://cs.illinois.edu/about/people/all-faculty', 'urllib')
# for i in a:
#     print(i)

# a = view_html_structure('https://www.eecs.mit.edu/role/faculty/?fwp_role=faculty&fwp_research=robotics', 'selenium')
# for i in a:
#     print(i)


# a = view_html_structure('https://udayton.edu/directory/artssciences/computerscience/index.php', 'selenium')
# for i in a:
#     print(i)
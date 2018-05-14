import re
from collections import OrderedDict
from collections import defaultdict

Rules = OrderedDict()
terminals = []
non_terminals = []
first_set = {}
follow_set = {}
parsing_table = {}


def parsing_table(rules, first, follow):
    parsing_table = defaultdict(dict)
    for x in non_terminals:
        for y in terminals:
            if y == "\L":
                parsing_table[x]["$"] = None
            else:
                parsing_table[x][y] = None

    for nonterminal, productions in rules.items():
        prod_buff = []
        stringaya = ""
        flag = False
        #7aga 3'abeya gedan matrkezsh m3aha awi ana hab2a ashr7-ha
        if "|" in productions:
            flag = True
            prod_buff = productions.split("|")
            prod_buff[0] = prod_buff[0][:-1]
            x = 1
            while x < len(prod_buff):
                prod_buff[x] = prod_buff[x][1:]
                x += 1

        for element in productions.replace("'", "").split("|"):
            index = 0
            "handling spaces"
            for x in element:
                if x == ' ':
                    if index == 0:
                        element = element[1:]
                        index = index - 1
                    elif index == len(element) - 1:
                        element = element[:-1]
                    else:
                        element = element[:index]
                        break
                index += 1
            if element == nonterminal:
                print "ERROR ! - LEFT FACTORING/RECURSION 7abibi !!"
                break

            if element in non_terminals:
                for temp in first[nonterminal]:
                    stringaya = str(nonterminal) + '->' + str(productions)
                    if parsing_table[nonterminal][temp] is None:
                        parsing_table[nonterminal][temp] = stringaya
                    else:
                        print "ERROR ya baba !!"

            elif element in terminals:
                if element == "\L":
                    # EPSILON HANDLING
                    for term in follow[nonterminal]:
                        parsing_table[nonterminal][term] = str(nonterminal) + '->' + "\L"
                    continue
                # bashof kan 3andi OR wla la2
                if flag:
                    for text in prod_buff:
                        # EPSILON HANDLING
                        if text == "\L" or element == "\L":
                            continue
                        if element in text:
                            stringaya = str(nonterminal) + '->' + str(text)
                else:
                    stringaya =str(nonterminal) + ' -> ' + str(productions)

                parsing_table[nonterminal][element] = stringaya

    return parsing_table


def handling_spaces(partition):
    index = 0
    "handling spaces"
    for x in partition:
        if x == ' ':
            if index == 0:
                partition = partition[1:]
                index = index - 1
            elif index == len(partition) - 1:
                partition = partition[:-1]
            else:
                continue
        index += 1
    return partition


def calculate_first(rules, terminals, non_terminals):
    first = {}
    for nonterminal , productions in reversed(rules.items()):
        elementbuffer = []
        for element in productions.replace("'", "").split("|"):
            index = 0
            "handling spaces"
            for x in element:
                if x == ' ':
                    if index == 0:
                        element = element[1:]
                        index = index - 1
                    elif index == len(element) - 1:
                        element = element[:-1]
                    else:
                        element =element[:index]
                        break
                index += 1

            #handling if non terminal = first nonterminal in production
            if nonterminal == element:
                continue
            if element in elementbuffer:
                continue
            else:
                elementbuffer.append(element)


            #handling el terminals
            if element in terminals:
                if element not in first:
                    first.setdefault(nonterminal, [])
                    first[nonterminal].append(element)
                else:
                    first[nonterminal].append(element)
            #handling el non terminals
            elif element in non_terminals:
                if nonterminal not in first:
                    first.setdefault(nonterminal, [])
                    for temp in first[element]:
                        first[nonterminal].append(temp)

                else:
                    for temp in first[element]:
                        first[nonterminal].append(temp)

    return first


def calculate_follow(rules, terminals, nonterminals, first):
    follow = {}
    follow.setdefault(list(Rules.keys())[0], [])
    follow[list(Rules.keys())[0]].append('$')
    for nonterminal, production in rules.items():
            curr_nonterminal = nonterminal
            for i_nonterminal, productions in rules.items():
                for partition_of_production in productions.replace("'", "").split("|"):
                    partition_of_production = handling_spaces(partition_of_production)
                    divided_elements = partition_of_production.split(" ")
                    if divided_elements[-1] == '':
                        divided_elements = divided_elements[:-1]
                    if curr_nonterminal in divided_elements:



                        #if there is terminal/nonterminal after the nonterminal that we want to calculate its follow
                        if (divided_elements.index(curr_nonterminal ) + 1) < len(divided_elements):
                            #check if it is a terminal or non terminal
                            #terminal case
                            if divided_elements[divided_elements.index(curr_nonterminal ) + 1] in terminals:
                                if curr_nonterminal not in follow:
                                    follow.setdefault(curr_nonterminal, [])
                                    follow[curr_nonterminal].append(divided_elements[divided_elements.index(curr_nonterminal ) + 1])
                                else:
                                    if divided_elements[divided_elements.index(curr_nonterminal ) + 1] not in follow[curr_nonterminal]:
                                        follow[curr_nonterminal].append(divided_elements[divided_elements.index(curr_nonterminal ) + 1])
                            # nonterminal case A --> ABC/ follow of B = First of C
                            elif divided_elements[divided_elements.index(curr_nonterminal ) + 1] in nonterminals:
                                        firstofnext = first[divided_elements[divided_elements.index(curr_nonterminal ) + 1]]
                                        for i in firstofnext:
                                            if curr_nonterminal not in follow and i != '\L':
                                                follow.setdefault(curr_nonterminal, [])
                                                follow[curr_nonterminal].append(i)
                                            else:
                                                if i not in follow[curr_nonterminal] and i != '\L':
                                                    follow[curr_nonterminal].append(i)

                                        if '\L' in firstofnext and not (divided_elements.index(curr_nonterminal) + 2) < len(divided_elements):
                                            #handling epsilon
                                            # copying values from list
                                            # A---> B'\L'
                                            for i in follow[i_nonterminal]:
                                                if curr_nonterminal not in follow and i != '\L':
                                                    follow.setdefault(curr_nonterminal, [])
                                                    follow[curr_nonterminal].append(i)
                                                else:
                                                    # check for redundancy then add
                                                    if i not in follow[curr_nonterminal] and i != '\L':
                                                        follow[curr_nonterminal].append(i)
                                        # elif '\L' in firstofnext and (divided_elements.index(curr_nonterminal) + 2) < len(divided_elements):
                                        #     #A --> B '\L' C  CASE NOT INCLUDED IN SLIDES
                                        #     firstofnextnext = first[divided_elements[divided_elements.index(curr_nonterminal) + 2]]
                                        #     for i in firstofnext:
                                        #         if curr_nonterminal not in follow:
                                        #             follow.setdefault(curr_nonterminal, [])
                                        #             follow[curr_nonterminal].append(i)
                                        #         else:
                                        #             if i not in follow[curr_nonterminal]:
                                        #                 follow[curr_nonterminal].append(i)





                        #if it is the last symbol in the production and it is A ---> BA / do nothing
                        elif i_nonterminal == curr_nonterminal:
                            continue
                        #else A --->B/ follow of B = follow of A
                        else:
                            #copying values from list
                            for i in follow[i_nonterminal]:
                                    if curr_nonterminal not in follow and i != '\L':
                                        follow.setdefault(curr_nonterminal, [])
                                        follow[curr_nonterminal].append(i)
                                    else:
                                        # check for redundancy then add
                                        if i not in follow[curr_nonterminal] and i != '\L':
                                            follow[curr_nonterminal].append(i)

    return follow



     #printing rules
     # for nonterminal, productions in rules.items():
     #    print nonterminal + " ---> " + productions


def parser(parse_table, tokens):
    stack = []
    # PUSH $ into stack
    stack.append("$")
    # PUSH Starting symbol into stack
    stack.append(non_terminals[0])
    stack_symbol = stack.pop()
    while len(tokens) > 0:
        token = tokens.pop()
        while parse_table[stack_symbol][token] is not None:
            production = parse_table[stack_symbol][token]
            production = production.replace("'", "").split("->")
            production = production[1].split(" ")
            for symbol in production:
                stack.append(symbol)
                stack_symbol = symbol
        if parse_table[stack_symbol][token] is None:
            print stack_symbol,token
            print stack
            print 'hey'
    return


with open("CFG.txt", "r") as x:
    for line in x:
        line = line.rstrip()
        if '#' in line:
            line = line[1:]
            line = line.split('::=')
            line[0] = line[0][:-1]
            non_terminals.append(line[0])
            line[1] = line[1][1:]
            Rules[line[0]] = line[1]
            if "'" in line[1]:
                non_t = re.findall(r"'(.*?)'", line[1], re.DOTALL)
                for element in non_t:
                    if element not in terminals:
                        terminals.append(element)


first = calculate_first(Rules, terminals, non_terminals)
print 'First = ' + str(first)
follow = calculate_follow(Rules, terminals, non_terminals, first)
print "follow = " + str(follow)
parse_table = parsing_table(Rules, first, follow)
#print parse_table
tokens = ['$', 'id', '+', 'id']
parser(parse_table, tokens)
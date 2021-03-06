import re
from collections import OrderedDict
from collections import defaultdict

Rules = OrderedDict()
terminals = []
non_terminals = []
first_set = {}
follow_set = {}
parsing_table = {}


def left_recursion(rules, terminals, nonterminals):
    new_rules = OrderedDict()
    nonterminal_count = 0
    left_flag = 0
    lst = []
    for nonterminal, productions in rules.items():
        left_recursed_list = []
        correct_partition_list = []
        loop_count = 0
        partition_count_1 = 0
        partition_count_2 = 0
        for partition_of_production in productions.split("|"):
            partition_of_production = handling_spaces(partition_of_production)
            divided_elements = partition_of_production.split(" ")
            if divided_elements[-1] == '':
                divided_elements = divided_elements[:-1]
            if divided_elements[0] == nonterminal:
                # left recursion detected , set flag = 1
                left_flag = 1
                # create new non terminal
                new_nonterminal = 'X' + str(nonterminal_count)
                del divided_elements[0]
                # List of alphas

                if partition_count_1 == 0:
                    loop_count = 1
                    # adding spaces between non terminals
                    while loop_count < len(divided_elements):
                        divided_elements.insert(loop_count, ' ')
                        loop_count += 2
                    partition_count_1 += 1
                else:
                    #case of A ---> AB | AC
                    # adding spaces between non terminals
                    loop_count = 1
                    while loop_count < len(divided_elements):
                        divided_elements.insert(loop_count, ' ')
                        loop_count += 2
                    # adding '|'
                    divided_elements = ' | ' + ''.join(divided_elements) + ' ' + new_nonterminal
                    left_recursed_list.append(''.join(divided_elements))
                    continue


                divided_elements.append(str(' ' + new_nonterminal))
                left_recursed_list.append(''.join(divided_elements))
            else:
                # List of Betas
                    if partition_count_2 == 0:
                        loop_count = 1
                        #adding spaces between non terminals
                        while loop_count < len(divided_elements):
                            divided_elements.insert(loop_count, ' ')
                            loop_count += 2
                        correct_partition_list.append(''.join(divided_elements))
                        partition_count_2 += 1
                    else:
                        # adding spaces between non terminals
                        loop_count = 1
                        while loop_count < len(divided_elements):
                            divided_elements.insert(loop_count, ' ')
                            loop_count += 2
                        # adding '|'
                        to_be_appended = ' | ' + ''.join(divided_elements)
                        correct_partition_list.append(to_be_appended)
        if left_flag == 1:
            loop_count = 0
            while loop_count < len(correct_partition_list):
                correct_partition_list[loop_count] = correct_partition_list[loop_count] + ' ' + new_nonterminal
                loop_count += 1
            lst.append(rules[nonterminal])
            new_rules[nonterminal] = ''.join(correct_partition_list)
            # then add alphas
            new_rules[new_nonterminal] = ''.join(left_recursed_list) + ' | \'\L\''

            left_flag = 0
            nonterminal_count += 1
        else:
            #if no left recursion put as is
            new_rules[nonterminal] = productions

    # for nonterminal, productions in new_rules.items():
    #      print nonterminal + " --->" + productions

    return new_rules


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
        # if we find | in the production do something else do other thing;;;
        if "|" in productions:
            prod_buff = productions.split("|")
            prod_buff[0] = prod_buff[0][:-1]
            x = 1
            while x < len(prod_buff):
                prod_buff[x] = prod_buff[x][1:]
                x += 1
            for production in prod_buff:
                original_production = production
                production = production.replace("'", "")

                if production != '\L':
                    if production[0] in terminals:
                        if production[0] in first[nonterminal]:
                            stringaya = nonterminal + '->' + original_production
                            parsing_table[nonterminal][production[0]] = stringaya

                    if production in terminals:
                        if production in first[nonterminal]:
                            stringaya = nonterminal + '->' + original_production
                            parsing_table[nonterminal][production] = stringaya

                if production in non_terminals:
                    for f in first[production]:
                        stringaya = nonterminal + '->' + original_production
                        parsing_table[nonterminal][f] = stringaya

                if production[0] in non_terminals:
                    for f in first[production[0]]:
                        stringaya = nonterminal + '->' + original_production
                        parsing_table[nonterminal][f] = stringaya

                if production == '\L':
                    stringaya = nonterminal + '->' + '\L'
                    parsing_table[nonterminal]["$"] = stringaya

        else:
            prod_buff = productions
            if prod_buff[0] in non_terminals:
                for f in first[prod_buff[0]]:
                    stringaya = nonterminal + '->' + prod_buff
                    parsing_table[nonterminal][f] = stringaya

        # Implementing PANIC ERROR ROUTINE
        for ff in follow[nonterminal]:
            if ff != "$":
                if parsing_table[nonterminal][ff] is None:
                    stringaya = 'SYNC'
                    parsing_table[nonterminal][ff] = stringaya

    # print(parsing_table)
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
    flag = True
    f = open("Output.txt", "w")
    # PUSH $ into stack
    stack.append("$")
    # PUSH Starting symbol into stack
    stack.append(non_terminals[0])
    stack_symbol = stack.pop()
    stack.append(stack_symbol)
    while len(tokens) > 0:
        flag = True
        token = tokens.pop()
        if token == "$":
            stack_symbol = stack.pop()
            stack.append(stack_symbol)
            while stack:
                if parse_table[stack_symbol][token] is not None:
                    production = parse_table[stack_symbol][token]
                    f.write(str(production)+'\n')
                    production = production.replace("'", "").split("->")
                    production = production[1].split(" ")
                    stack.pop()
                    if production == "\L":
                        stack.pop()
                        stack_symbol = stack.pop()

        if stack_symbol in terminals:
            if stack_symbol != token:
                op = 'Error: missing ' + stack_symbol + ' ,inserted'
                f.write(op+'\n')
                stack.pop()
                stack_symbol = stack.pop()
                stack.append(stack_symbol)
                tokens.append(token)
            else:
                op = 'Matched Token ' + stack_symbol
                stack.pop()
                stack_symbol = stack.pop()
                stack.append(stack_symbol)
                f.write(str(op)+'\n')
                continue

        else:
            while parse_table[stack_symbol][token] is not None and token != "$":
                production = parse_table[stack_symbol][token]
                if production == 'SYNC':
                    if token not in first[stack_symbol] and token in follow[stack_symbol]:
                        stack_symbol = stack.pop()
                        continue
                    else:
                        f.write('Error Skip ' + token + '\n')
                        break
                f.write(str(production)+'\n')
                production = production.replace("'", "").split("->")
                production = production[1].split(" ")
                stack.pop()
                for symbol in reversed(production):
                    if symbol != "\L":
                        stack.append(symbol)
                        stack_symbol = symbol
                    else:
                        stack_symbol = stack.pop()
                        stack.append(stack_symbol)
                        break

                if stack_symbol in non_terminals:
                    continue

                elif stack_symbol is "\L":
                    continue

                elif stack_symbol in terminals and stack_symbol != "\L":
                    f.write('Matched Token ' + token + '\n')
                    stack.pop()
                    stack_symbol = stack.pop()
                    stack.append(stack_symbol)
                    flag = False
                    break

        if stack_symbol in non_terminals and parse_table[stack_symbol][token] is None and flag is True:
            f.write('Error: illegal ' + stack_symbol + '- discard ' + token + '\n')
            continue
    if len(stack) == 0 and len(tokens) == 0:
        f.write('Accepted')
    f.close()
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

# Rules = left_recursion(Rules,terminals,non_terminals)
print('Terminals ', terminals)
print('Non-Terminals ', non_terminals)
first = calculate_first(Rules, terminals, non_terminals)
print 'First = ' + str(first)
follow = calculate_follow(Rules, terminals, non_terminals, first)
print "follow = " + str(follow)
parse_table = parsing_table(Rules, first, follow)

for x, y in parse_table.items():
    for z, k in parse_table.items():
        print("    " + str(z))
        print("        " + str(k))
    break


tokens = ['$','b','d','a','e','c']
parser(parse_table, tokens)

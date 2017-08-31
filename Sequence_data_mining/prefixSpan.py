import time
import resource

def parser_to_sequence(data):
    nowSid = ""
    nowTid = ""
    sequence_array = []
    sequence_items = []
    sequence_item = []
    for row in data:
        row_items = row.split()
        if row_items[0] != nowSid:
            sequence_items.append(sequence_item)
            sequence_array.append(sequence_items)
            sequence_items = []
            sequence_item = []
            sequence_item.append(row_items[2])
        else:
            if row_items[1] != nowTid:
                sequence_items.append(sequence_item)
                sequence_item = []
                sequence_item.append(row_items[2])
            else:
                sequence_item.append(row_items[2])
        nowSid = row_items[0]
        nowTid = row_items[1]
    sequence_items.append(sequence_item)
    sequence_array.append(sequence_items)
    sequence_array.pop(0)
    return sequence_array


def get_support_list(prefix_item, sequence_array, min_sup_count):
    support_table = {}
    add_items = []
    for sequence_items in sequence_array:
        for sequence_item in sequence_items:
            check_prefix_item_index = 0
            is_need_dash = False
            for sequence_item_detail in sequence_item:
                if check_prefix_item_index == len(prefix_item):
                    if len(prefix_item) != 0:
                        is_need_dash = True
                else:
                    if prefix_item[check_prefix_item_index] == sequence_item_detail:
                        check_prefix_item_index += 1
                if is_need_dash:
                    dash_sequence_item_detail = ("_" + sequence_item_detail)
                    if dash_sequence_item_detail not in add_items:
                        add_items.append(dash_sequence_item_detail)
                        if dash_sequence_item_detail in support_table:
                            support_table[dash_sequence_item_detail] += 1
                        else:
                            support_table[dash_sequence_item_detail] = 1
                else:
                    if "_" != sequence_item_detail:
                        if sequence_item_detail not in add_items:
                            add_items.append(sequence_item_detail)
                            if sequence_item_detail in support_table:
                                support_table[sequence_item_detail] += 1
                            else:
                                support_table[sequence_item_detail] = 1
                    else:
                        is_need_dash = True
        add_items = []
    support_list = list(k for k, v in support_table.iteritems() if v > min_sup_count - 1)
    return support_list


def get_new_sequence_array(prefix_item, sequence_array, support_item):
    new_sequence_array = []
    for sequence_items in sequence_array:
        def reset_sequence_items():
            new_sequence_items = list(sequence_items)
            for idx, sequence_item in enumerate(sequence_items):
                new_sequence_item = list(sequence_item)
                check_prefix_item_index = 0
                for sequence_item_detail in sequence_item:
                    if "_" in support_item:
                        if check_prefix_item_index == (len(prefix_item) - 1):
                            support_item2 = support_item.replace("_", "")
                            if support_item2 == sequence_item_detail:
                                if 1 != len(new_sequence_item):
                                    new_sequence_item.pop(0)
                                    new_sequence_item.insert(0, "_")
                                    if new_sequence_items:
                                        new_sequence_items.pop(0)
                                        new_sequence_items.insert(0, new_sequence_item)
                                else:
                                    new_sequence_item.pop(0)
                                    if new_sequence_items:
                                        new_sequence_items.pop(0)
                                if new_sequence_items:
                                    new_sequence_array.append(new_sequence_items)
                                return
                            else:
                                if 1 == len(new_sequence_item):
                                    new_sequence_items.pop(0)
                                else:
                                    new_sequence_item.pop(0)
                        else:
                            if prefix_item[check_prefix_item_index] == sequence_item_detail:
                                check_prefix_item_index += 1
                            if "_" == sequence_item_detail:
                                check_prefix_item_index = (len(prefix_item) - 1)
                            if 1 == len(new_sequence_item):
                                new_sequence_items.pop(0)
                            else:
                                new_sequence_item.pop(0)
                    else:

                        if "_" == sequence_item_detail:
                            new_sequence_items.pop(0)
                        else:
                            if support_item == sequence_item_detail:
                                if 1 != len(new_sequence_item):
                                    new_sequence_item.pop(0)
                                    new_sequence_item.insert(0, "_")
                                    if new_sequence_items:
                                        new_sequence_items.pop(0)
                                        new_sequence_items.insert(0, new_sequence_item)
                                else:
                                    new_sequence_item.pop(0)
                                    if new_sequence_items:
                                        new_sequence_items.pop(0)
                                if new_sequence_items:
                                    new_sequence_array.append(new_sequence_items)
                                return
                            else:
                                if 1 == len(new_sequence_item):
                                    new_sequence_items.pop(0)
                                else:
                                    new_sequence_item.pop(0)
        reset_sequence_items()
    return new_sequence_array


def mining_sequence(prefix_items, result_list, sequence_array, min_sup_count=10):
    support_list = []
    if prefix_items:
        support_list = get_support_list(prefix_items[-1], sequence_array, min_sup_count)
    else:
        support_list = get_support_list([], sequence_array, min_sup_count)
    for support_item in support_list:
        # print("prefix_items", prefix_items)
        # print("support_item", support_item)
        new_prefix_items = list(prefix_items)
        new_prefix_item = []
        if "_" in support_item:
            new_prefix_item = list(new_prefix_items[-1])
            new_prefix_items.pop()
            new_prefix_item.append(support_item.replace("_", ""))
        else:
            new_prefix_item.append(support_item)
        new_prefix_items.append(new_prefix_item)
        # print("new_prefix_items", new_prefix_items)
        result_list.append(new_prefix_items)
        if prefix_items:
            new_sequence_array = get_new_sequence_array(prefix_items[-1], sequence_array, support_item)
        else:
            new_sequence_array = get_new_sequence_array([], sequence_array, support_item)
        # print("new_sequence_array", new_sequence_array)
        mining_sequence(new_prefix_items, result_list, new_sequence_array, min_sup_count)


def prefix_span(abs_path="", min_sup=0.4):
    # print(parser_to_sequence(open(abs_path, mode='r')))
    sequence_array = parser_to_sequence(open(abs_path, mode='r'))
    min_sup_count = len(sequence_array) * min_sup
    print("min_sup_count", min_sup_count)
    result_list = []
    prefix_items = []
    # print("sequence_array", sequence_array)
    mining_sequence(prefix_items, result_list, sequence_array, min_sup_count)
    print("result_count", len(result_list))
    print("result_list", result_list)
    # print("min_sup_count", min_sup_count)
    return None


if __name__ == "__main__":
    min_sup = 0.01
    start = time.time()
    prefix_span("Dataset/C50S10T5N10000.ascii", min_sup)
    end = time.time()
    elapsed = end - start
    print "Time taken: ", elapsed, "seconds."
    print "Memory taken", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, "bytes"

    # a = [[['7514']], [['6790']], [['2319']], [['2313']], [['3772']], [['7860']], [['9435']], [['9632']], [['9327']], [['5181']], [['6978']], [['5539']], [['1286']], [['5621']], [['7696']], [['1375']], [['401']], [['5991']], [['3746']], [['3744']], [['2454']], [['7984']], [['2695']], [['7669']], [['6965']], [['7196']], [['1784']], [['8022']], [['8027']], [['7680']], [['8444']], [['4282']], [['4630']], [['3680']], [['4521']], [['9437']], [['2517']], [['6220']], [['1099']], [['1970']], [['3322']], [['8459']], [['6163']], [['2214']], [['6699']], [['7830']], [['2725']], [['1809']], [['6230']], [['8861']], [['810']], [['3332']], [['3337']], [['8737']], [['5671']], [['8288']], [['6500']], [['438']], [['3801']], [['9362']], [['2402']], [['930']], [['917']], [['795']], [['5259']], [['8618']], [['3876']], [['3904']], [['4762']], [['5805']], [['9713']], [['9715']], [['9004']], [['5481']], [['7790']], [['1211']], [['8068']], [['8494']], [['8085']], [['9924']], [['378']], [['9723']], [['1028']], [['6461']], [['8302']], [['6091']], [['6090']], [['5919']], [['5003']], [['7342']], [['5425']], [['8936']], [['4315']], [['8242']], [['1476']], [['8647']], [['3932']], [['3288']], [['3282']], [['3443']], [['6869']], [['5362']], [['1045']], [['8432']], [['1310']], [['6912']], [['5598']], [['8320']], [['3618']], [['4441']], [['2100']], [['1242']], [['1910']], [['3048']], [['1090']], [['4338']], [['3137']], [['8684']], [['9857']], [['4207']], [['5565']], [['4110']], [['4110', '6163']], [['3600']], [['9459']], [['8908']], [['4212']], [['7700']], [['4103']], [['139']], [['9069']], [['8974']], [['2901']], [['5319']], [['4263']], [['5547']], [['8599']], [['8371']], [['3881']], [['4663']], [['9270']], [['991']], [['7950']], [['8961']], [['1646']], [['6952']], [['2321']], [['4704']], [['4701']], [['289']], [['4647']], [['7272']], [['5088']], [['5339']], [['8773']], [['563']], [['5527']], [['7460']]]

    # print(len(a))

import csv
from collections import OrderedDict


class treeNode:
    def __init__(self, nameValue, numOccur, parentNode, myNodeLink):
        self.name = nameValue
        self.count = numOccur
        self.parent = parentNode
        self.children = {}
        self.nodeLink = myNodeLink

    def add_count(self, numOccur):
        self.count += numOccur

    def add_child(self, new_name, new_link):
        self.children[new_name] = treeNode(new_name, 1, self, new_link)
        # first_link_node_table[new_name] = self.children[new_name]
        return self.children[new_name]


def read_data_for_count(reader, min_sup):
    itemsList = []
    header_table = {}
    count = 0
    for row in reader:
        newRow = []
        count += 1
        for item in row:
            item = item.replace(" ", "")
            newRow.append(item)
            if item in header_table:
                header_table[item] += 1
            else:
                header_table[item] = 1
        itemsList.append(newRow)
    min_sup_count = min_sup * count
    header_table = dict((k, v) for k, v in header_table.iteritems() if v > min_sup_count-1)
    # headerTable = sorted(headerTable.items(), key=operator.itemgetter(1))
    header_table = OrderedDict(sorted(header_table.items(), key=lambda t: t[1], reverse=True))
    return itemsList, header_table, min_sup_count


def read_data_for_count_by_min_sup_count(reader, min_sup_count):
    itemsList = []
    header_table = {}
    count = 0
    for row in reader:
        newRow = []
        count += 1
        for item in row:
            item = item.replace(" ", "")
            newRow.append(item)
            if item in header_table:
                header_table[item] += 1
            else:
                header_table[item] = 1
        itemsList.append(newRow)
    header_table = dict((k, v) for k, v in header_table.iteritems() if v > min_sup_count-1)
    # headerTable = sorted(headerTable.items(), key=operator.itemgetter(1))
    header_table = OrderedDict(sorted(header_table.items(), key=lambda t: t[1], reverse=True))
    return itemsList, header_table, min_sup_count


def build_tree(items_list, header_table, min_sup_count):
    # print(header_table)
    new_items_list = []
    first_node = treeNode(None, 0, None, None)
    # first_link_node_table = header_table
    first_link_node_table = OrderedDict()
    # print(first_link_node_table)
    for items in items_list:
        new_items = {}
        for item in items:
            if item in header_table.keys():
                new_items[item] = header_table[item]
                # new_items.gd
        # print(new_items)
        new_items = OrderedDict(sorted(new_items.items(), key=lambda t: t[1], reverse=True))
        new_items = new_items.keys()
        new_items_list.append(new_items)
        #start to buid tree
        #to implement first_node to add child
        now_node = first_node
        for new_item in new_items:
            if new_item in now_node.children.keys():
                now_node.children[new_item].add_count(1)
                now_node = now_node.children[new_item]
            else:
                if new_item in first_link_node_table:
                    # print(new_item, first_link_node_table[new_item])
                    first_link_node_table[new_item] = now_node.add_child(new_item, first_link_node_table[new_item])

                else:
                    first_link_node_table[new_item] = now_node.add_child(new_item, None)
                # childNode = now_node.add_child(new_item, None)
                now_node = now_node.children[new_item]
                # now_node

    # print(first_link_node_table)
    return first_link_node_table


def get_new_tree_items(new_set_tree_items, last_link_node):
    while last_link_node is not None:
        condition_item = []
        condition_item_count = last_link_node.count
        parent_node = last_link_node.parent
        # print("last_link_node.name ", last_link_node.name)
        # print("last_link_node ", last_link_node)
        # print("last_link_node.parent ", last_link_node.parent)
        while parent_node.name is not None:
            condition_item.insert(0, parent_node.name)
            parent_node = parent_node.parent
        if condition_item:
            while condition_item_count != 0:
                new_set_tree_items.append(condition_item)
                condition_item_count -= 1
        last_link_node = last_link_node.nodeLink
    return None


def mining_tree(first_link_node_table, min_sup_count=0, freq_items=[], freq_item=[]):
    for last_link_node_name in reversed(first_link_node_table):
        last_link_node = first_link_node_table.pop(last_link_node_name)
        # print("last_link_node.name ", last_link_node.name)
        # print("last_link_node ", last_link_node)
        # print("last_link_node.parent ", last_link_node.parent)
        new_set_tree_items = []
        # print(last_link_node_name)
        new_freq_item = list(freq_item)
        # print("last_link_node_name", last_link_node_name)
        new_freq_item.append(last_link_node_name)
        # print("freq_item", freq_item)
        # print("new_freq_item", new_freq_item)
        freq_items.append(new_freq_item)
        # print("freq_items", freq_items)
        get_new_tree_items(new_set_tree_items, last_link_node)
        # print("new_set_tree_items", new_set_tree_items)
        if new_set_tree_items:
            items_list, header_table, min_sup_count = read_data_for_count_by_min_sup_count(new_set_tree_items, min_sup_count)
            # print("items_list", items_list)
            link_node_table = build_tree(items_list, header_table, min_sup_count)
            # print("link_node_table", link_node_table)
            if header_table:
                mining_tree(link_node_table, min_sup_count, freq_items, new_freq_item)
            else:
                freq_item = []

        # mining_tree(first_link_node_table, min_sup)


def fp_growth(abs_path="", min_sup=0.4):
    with open(abs_path, mode='r') as file:
        reader = csv.reader(file)
        items_list, header_table, min_sup_count = read_data_for_count(reader, min_sup)
        # print("items_list", items_list)
        first_link_node_table = build_tree(items_list, header_table, min_sup_count)
        # print(first_link_node_table)
        # print(next(reversed(first_link_node_table)))
        # first_link_node_table.pop(next(reversed(first_link_node_table)))
        # print(next(reversed(first_link_node_table)))
        freq_items = []

        print("min_sup_count", min_sup_count)
        mining_tree(first_link_node_table, min_sup_count, freq_items)
        print("Ans freq_items", freq_items)

    return None


if __name__ == "__main__":
    # dut_file_obj = parser("c2mftfs02.kyec.com.tw_mft-testdata.20170504232116.DUTLOG_May0417_170048_LH5016JAC1.log")
    min_sup = 0.2
    dut_file_obj = fp_growth("Dataset/test.txt", min_sup)


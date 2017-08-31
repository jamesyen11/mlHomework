import time
import csv
import resource

def parser_data(file):
	item_object = {}
	header = []
	reader = csv.reader(file)
	for idx, datas in enumerate(reader):
		if idx == 0:
			for data in datas:
				item_object[data] = []
				header.append(data)
		else:
			for idx2, data in enumerate(datas):
				if data != "":
					item_object[header[idx2]].append(data)
	return item_object


def c45(abs_path="", split_group=10, train_start=0.5):
	item_object = parser_data(open(abs_path, mode='r'))
	print(item_object)


if __name__ == "__main__":
    split_group = 10
    train_start = 0.5
    start = time.time()
    c45("Dataset/CUSTOMER.TXT", split_group, train_start)
    end = time.time()
    elapsed = end - start
    print "Time taken: ", elapsed, "seconds."
    print "Memory taken", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, "bytes"
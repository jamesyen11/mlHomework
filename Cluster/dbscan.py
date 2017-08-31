import matplotlib.pyplot as plt
import numpy


def parser_to_list(reader):
    data_list = []
    for row in reader:
        data = row.split()
        data[0] = float(data[0])
        data[1] = float(data[1])
        #0 for no visited 1 for visited 2 for noise
        data[2] = 0
        data.append(False)
        data_list.append(data)
    return data_list


def find_neighbors(all_points, p, eps):
    neighbors = []
    for other_p in all_points:
        d = ((p[0]-other_p[0])**2 + (p[1]-other_p[1])**2) ** 0.5
        if d < eps:
            neighbors.append(other_p)
    return neighbors


def expand_cluster(all_points, p, neighbors, cluster, eps, min_pts):
    cluster.append(p)
    p[3] = True
    for np in neighbors:
        if np[2] != 1:
            np[2] = 1
            np_neighbors = find_neighbors(all_points, np, eps)
            if len(np_neighbors) >= min_pts:
                for npp in np_neighbors:
                    need_add = True
                    for now_p in neighbors:
                        if npp[0] == now_p[0] and npp[1] == now_p[1]:
                            need_add = False
                    if need_add:
                        neighbors.append(npp)
        if not np[3]:
            cluster.append(np)


def dbscan(abs_path="", eps=2, min_pts=5):
    all_points = parser_to_list(open(abs_path, mode='r'))
    clusters = {}
    noises = []
    clusters["noises"] = noises
    cluster_id = 0
    for p in all_points:
        if p[2] == 1:
            continue
        neighbors = find_neighbors(all_points, p, eps)
        if len(neighbors) < min_pts:
            p[2] = 2
            noises.append(p)
        else:
            cluster = []
            clusters[cluster_id] = cluster
            cluster_id += 1
            expand_cluster(all_points, p, neighbors, cluster, eps, min_pts)
    # print(clusters[1])
    # print(clusters[2])
    print(len(all_points))
    # print(len(clusters[0]) + len(clusters[1]) + len(clusters[2]) + len(clusters["noises"]))
    # print(clusters[3])
    # print(clusters[4])
    return clusters


# def random_color():
#     rgbl = [255, 0, 0]
#     random.shuffle(rgbl)
#     return tuple(rgbl)


if __name__ == "__main__":
    eps = 2.7
    min_pts = 9
    # eps = 2.6
    # min_pts = 8

    clusters = dbscan("Dataset/clustering_test.txt", eps, min_pts)
    for key in clusters.keys():
        value = clusters[key]
        xs = []
        ys = []
        for cluster_p in value:
            xs.append(cluster_p[0])
            ys.append(cluster_p[1])
        # now_color = next(colors)

        plt.scatter(xs, ys, color=numpy.random.rand(3, 1))
        if key == "noises":
            plt.scatter(xs, ys, color='black')
        else:
            plt.scatter(xs, ys, color=numpy.random.rand(3, 1))
    plt.show()

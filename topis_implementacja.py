import numpy as np


norms = np.array([])


def normalize(points, weights):
    global norms

    weights = np.tile(weights, (len(points), 1))

    norms = np.linalg.norm(points, axis=0)
    norms = np.tile(norms, (len(points), 1))

    return np.divide(weights * points, norms)


# def denormalize(points, weights):
#     global norms
#     weights = np.tile(weights, (len(points), 1))
#     points = points / weights
#
#     return np.multiply(points, norms[points.shape[0], :])


def topsis(points, weights, ideal_point):
    # np.set_printoptions(precision=4)

    # # normalizacja
    # norm_points = normalize(points, weights)
    # # ======================================================================
    # # punkty zdominowane
    # non_dominated_points = norm_points
    # temp_dom = []
    #
    # for i, point1 in enumerate(norm_points[:-1]):
    #     temp_dom.append(point1)
    #     for point2 in non_dominated_points:
    #         # Usuwanie zdominowanych
    #         if np.all(point1 > point2):
    #             del_idx = np.all(np.equal(non_dominated_points, point1), axis=1)
    #             non_dominated_points = np.delete(non_dominated_points, del_idx, 0)
    #             break
    #     else:
    #         # Filtracja
    #         for point2 in norm_points[i:]:
    #             if np.all(point1 < point2):
    #                 del_idx = np.all(np.equal(non_dominated_points, point2), axis=1)
    #                 non_dominated_points = np.delete(non_dominated_points, del_idx, 0)
    #                 # print(f"{point1} deleted {point2}")
    #
    # non_dominated_points_not_normalized = np.copy(points)
    # for i, point1 in enumerate(points[:-1]):
    #     for point2 in non_dominated_points_not_normalized:
    #         # Usuwanie zdominowanych
    #         if np.all(point1 > point2):
    #             del_idx = np.all(np.equal(non_dominated_points_not_normalized, point1), axis=1)
    #             non_dominated_points_not_normalized = np.delete(non_dominated_points_not_normalized, del_idx, 0)
    #             break
    #     else:
    #         # Filtracja
    #         for point2 in points[i:]:
    #             if np.all(point1 < point2):
    #                 del_idx = np.all(np.equal(non_dominated_points_not_normalized, point2), axis=1)
    #                 non_dominated_points_not_normalized = np.delete(non_dominated_points_not_normalized, del_idx, 0)
    #                 # print(f"{point1} deleted {point2}")


    # ======================================================================
    # punkty zdominowane
    non_dominated_points = points
    temp_dom = []

    for i, point1 in enumerate(points[:-1]):
        temp_dom.append(point1)
        for point2 in non_dominated_points:
            # Usuwanie zdominowanych
            if np.all(point1 > point2):
                del_idx = np.all(np.equal(non_dominated_points, point1), axis=1)
                non_dominated_points = np.delete(non_dominated_points, del_idx, 0)
                break
        else:
            # Filtracja
            for point2 in points[i:]:
                if np.all(point1 < point2):
                    del_idx = np.all(np.equal(non_dominated_points, point2), axis=1)
                    non_dominated_points = np.delete(non_dominated_points, del_idx, 0)
                    # print(f"{point1} deleted {point2}")

    normal_points = non_dominated_points
    norm_points = normalize(points, weights)
    non_dominated_points = normalize(non_dominated_points, weights)

    # ======================================================================
    # punkt idealny, antyidealny i nadir

    # ideal_point = np.min(non_dominated_points, axis=0)
    nonideal_point = np.max(norm_points, axis=0)
    nadir = np.max(non_dominated_points, axis=0)

    # ======================================================================
    # Wyliczenie odległość od punktu idealnego i nadir

    ideal_point = np.tile(ideal_point, (len(non_dominated_points), 1))
    nadir = np.tile(nadir, (len(non_dominated_points), 1))

    d_ideal_lst = np.linalg.norm(non_dominated_points - ideal_point, axis=1)
    d_nadir_lst = np.linalg.norm(non_dominated_points - nadir, axis=1)

    assert (len(d_ideal_lst) == len(non_dominated_points))
    assert (len(d_nadir_lst) == len(non_dominated_points))

    # ======================================================================
    # Wyliczenie współczynnika skoringowego

    ci_lst = np.divide(d_nadir_lst, d_nadir_lst + d_ideal_lst)
    ci_idx_sort = np.argsort(ci_lst)

    ci_lst_sorted = np.take_along_axis(ci_lst, ci_idx_sort, axis=0)
    ci_lst_sorted = np.vstack(ci_lst_sorted)

    # idx_eq = np.all(norm_points == non_dominated_points, axis=1)
    # idx_eq = (norm_points[:, None] == non_dominated_points[None, :]).all(1).any(0)

    ci_idx_sort = np.tile(ci_idx_sort, (normal_points.shape[1], 1))

    non_dominated_points_sorted = np.take_along_axis(normal_points, ci_idx_sort.T, axis=0)
    # non_dominated_points_sorted = denormalize(non_dominated_points_sorted, weights)

    points_with_ci = np.append(non_dominated_points_sorted, ci_lst_sorted, axis=1)

    return points_with_ci

    # adres = 0
    # top = np.argmax(ci_lst, axis=0)
    # for i in range(len(temp_dom)):
    #     if np.all(temp_dom[i] == non_dominated_points[top]):
    #         adres = i
    #         return ci_lst[top], adres
    #
    # return ci_lst[top], adres

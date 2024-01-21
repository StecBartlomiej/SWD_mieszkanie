import matplotlib.pyplot as plt
import numpy as np


# wyznaczenie klas poprzez wyznaczanie niezdominowanych podzbiorów ze zbioru punktów
def undominated_points(X):
    n = X.shape[0]
    P = []
    X = X[X[:, 0].argsort()]  # Sortuj według pierwszej kolumny

    i = 0
    while i < X.shape[0]:
        Y = X[i, :]
        do_usuniecia = []

        for j in range(i + 1, X.shape[0]):
            if np.all(Y <= X[j, :]):
                do_usuniecia.append(j)
            elif np.all(X[j, :] <= Y):
                do_usuniecia.append(i)
                Y = X[j, :]

        X = np.delete(X, do_usuniecia, axis=0)

        if X.size == 0:
            break

        P.append(Y)
        i += 1

    return np.array(P)


def rectangles(Aquo, Adoc):
    n = Aquo.shape[0]
    P = []
    X = Aquo
    Y = Adoc
    for i in Adoc:
        w = []
        for j in Aquo:
            d = np.linalg.norm(i - j)
            w.append(d ** n / n)
        P.append(w)
    # print(P)
    return P


def rsm(point_list, Aquo, Adoc):
    point_list = undominated_points(point_list)

    Aquo = undominated_points(Aquo)
    Adoc = undominated_points(Adoc)

    # Aquo = np.tile(Aquo[0, :], (7, 1))
    # Adoc = np.tile(Adoc[0, :], (7, 1))
    # print(f"Aquo {Aquo}")
    # print(f"Adoc {Adoc}")

    X = point_list
    P = rectangles(Aquo, Adoc)
    # print(P)

    s = 0
    for i in range(len(P)):
        s += sum(P[i])

    # s = 0
    # for i in range(len(Aquo[0])):
    #     s = s + sum(P[i])

    suma = s
    P = np.array(P)
    # print(point_list)

    # print(f"Suma: {suma}")
    w = P / suma
    R = []
    for p in point_list:
        r = 0
        for x, i in enumerate(Adoc):
            for y, j in enumerate(Aquo):
                # print(f"i = \n{i}")
                # print(f"p = \n{p}")
                # print(f"j = \n{j}")
                # print(f"i < p = \n{i < p}")
                # print(f"p < j = \n{p < j}")
                if np.all((i <= p) & (p <= j)):
                    r = r + w[x][y] * (np.linalg.norm(p - j)) / (np.linalg.norm(p - i) + (np.linalg.norm(p - j)))
        # print(f"r: {r}")
        R.append([p, r])

    r = sorted(R, key=lambda x: x[1])
    # print(r)
    return r


def plot_points_with_colors(classes, point_list):
    for i, points in enumerate(classes):
        x, y = zip(*points)  # rozdzielenie punktów na współrzędne x i y
        color = f'C{i}'  # przypisanie koloru na podstawie indeksu z listy
        plt.scatter(x, y, color=color, label=f'A{i}')

    x, y = zip(*point_list)
    plt.scatter(x, y, color='gray', label='Punkty')

    plt.xlabel('Oś X')
    plt.ylabel('Oś Y')
    plt.title('RSM')
    plt.grid(axis='both')
    plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    pointsy = np.array(
        [[4, 4, -1], [5, 4, 0], [0, 1, 2], [2, 1, -2], [3, 3, 0], [3, -1, 2], [-1, 1, 4], [4, -2, 1], [-1, 3, 4]])
    Adoc = np.array([[-6, -5, -5], [-5, -6, -5], [-5, -5, -6]])
    Aquo = np.array([[5, 5, 6], [6, 5, 5], [5, 6, 5]])
    Ranking = rsm(pointsy, Aquo, Adoc)
    print(Ranking)

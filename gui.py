import tkinter as tk
from tkinter import ttk

import numpy as np
import pandas as pd
from pandastable import Table
from math import isclose
from rsm import rsm
from topis_implementacja import topsis
from uta import uta



is_weights_window_open = False
is_rsm_open = False


columns_name = [
    'Cena [zł]', 'Czynsz [zł]', 'Piętro', 'Metraż [m^2]',
    'Liczba pokoi', 'Umeblowane', 'Balkon'
]


def show_ranking(root, df: pd.DataFrame, title: str):
    w = 750
    h = 300

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    window = tk.Toplevel(root)
    window.wm_title(title)

    window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    frame = ttk.Frame(window)

    pt = Table(frame, dataframe=df, width=900, maxcellwidth=15000)
    pt.adjustColumnWidths(limit=15000)
    pt.show()

    frame.pack(fill='both', expand=True)


def show_weights(window, weights):
    global is_weights_window_open

    if is_weights_window_open:
        return
    is_weights_window_open = True

    subwindow = tk.Toplevel(window)
    subwindow.wm_title("Wagi")

    subwindow.rowconfigure(0, weight=1)
    subwindow.columnconfigure(0, weight=1)
    subwindow.resizable(False, False)

    num_lst = [tk.DoubleVar(subwindow, value=x) for _, x in enumerate(weights)]

    for idx, x in enumerate(num_lst):
        tk.Label(subwindow, text=f"{columns_name[idx]}").grid(row=idx, column=0, padx=5)
        tk.Entry(subwindow, textvariable=x).grid(row=idx, column=1, padx=4, sticky='news')

    def copy_weights():
        for idx, x in enumerate(num_lst):
            weights[idx] = x.get()

        if not isclose(sum(weights), 1):
            for i in range(7):
                weights[i] = 1/7
                num_lst[i]= tk.DoubleVar(subwindow, value=weights[i])

    def on_close():
        global is_weights_window_open
        is_weights_window_open = False

    def copy_close():
        copy_weights()
        on_close()
        subwindow.destroy()

    subwindow.protocol("WM_DELETE_WINDOW", on_close())

    button = tk.Button(subwindow, text="Ok", command=copy_close)
    max_row = len(num_lst)
    button.grid(row=max_row, column=1)


def open_ideal(root, ideal_point):
    global is_rsm_open

    if is_rsm_open:
        return
    is_rsm_open = True

    subwindow = tk.Toplevel(root)
    subwindow.wm_title("Punkt idealny")

    subwindow.rowconfigure(0, weight=1)
    subwindow.columnconfigure(0, weight=1)
    subwindow.resizable(False, False)

    num_lst = [tk.IntVar(subwindow, value=x) for _, x in enumerate(ideal_point[0])]

    labels_str = ["Cena", "Czynsz", "Piętro", "Metraż", "Liczba pokoi"]
    for idx in range(5):
        x = num_lst[idx]
        tk.Label(subwindow, text=labels_str[idx]).grid(row=idx, column=0, padx=5)
        tk.Entry(subwindow, textvariable=x).grid(row=idx, column=1, padx=4, sticky='news')

    tk.Label(subwindow, text="Umeblowane").grid(row=5, column=0, padx=5)
    tk.Checkbutton(subwindow, variable=num_lst[-2]).grid(row=5, column=1, padx=4, sticky='news')

    tk.Label(subwindow, text="Balkon").grid(row=6, column=0, padx=5)
    tk.Checkbutton(subwindow, variable=num_lst[-1]).grid(row=6, column=1, padx=4, sticky='news')

    def copy_weights():
        for i, x in enumerate(num_lst):
            ideal_point[0, i] = x.get()

    def on_close():
        global is_rsm_open
        is_rsm_open = False

    def copy_close():
        on_close()
        copy_weights()
        subwindow.destroy()

    subwindow.protocol("WM_DELETE_WINDOW", on_close())

    button = tk.Button(subwindow, text="Ok", command=copy_close)
    max_row = 7
    button.grid(row=max_row, column=1)


def run_uta(window, no_of_sections = None, usability_values = None):
    rank = uta("SWD_baza_danych.xlsx", no_of_sections, usability_values)

    names = columns_name.copy()
    names.append("Funkcja użyteczności")

    df = pd.DataFrame(rank, columns=names)
    show_ranking(window, df, "Ranking UTA")


def run_rsm(window, point_lst, Aquo, Adoc):
    array = get_rsm(point_lst, Aquo, Adoc)

    names = columns_name.copy()
    names.append("ci")

    df_rank = pd.DataFrame(array, columns=names)
    show_ranking(window, df_rank, "Ranking RSM")


def get_rsm(point_lst, Aquo, Adoc):
    copy_points = np.copy(point_lst)
    copy_Adoc = np.copy(Adoc)
    copy_Aquo = np.copy(Aquo)

    copy_points[:, range(3, 7)] = -copy_points[:, range(3, 7)]
    copy_Adoc[:, range(3, 7)] = -copy_Adoc[:, range(3, 7)]
    copy_Aquo[:, range(3, 7)] = -copy_Aquo[:, range(3, 7)]

    if Adoc[0][6] == 0:
        copy_points[:, 6] = -copy_points[:, 6]
        Adoc[:, 6] = -Adoc[:, 6]

    if Adoc[0][5] == 0:
        copy_points[:, 5] = -copy_points[:, 5]
        Adoc[:, 5] = -Adoc[:, 5]

    rank = rsm(copy_points, copy_Adoc, copy_Aquo)

    array = np.array([])
    array1 = np.array([])

    for i, x in enumerate(rank):
        array = np.append(array, x[0], axis=0)
        array1 = np.append(array1, [x[1]], axis=0)

    array = array.reshape((len(rank), 7))
    array[:, range(3, 7)] = -array[:, range(3, 7)]
    array = np.append(array, np.vstack(array1), axis=1)

    array[:, range(3, 7)] = array[:, range(3, 7)]

    if Adoc[0][6] == 0:
        array[:, 6] = -array[:, 6]

    if Adoc[0][5] == 0:
        array[:, 5] = -array[:, 5]

    array = array[::-1]
    return array


def run_topsis(window, points, weights, ideal_point):
    rank = get_topsis(points, weights, ideal_point)
    names = columns_name.copy()
    names.append("ci")

    df_rank = pd.DataFrame(rank, columns=names, dtype="float")
    show_ranking(window, df_rank, "Ranking topsis")


def get_topsis(points, weights, ideal_point):
    # Change max -> -1 * min
    copy_points = np.copy(points)
    copy_points[:, range(3, 7)] = -copy_points[:, range(3, 7)]

    ideal_point_copy = np.copy(ideal_point)
    ideal_point_copy[:, range(3, 7, 1)] = -ideal_point_copy[:, range(3, 7, 1)]

    if ideal_point[0][6] == 0:
        copy_points[:, 6] = -copy_points[:, 6]
        ideal_point_copy[:, 6] = -ideal_point_copy[:, 6]

    if ideal_point[0][5] == 0:
        copy_points[:, 5] = -copy_points[:, 5]
        ideal_point_copy[:, 5] = -ideal_point_copy[:, 5]

    rank = topsis(copy_points, weights, ideal_point_copy)
    rank[:, range(3, 7, 1)] = -rank[:, range(3, 7, 1)]

    if ideal_point[0][6] == 0:
        rank[:, 6] = -rank[:, 6]

    if ideal_point[0][5] == 0:
        rank[:, 5] = -rank[:, 5]

    rank = rank[::-1]
    return rank


def run_all(window, points, ideal_point, weights, Aquo, Adoc, no_of_sections, usability_values):
    topsis_rank = get_topsis(points, weights, ideal_point)
    rsm_rank = get_rsm(points, Aquo, Adoc)
    uta_rank = uta("SWD_baza_danych.xlsx", no_of_sections, usability_values)


def non_dominated(points):
    non_dominated_points = points

    for i, point1 in enumerate(points):
        for point2 in non_dominated_points:
            if np.all(point1 == point2):
                continue

            if np.all(point1 <= point2):
                # print(f"{point1} dominated by {point2}")
                del_idx = np.all(np.equal(non_dominated_points, point1), axis=1)
                non_dominated_points = np.delete(non_dominated_points, del_idx, 0)
                break
        else:
            # Filtracja
            for point2 in points[i:]:
                if np.all(point1 > point2):
                    del_idx = np.all(np.equal(non_dominated_points, point2), axis=1)
                    non_dominated_points = np.delete(non_dominated_points, del_idx, 0)
                    # print(f"{point1} deleted {point2}")
    return non_dominated_points

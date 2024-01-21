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
    'Cena [zł]', 'czynsz [zł]', 'piętro', 'metraż [m^2]',
    'Liczba pokoi', 'umeblowane', 'balkon'
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
        tk.Label(subwindow, text=f"Waga {idx}:").grid(row=idx, column=0, padx=5)
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
    rank = rsm(point_lst, Aquo, Adoc)
    # print(rank)

    names = columns_name.copy()
    names.append("ci")

    array = np.array([])
    array1 = np.array([])

    for i, x in enumerate(rank):
        array = np.append(array, x[0], axis=0)
        array1 = np.append(array1, [x[1]], axis=0)

    array = array.reshape((len(rank), 7))
    array = np.append(array, np.vstack(array1), axis=1)

    df_rank = pd.DataFrame(array, columns=names)
    show_ranking(window, df_rank, "Ranking RSM")


def run_topsis(window, points, weights, ideal_point):
    # Change max -> -1 * min
    copy_points = np.copy(points)
    copy_points[:, range(3, 7, 1)] = -copy_points[:, range(3, 7, 1)]

    rank = topsis(copy_points, weights, ideal_point)
    rank[:, range(3, 7, 1)] = -rank[:, range(3, 7, 1)]

    names = columns_name.copy()
    names.append("ci")

    df_rank = pd.DataFrame(rank, columns=names, dtype="float")
    show_ranking(window, df_rank, "Ranking topsis")


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

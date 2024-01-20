import tkinter as tk
from tkinter import ttk
import pandas as pd
from pandastable import Table
from functools import partial
from math import isclose


is_weights_window_open = False


def show_weights(window, weights):
    global is_weights_window_open

    if is_weights_window_open:
        return
    is_weights_window_open = True

    subwindow = tk.Toplevel(window)
    subwindow.wm_title("Wagi")

    subwindow.rowconfigure(0, weight=1)
    subwindow.columnconfigure(0, weight=1)

    frame = tk.ttk.Frame(subwindow)

    num_lst = [tk.DoubleVar() for _ in range(len(weights))]

    for idx, x in enumerate(num_lst):
        tk.Label(subwindow, text=f"Waga {idx}:").grid(row=idx, column=0, padx=5)
        tk.Entry(subwindow, textvariable=x).grid(row=idx, column=1, padx=4, sticky='news')

    def copy_weights():
        for idx, x in enumerate(num_lst):
            weights[idx] = x.get()

        if isclose(sum(weights), 1):
            pass  # TODO - co jak nie sumują się do 1

    def on_close():
        global is_weights_window_open
        is_weights_window_open = False

    def copy_close():
        copy_weights()
        on_close()
        subwindow.destroy()

    subwindow.protocol("WM_DELETE_WINDOW", on_close())

    button = tk.Button(subwindow, text="Ok", command=copy_close)
    button.grid(row=3, column=1)


if __name__ == '__main__':
    excel_data = pd.read_excel("SWD_baza_danych.xlsx", dtype='int32')

    # Window App
    window = tk.Tk()
    window.title("Wybór mieszkania")
    window.geometry("800x400")

    down_frame = ttk.Frame(window)
    button_frame = ttk.Frame(window)

    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=3)

    weights = [1 / 6 for _ in range(6)]
    open_weights = partial(show_weights, window, weights)

    button = tk.Button(button_frame, text="Metoda 1")
    button1 = tk.Button(button_frame, text="Metoda 2")
    button2 = tk.Button(button_frame, text="Metoda 3")
    button_weight = tk.Button(button_frame, text="Wagi", command=open_weights)

    # layout
    button.pack(side='left',  fill='x', pady=5, padx=10)
    button1.pack(side='left', fill='x', pady=5, padx=10)
    button2.pack(side='left', fill='x', pady=5, padx=10)
    button_weight.pack(side='left', fill='x', pady=5, padx=10)
    button_frame.pack(side='top')

    pt = Table(down_frame, dataframe=excel_data, width=900, maxcellwidth=15000)
    pt.adjustColumnWidths(limit=15000)
    pt.show()

    down_frame.pack(fill='both', expand=True)

    window.mainloop()

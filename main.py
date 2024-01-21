from gui import *
from functools import partial
import warnings

warnings.filterwarnings("ignore")

# TODO 3.1 - add subwindow for uta


if __name__ == '__main__':
    excel_data = pd.read_excel("SWD_baza_danych.xlsx", dtype='int32')
    ideal_point = np.array([[0, 0, 0, 100, 10, 1, 1]])
    # anty_ideal_point = np.array([[1e10, 1e10, 1e10, 0, 0, 0, 0]])
    anty_ideal_point = non_dominated(excel_data.to_numpy())

    # Window App
    window = tk.Tk()
    window.title("Wybór mieszkania")
    window.geometry("800x400")

    down_frame = ttk.Frame(window)
    button_frame = ttk.Frame(window)

    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=3)

    weights = [1 / 7 for _ in range(7)]
    open_weights = partial(show_weights, window, weights)

    przedzialy = [2, 2, 2, 2, 2, 2, 2]
    wartosci = [[5, 0, 0], [0, 0, 0], [0, 0, 0], [5, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Methods
    topsis = partial(run_topsis, window, excel_data.to_numpy(), weights, ideal_point)
    go_rsm = partial(run_rsm, window, excel_data.to_numpy(), ideal_point, anty_ideal_point)
    go_uta = partial(run_uta, window, przedzialy, wartosci)
    run_ideal = partial(open_ideal, window, ideal_point)
    # run_all = partial()

    # Buttons
    button = tk.Button(button_frame, text="Topsis", command=topsis)
    button1 = tk.Button(button_frame, text="RSM", command=go_rsm)
    button2 = tk.Button(button_frame, text="UTA", command=go_uta)
    # button_all = tk.Button(button_frame, text="Porównanie", command=go_uta)
    button_weight = tk.Button(button_frame, text="Wagi", command=open_weights)
    button_ideal = tk.Button(button_frame, text="Punkt idealny", command=run_ideal)

    # layout
    button.pack(side='left', fill='x', pady=5, padx=10)
    button1.pack(side='left', fill='x', pady=5, padx=10)
    button2.pack(side='left', fill='x', pady=5, padx=10)
    button_weight.pack(side='left', fill='x', pady=5, padx=10)
    button_ideal.pack(side='left', fill='x', pady=5, padx=10)
    button_frame.pack(side='top')

    pt = Table(down_frame, dataframe=excel_data, width=900, maxcellwidth=15000)
    pt.adjustColumnWidths(limit=15000)
    pt.show()

    down_frame.pack(fill='both', expand=True)

    window.mainloop()

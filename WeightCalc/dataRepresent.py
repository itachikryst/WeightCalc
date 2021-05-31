from matplotlib import style, animation
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from dataManip import *
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *


def print_last_day_info(_data):
    lastDay = get_last_day(_data)
    lastDayBetterPercent = get_day_worse_than_percent(lastDay, _data)
    output = "Najnowszy dzień to {}, ważyłeś w nim {}kg, dzień lepszy od {}% dni.".format(
        lastDay[0].strftime("%d/%m/%Y"),
        lastDay[1],
        round(lastDayBetterPercent * 100, 2))
    #print(output)
    return output


def print_best_day_info(_data):
    bestDay = get_best_day(_data)
    output = "Najlepszy dzień to {}, ważyłeś w nim {}kg.".format(
        bestDay[0].strftime("%d/%m/%Y"),
        bestDay[1])
    #print(output)
    return output


def generate_mpl_full_plot(window):
    ###
    style.use("dark_background")
    fig = Figure(figsize=(5, 5),
                 dpi=100)
    ###
    plot1 = fig.add_subplot(111)

    ###
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=5, columnspan=4, sticky="NSEW")
    ###
    toolbarFrame = Frame(master=window)
    toolbarFrame.grid(row=6, columnspan=4, sticky="NSEW")
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
    # toolbar.update()
    return fig, plot1


def start_tkinter(_data=get_data_from_ods_file()):
    def animate_plot(f):
        plot1.clear()
        days, weights, fatPercentages, musclePercentages = get_valid_values_from_data(
            get_data_from_ods_file())
        numDays = None
        if numDays is None:
            numDays = len(days)
        plot1.plot(days[-numDays:], weights[-numDays:], 'g', label='Weight',
                   linewidth=5)
        plot1.plot(days[-numDays:], fatPercentages[-numDays:], 'r', label='Fat',
                   linewidth=3)
        plot1.plot(days[-numDays:], musclePercentages[-numDays:], 'c',
                   label='Muscle',
                   linewidth=3)
        anim.event_source.stop()

    def on_click_add_db_entry():
        date = dateTextbox.get()
        weight = weightTextbox.get()
        fat = fatTextbox.get()
        muscle = muscleTextbox.get()
        try:
            anim.event_source.start()
            add_db_entry(date, weight, fat, muscle)
            __data = get_data_from_ods_file()
            lastDayLabel.config(
                text=print_last_day_info(__data))
            bestDayLabel.config(
                text=print_best_day_info(__data))
        except:
            print("Couldn't add new db entry")

    window = Tk()
    window.title("Weight Calculator App")
    window.configure(background="black")
    window.minsize(800, 600)
    window.columnconfigure((0, 1, 2, 3), weight=1)
    window.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=5)
    window.rowconfigure(0, weight=3)
    window.rowconfigure(1, weight=2)
    window.rowconfigure(2, weight=1)
    window.rowconfigure(3, weight=1)
    window.rowconfigure(4, weight=1)
    ###
    lastDayLabel = Label(window, text=print_last_day_info(_data), bg="black",
                         fg="white",
                         font="none 12 bold")
    lastDayLabel.grid(row=0, columnspan=4, sticky="NSEW")
    ###
    bestDayLabel = Label(window, text=print_best_day_info(_data), bg="black",
                         fg="white",
                         font="none 12 bold")
    bestDayLabel.grid(row=1, columnspan=4, sticky="NSEW")
    ###
    dateLabel = Label(window, text="Data", bg="black",
                      fg="white",
                      font="none 12 bold")
    dateLabel.grid(row=2, column=0, sticky="NSEW")
    ###
    weightLabel = Label(window, text="Waga", bg="black",
                        fg="white",
                        font="none 12 bold")
    weightLabel.grid(row=2, column=1, sticky="NSEW")
    ###
    fatLabel = Label(window, text="Tłuszcz", bg="black",
                     fg="white",
                     font="none 12 bold")
    fatLabel.grid(row=2, column=2, sticky="NSEW")
    ###
    muscleLabel = Label(window, text="Mięśnie", bg="black",
                        fg="white",
                        font="none 12 bold")
    muscleLabel.grid(row=2, column=3, sticky="NSEW")
    ###
    dateTextbox = Entry(window, width=8, bg="white")
    dateTextbox.grid(row=3, column=0, sticky="NSEW")
    ###
    weightTextbox = Entry(window, width=8, bg="white")
    weightTextbox.grid(row=3, column=1, sticky="NSEW")
    ###
    fatTextbox = Entry(window, width=8, bg="white")
    fatTextbox.grid(row=3, column=2, sticky="NSEW")
    ###
    muscleTextbox = Entry(window, width=8, bg="white")
    muscleTextbox.grid(row=3, column=3, sticky="NSEW")
    ###
    submitButton = Button(window, text="Dodaj wpis do bazy",
                          command=on_click_add_db_entry, bg="black", fg="white")
    submitButton.grid(row=4, columnspan=4, sticky="NSEW")
    ###
    fig, plot1 = generate_mpl_full_plot(window)
    anim = animation.FuncAnimation(fig, animate_plot, interval=100)

    ###
    window.mainloop()

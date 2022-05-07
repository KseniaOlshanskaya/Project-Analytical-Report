import matplotlib.pyplot as plt
import pandas as pd


class FigureMaker(object):

    @staticmethod
    def make_pie_chart(values, labels, description, export=True):
        plt.pie(values)
        plt.legend(labels, loc="best", bbox_to_anchor=(1, 1))
        plt.title(description)
        if export:
            plt.savefig("ExportRussiaPie.png")
        else:
            plt.savefig("ImportRussiaPie.png")
        plt.close()

    @staticmethod
    def make_double_bar_chart(values_previous, values_current, labels_previous, export=True):
        plotdata = pd.DataFrame({
            "2020": values_previous,
            "2021": values_current,
        },
            index=labels_previous
        )
        plotdata.plot(kind="bar", alpha=0.75, rot=30)
        plt.xlabel("Сектор")
        plt.ylabel("млн. долл. США")
        if export:
            plt.title("Динамика экспорта России в Казахстан по секторам")
            plt.savefig("ExportRussiaBar.png")
        else:
            plt.title("Динамика импорта России в Казахстан по секторам")
            plt.savefig("ImportRussiaBar.png")
        plt.close()

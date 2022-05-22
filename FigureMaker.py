import matplotlib.pyplot as plt
import pandas as pd


class FigureMaker(object):

    @staticmethod
    def make_pie_chart(values, labels, description, export=True):
        colors = ["#3E7DCC", "#8F9CB3", "#00C8C8", "#F9D84A", "#FF6055", "#4D525A"]
        if export:
            colors.append("#8CC0FF")
        plt.pie(values, wedgeprops = { 'linewidth' : 3, 'edgecolor' : 'white' }, colors=colors)
        centre_circle = plt.Circle((0, 0), 0.50, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.legend(labels, loc="best", bbox_to_anchor=(1, 1))
        plt.text(-0.7, -1.2, description, size=11)
        if export:
            plt.savefig("ExportRussiaPie.png", bbox_inches='tight')
        else:
            plt.savefig("ImportRussiaPie.png", bbox_inches='tight')
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

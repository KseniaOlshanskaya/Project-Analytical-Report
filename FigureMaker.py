import matplotlib.pyplot as plt

class FigureMaker(object):

    @staticmethod
    def makePieChart(values, labels, description, export=True):
        plt.pie(values)
        plt.legend(labels, loc="best", bbox_to_anchor=(1, 1))
        plt.title(description)
        if export:
            plt.savefig("ExportRussia.png")
        else:
            plt.savefig("ImportRussia.png")
        plt.close()

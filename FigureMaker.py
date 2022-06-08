import matplotlib.pyplot as plt


COLORS = ["#3E7DCC", "#8F9CB3", "#00C8C8", "#F9D84A", "#FF6055", "#4D525A", "#8CC0FF", "#DEB887",
          "#800080", "c0c0c0"]


class FigureMaker(object):

    @staticmethod
    def make_pie_chart(values, labels, description, file_name):
        count_parts = len(labels)
        colors = COLORS[:count_parts]
        plt.pie(values, wedgeprops={'linewidth':3, 'edgecolor':'white'}, colors=colors)
        centre_circle = plt.Circle((0, 0), 0.50, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.legend(labels, loc="best", bbox_to_anchor=(1, 1))
        plt.text(-0.7, -1.2, description, size=11)
        plt.savefig(file_name, bbox_inches='tight')


    @staticmethod
    def make_double_bar_chart(df_plot, description, file_name):
        plt.rcParams.update({'font.size': 8})
        df_plot.plot(kind="bar", rot=22, color=["#8F9CB3", "#8CC0FF"])
        plt.xlabel("Сектор")
        plt.ylabel("млн. долл. США")
        plt.title(description, x=0.5, y=1.05)
        plt.savefig(file_name)
        plt.close()

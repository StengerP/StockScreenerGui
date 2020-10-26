from classes.stock import Stock
import matplotlib.pyplot as plt
import plotly.graph_objects as go

class Screener:

    #def __init__(self, company:Stock):
    #    pass

    @classmethod
    def plot_revenue(cls, company:Stock):
        """
        Plots a bar chart of the given input[type]

        Parameters
        ----------
        var : Name of the variable to be plotted (str)
            e.g. 'price', 'PE ratio', 'Book Value per Share'

        Returns
        -------
        None
        """

        #TODO Check company for type Stock
        # ...

        attribute = "revenue"
        # accept single or list input
        if not isinstance(company, list):
            company = [company]

        for aCompany in company:
            data_x, data_y = [], []
            for k in aCompany.data["income_statement"].keys():
                if 'Annual' in aCompany.data["income_statement"][k]:
                    data_x.append(k)
                    data_y.append(aCompany.data["income_statement"][k]['Annual'][attribute])
            #growth = (data_y[1] - data_y[0])/data_y[1]
            fig = go.Figure(data=[go.Bar(x=data_x, y=data_y)]) #hovertext=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19'])])
            # Customize aspect
            fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                              marker_line_width=1.5, opacity=0.6)
            fig.update_layout(title_text='Historical '+attribute, yaxis=dict(title="Revenue in Billion USD"), xaxis=dict(title="year"))
            fig.show()

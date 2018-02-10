class IRKISUtils:
    NAME = "IRKIS"

    def __init__(self):
        pass

    # @classmethod
    # def map_value(cls, value):
    #     new_value = cls.NO_DATA if value == cls.NO_DATA else round(float(value)*1000, 0)
    #     return new_value

    @classmethod
    def plot(cls, filename, df):
        sensor_labels = ['A', 'B']
        for label in sensor_labels:
            label_columns = [col for col in df.columns if label in col]
            df_label = df[label_columns]  # remove columns from the other label
            title = 'Sensors with label ' + label + ' in ' + filename
            ax = df_label.plot(title=title, ylim=[0, 600])
            fig = ax.get_figure()
            fig.savefig(filename + '_' + label + '.png')

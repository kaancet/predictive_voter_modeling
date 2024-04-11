from bokeh.models import ColumnDataSource
import polars as pl


class DashBoard:
    def __init__(self):

        self.data = None
        self.cds = None

        self.widgets = {}
        self.graphs = {}
        self.callbacks = {}

    def set_data(self, _df: pl.DataFrame) -> None:
        self.data = _df.clone()

    def update(self, x: str, y: str) -> None:
        if x == y:
            temp_df = self.data.with_columns(pl.col(x).alias(f"temp_col"))
            y = "temp_col"
        else:
            temp_df = self.data.clone()

        df = temp_df.select([x, y]).drop_nulls()

        print(df)
        data = {
            "x": df[x].to_list(),
            "y": df[y].to_list(),
        }
        if self.cds is None:
            self.cds = ColumnDataSource(data)
        else:
            self.cds.data = data

    def add_graph(self, graph_name: str, graph2add) -> None:
        self.graphs[graph_name] = graph2add

    def add_widget(self, widget_name: str, widget2add) -> None:
        self.widgets[widget_name] = widget2add

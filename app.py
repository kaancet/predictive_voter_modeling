import polars as pl
from datetime import date, datetime
from time import localtime
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row, column, layout
from bokeh.models import Select, DateRangeSlider

from dashboard import DashBoard
from data_clean_utils import *

# Instantiate and initialize the DashBoard
dash = DashBoard()
df = pl.read_csv("contacts.csv")

# clean all nulls
df_dropped = drop_columns_that_are_all_null(df, verbose=False)

# convert string date to dates
df_date = convert_dates(df_dropped, verbose=False)
date_columns = [c for c in df_date.columns if "Date" in c]
df_date = df_date.select(date_columns)
df_show = df_date.clone()

dash.set_data(df_show)
selected_x = date_columns[0]
selected_y = date_columns[1]
dash.update(x=selected_x, y=selected_y)

###################
# CONTROL WIDGETS #
###################
# dash.add_widget(
#     "date_range",
#     DateRangeSlider(
#         value=(date(2023, 1, 1), date(2023, 12, 31)),
#         start=date(2015, 1, 1),
#         end=date(2024, 12, 31),
#     ),
# )

dash.add_widget(
    "select_y",
    Select(title="Select Y axis", options=date_columns, value=selected_y),
)
dash.add_widget(
    "select_x",
    Select(title="Select X axis", options=date_columns, value=selected_x),
)

#########
# PLOTS #
#########
f1 = figure(
    title="",
    width=600,
    height=400,
    x_axis_type="datetime",
    y_axis_type="datetime",
    x_axis_label="x",
    y_axis_label="y",
)
f1.circle(x="x", y="y", source=dash.cds)


#############################
# CALLBACKS AND OTHER FUNCS #
#############################
# def date_range_slider_callback(attr, new, old) -> None:
#     val = dash.widgets["date_range"].value
#     dt1 = datetime.fromtimestamp(val[0] / 1000)
#     dt2 = datetime.fromtimestamp(val[1] / 1000)
#     dat = df_show.filter((pl.col(selected_x) >= dt1) & (pl.col(selected_x) <= dt2))
#     dash.set_data(dat)
#     dash.update(x=selected_x, y=selected_y)


def yaxis_select_callback(attr, new, old) -> None:
    selected_y = dash.widgets["select_y"].value
    selected_x = dash.widgets["select_x"].value
    print(selected_x, selected_y)
    dash.update(x=selected_x, y=selected_y)


def xaxis_select_callback(attr, new, old) -> None:
    selected_y = dash.widgets["select_y"].value
    selected_x = dash.widgets["select_x"].value
    print(selected_x, selected_y)
    print("ijwbdibwdwd\n")
    dash.update(x=selected_x, y=selected_y)


# dash.widgets["date_range"].on_change("value_throttled", date_range_slider_callback)
dash.widgets["select_y"].on_change("value", yaxis_select_callback)
dash.widgets["select_x"].on_change("value", xaxis_select_callback)

#############################
# LAYOUT #
#############################
plots = row(f1)
layout = column(
    dash.widgets["select_x"],
    dash.widgets["select_y"],
    # dash.widgets["date_range"],
    plots,
)

curdoc().add_root(layout)
curdoc().title = "Dashboard"

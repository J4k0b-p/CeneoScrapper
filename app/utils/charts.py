from utils import product_parser
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.models import ColumnDataSource
import pandas as pd
from math import pi

def apply_dark_minimal_theme(p):
    p.background_fill_color = '#222529'
    p.border_fill_color = '#15191C'
    p.outline_line_color = '#E0E0E0'
    p.axis.major_label_text_color = 'white'
    p.axis.axis_label_text_color = 'white'
    p.axis.major_tick_line_color = 'white'
    p.axis.minor_tick_line_color = 'white'
    p.axis.axis_line_color = 'white'
    p.title.text_color = 'white'
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    return p

def create_bar_chart(product_id):
    reviews = product_parser.get_reviews_rate_data(product_id)
    values = reviews.values()
    rates = ['0.5','1.0', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5'] 
    data = list(values)
    p = figure( 
        x_range=rates, 
        height=350, 
        title="Rates amount per rate", 
    ) 

    p.vbar(x=rates, top=data, width=0.5) 
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    
    p = apply_dark_minimal_theme(p)

    return p

def create_doughnut_chart(product_id):
    data = product_parser.get_recomendation_data(product_id)

    data = pd.Series(data).reset_index(name='value').rename(columns={'index': 'options'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    data['color'] = [Category20c[20][i] for i in range(len(data))]
    data['legend_label'] = data['options'] + ': ' + data['value'].astype(str)
    p = figure(height=350, title="Recommendations amount in all opinions", toolbar_location="right",
           tools="hover", tooltips="@options: @value", x_range=(-0.5, 1.0))
    p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='legend_label', source=data)
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    p = apply_dark_minimal_theme(p)
    return p
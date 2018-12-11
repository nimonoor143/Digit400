Hello! 

This is my Digit 400 project.

Contains:

Pygal Library:

import pygal
import json

line_chart = pygal.Bar()
line_chart.title = 'Number of Time Yemen Been Air-raid in March 2015'
line_chart.x_labels = map(str, range(3/26/2015, 3/31/2015))
line_chart.add('Early-Morning', ([2,2,2,3,3,4,4,4,3, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
line_chart.add('Afternoon',  ([None,16,16 None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
line_chart.add('Evening',      ([21,21,21,2121,21,21,21,None,None,None,20, 20, 20, ])
line_chart.render_to_file("/var/www/FlaskApp/FlaskApp/static/graphs/graph.svg")
               
               
pie_chart = pygal.Pie()
pie_chart.title = 'Number of Air-raid in March 2018'
pie_chart.add('Sanaa', 12)
pie_chart.add('Saada',111 )
pie_chart.add('Hajja', 84)
pie_chart.add('Hudaydah', 52)
pie_chart.add('Lahj', 14)
pie_chart.render_to_file("/var/www/FlaskApp/FlaskApp/static/graphs/graph2.svg")






#!/usr/bin/python
import csv

with open('log.csv', 'rb') as csvfile:
    read = csv.reader(csvfile)
    for row in read:
         print(row)
         currentTemp = row[5]
         print(currentTemp) 
root@dagobah:/opt/highTunnel# cat line.py 
#!/usr/bin/python
import pygal                                                       # First import pygal

line_chart = pygal.Line(fill=True,legend_at_bottom=True)
line_chart.x_labels = map(str, range(1, 12))
line_chart.add('Tempurature', [61.3, 64.8, 61.3, 61.3, 66.2, 66.6, 69.6, 64.0, 63.0, 66.1, 67.0])
line_chart.add('Humidity',  [45.8, 52, 54, 49, 51, 52, 57, 55, 53, 54, 52])
line_chart.range = [30, 100]
line_chart.render_to_file('/var/www/html/chart.svg') 

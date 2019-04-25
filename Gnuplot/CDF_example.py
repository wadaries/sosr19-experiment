from numpy import *
import Gnuplot, Gnuplot.funcutils

g = Gnuplot.Gnuplot(debug=1)
g.title('CDF plot test') # (optional)
x = range(1, 1001)
x = [float(a)/1000 for a in x]
y1 = random.normal(0, 1, 1000)
y1.sort()
y2 = random.normal(10, 5, 1000)
y2.sort()
y3 = random.normal(20, 10, 1000)
y3.sort()
d1 = Gnuplot.Data(y1, x, title='mean: 0, deviation: 1', with_='lines')
d2 = Gnuplot.Data(y2, x, title='mean: 10, deviation: 5', with_='lines')
d3 = Gnuplot.Data(y3, x, title='mean: 20, deviation: 10', with_='lines')
g.xlabel('distribution')
g.ylabel('percentage')
g.plot(d1, d2, d3)
raw_input('Please press return to exit.\n')
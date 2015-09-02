
import numpy as np

from plotly import plotly
import plotly.graph_objs as plotlyGraph
from refined_stats.ValueUncertainty import ValueUncertainty

from refined_stats.density import DensityDistribution

#-------------------------------------------------------------------------------
# SINGLE POINT TEST

tests = [
    {   'title':'Single Point Test',
        'points':[
            ValueUncertainty() ] },
    {   'title':'Double Point Test',
        'points':[
            ValueUncertainty(),
            ValueUncertainty()] },
    {   'title':'Separate Double Point Test',
        'points':[
            ValueUncertainty(-3.0, 2.0),
            ValueUncertainty(2.0, 0.5) ] },
    {   'title':'Random Points Test',
        'points':[
            ValueUncertainty.createRandom(-10, -2, maxUnc=10.0),
            ValueUncertainty.createRandom(-7, 0, maxUnc=10.0),
            ValueUncertainty.createRandom(-2, 5, maxUnc=2.0),
            ValueUncertainty.createRandom(3, 8, maxUnc=1.0) ] }]

for i in range(len(tests)):
    test = tests[i]

    dd = DensityDistribution(values=test['points'])
    values = np.array(dd.getDistributionPoints())

    print(
        'DATA: %s' % test['title'],
        '\n * POINT COUNT:', len(values),
        '\n * MEAN:', values.mean(),
        '\n * STD:', values.std(),
        '\n * MEDIAN:', np.median(values))

    trace = plotlyGraph.Histogram(x=values)
    data = plotlyGraph.Data([trace])
    layout = plotlyGraph.Layout(
            showlegend=False,
            title=test['title'])

    url = plotly.plot(
        filename='RefStats/test-population-%s' % i,
        figure_or_data=plotlyGraph.Figure(data=data, layout=layout),
        auto_open=False)
    print('PLOT[%s]:' % i, url)


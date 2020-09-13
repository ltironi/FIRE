#%%

import pandas as pd
data = {'Date':[2012,2013,2014,2015,2016,2017,2018,2019,2020], 'Balance':[50000,73000,10000,168000,250000,303000,419000,580000,880000]}
data = pd.DataFrame(data=data)
data.dropna(inplace=True)

import chart_studio.plotly as ply
import cufflinks as cf

data.iplot(title="Energy Production Jan 1985--Jan 2018")


from chart_studio.plotly import plot_mpl
from statsmodels.tsa.seasonal import seasonal_decompose
result = seasonal_decompose(data, model='multiplicative')
fig = result.plot()
plot_mpl(fig)

from pyramid.arima import auto_arima
stepwise_model = auto_arima(data, start_p=1, start_q=1,
                           max_p=3, max_q=3, m=12,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
print(stepwise_model.aic())
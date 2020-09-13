#%%

# Importing required libraries 
import numpy as np 
import pandas as pd 
#import matplotlib.pylot as plt 
import matplotlib as plt 
from statsmodels.tsa.seasonal import seasonal_decompose
from pmdarima import auto_arima
import warnings 
from statsmodels.tsa.statespace.sarimax import SARIMAX


def proj():  
    #series = read_csv('shampoo-sales.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
    data = {'Balance':[73759,65481,57204,59083.26,60806.19,62529.12,64252.04,65974.97,67697.90,69420.83,71143.76,72866.68,74589.61,76312.54,77879,83628.52,89378.21,95127.90,100877.59,106627,162376,161158,161637,159720,161820,159664,155288,157594,168355,183888,180391,195904,218787,229107,238964,234364,234364,254000,254733,251013,250247,248940,248198,247639,245056,252553,252553,258273,258050,258050,280257,292264,303316,313540,331152,342062,351021,358763,364825,372807,379632,389456,406364,413692,418928,427473,458962,470843,483095,489348,496143,524020,530082,539085,554339,566468,580270,594674,641453,684478,744235,752682,761175,792287,831410,851105]}
    series = pd.DataFrame(data=data)
    series.dropna(inplace=True) 
    
    # ETS Decomposition 
    result = seasonal_decompose(series['Balance'],period=12) 
    
    # ETS plot  
    result.plot()
    
    #%%
     
    # Ignore harmless warnings 

    warnings.filterwarnings("ignore") 
    
    # # Fit auto_arima function to AirPassengers dataset 
    # stepwise_fit = auto_arima(series['Balance'], start_p = 1, start_q = 1, 
    #                         max_p = 3, max_q = 3, m = 12, 
    #                         start_P = 0, seasonal = True, 
    #                         d = None, D = 1, trace = True, 
    #                         error_action ='ignore',   # we don't want to know if an order does not work 
    #                         suppress_warnings = True,  # we don't want convergence warnings 
    #                         stepwise = True)           # set to stepwise 
    
    # # To print the summary 
    # stepwise_fit.summary() 

    #%%
    #Split data into train / test sets 
    train = series.iloc[:len(series)-12]
    test = series.iloc[len(series)-12:]  
    
    # Fit a SARIMAX(1, 1, 1)x(1, 1, 1, 12) on the training set 
    model = SARIMAX(train['Balance'],  
                    order = (1, 1, 1),  
                    seasonal_order =(1, 1, 1, 12)) 
    
    result = model.fit() 
    result.summary() 

    #%%
    #Predictions
    start = len(train) 
    end = len(train) + len(test) - 1
    
    # Predictions for one-year against the test set 
    predictions = result.predict(start, end, 
                                typ = 'levels').rename("Predictions") 
    
    # plot predictions and actual values 
    predictions.plot(legend = True) 
    test['Balance'].plot(legend = True) 

    #%%
    # Train the model on the full dataset 
     
    model = model = SARIMAX(series['Balance'],  
                    order = (1, 1, 1),  
                    seasonal_order =(1, 1, 1, 12)) 
    result = model.fit() 
    
    # Forecast for the next 5 years 
    forecast = result.predict(start = len(series),  
                            end = (len(series)) + 5*12,  
                            typ = 'levels').rename('Forecast') 
    
    # Plot the forecast values 
    series['Balance'].plot(figsize = (12, 5), legend = True) 
    forecast.plot(legend = True) 

    print('###predictions###')
    print(forecast)


    return series['Balance'], forecast

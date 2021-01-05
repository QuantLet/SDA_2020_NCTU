import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import sqrt
from keras.regularizers import l2
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr

def define_model0(hyparam,train_X):
    model = Sequential()
    model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2]),
                   kernel_regularizer=l2(hyparam),recurrent_regularizer=l2(hyparam),
                   bias_regularizer=l2(hyparam)))
    model.add(Dense(1))
    model.compile(loss='mae', optimizer='adam')
    return model

DF = pd.read_csv('C:/Users/user/Downloads/fe_covid_cur3.csv') #You can change the data on this part to get the result of the other models
#colnames=["MYR-1","MYR-2","MYR-3","USD-1","USD-2","USD-3","EUR-1","EUR-2","EUR-3","EURO"]
#DF.columns=colnames
print(DF.tail())
arr_curr3 = np.array(DF)
scaler = MinMaxScaler(feature_range=(0, 1))
dset = scaler.fit_transform(arr_curr3)
dataset = dset

# split into train and test sets
nrow,ncol = dataset.shape
train_size = np.int(nrow * 0.8)
test_size = nrow - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
print(train.shape, test.shape)

trainX, trainY = train[:,:-1],train[:,-1] 
testX, testY = test[:,:-1],test[:,-1]

# reshape input to be 3D [samples, timesteps, features]

train_X = trainX.reshape((trainX.shape[0],trainX.shape[1],1))
test_X = testX.reshape((testX.shape[0], testX.shape[1],1))
print(train_X.shape, trainY.shape, test_X.shape, testY.shape)

hyperpar=0.01 #You can modify this value of hyperparameter lambda
iter = 500
model = define_model0(hyperpar,train_X)
history = model.fit(train_X, trainY, epochs=iter,
                    validation_data=(test_X, testY), verbose=2, shuffle=False)

# plot history
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()
plt.show()

# make a prediction
yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0],test_X.shape[1]))

# invert scaling for forecast
X_yhat = np.concatenate((test_X,yhat), axis=1)
Xy_back = scaler.inverse_transform(X_yhat)
yhat_back = Xy_back[:,-1].astype(int)
yh = yhat_back

# invert scaling for actual
testY = testY.reshape((len(testY),1))
X_y = np.concatenate((test_X, testY), axis=1)
XY_test = scaler.inverse_transform(X_y)
y_test = XY_test[:,-1]
ya = y_test.astype(int)

ts_pairs = np.vstack((ya,yh))
print(ts_pairs)
# calculate RMSE
rmse = sqrt(mean_squared_error(y_test, yhat_back))
print('Test RMSE: %.3f' % rmse)

DF_out = pd.DataFrame(ts_pairs.T,columns=["Actual", "Predicted"])
print(DF_out.tail())
plt.plot(DF_out['Actual'], label='EURO Low')
plt.plot(DF_out['Predicted'], label='Predicted EURO Low')
plt.legend()
plt.show()

def model_performance(A,F):
    n = len(A)
    tot = 0
    for i in range (n):
        tot += abs((A[i]-F[i])/A[i])
    mp = np.round(tot/n,3)*100
    corr, _ = pearsonr(A,F)
    r2 = np.square(corr)
    return mp,r2

mape,R2 = model_performance(y_test, yhat_back)
rmse = sqrt(mean_squared_error(y_test, yhat_back))
print('Test RMSE: %.3f' % rmse)
print('Test MAPE: %.3f' % mape)
print('Test R_squared: %.3f' % R2)
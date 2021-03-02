import pandas as pd 

def prepare_data_Y_for_ML(df, weekly_or_monthly):
    output = df['Adj Close']
    output.rename('Stock Price')
    advance = df['Adj Close'].shift(10)
    advance = advance.rename('Short Term Advance')
    advance2 = df['Adj Close'].shift(40)
    advance2 = advance2.rename('Mid Term Advance')
    gt = pd.concat([output, advance, advance2], axis=1)
    gt['Short Term Change'] = ((gt['Short Term Advance'] - gt['Adj Close'])/gt['Adj Close'])*100
    gt['Mid Term Change'] = ((gt['Mid Term Advance'] - gt['Adj Close'])/gt['Adj Close'])*100
    #print(gt[9:110])
    #gt['Short Term Change'].plot()

    if weekly_or_monthly == 'weekly':
        Y = gt['Short Term Change'][10:]
    elif weekly_or_monthly == 'monthly':
        Y = gt['Mid Term Change'][40:]
    else:
        assert 0
    
    Y=Y.rename("Ground Truth")
    return Y

def prepare_data_X_for_ML(df, weekly_or_monthly):
    df['Weekly Sentiment'] = df['Avg Sentiment'].rolling(5, win_type='triang').sum()
    df['Monthly Sentiment'] = df['Avg Sentiment'].rolling(20, win_type='triang').sum()
    avg_monthly_sentiment = df['Monthly Sentiment'].sum()/len(df['Monthly Sentiment'])
    avg_week = df['Weekly Sentiment'].sum()/len(df['Monthly Sentiment'])
    if weekly_or_monthly == 'weekly':
        X = df[10:]
    elif weekly_or_monthly == 'monthly':
        X = df[40:]
    else:
        assert 0
    ## Ish: Below two lines commented because it was not needed but giving warning: 
    ## ERR:A value is trying to be set on a copy of a slice from a DataFrame.Try using .loc[row_indexer,col_indexer] = value instead
    X['Monthly Sentiment'] = X['Monthly Sentiment'].fillna(avg_monthly_sentiment)
    X['Weekly Sentiment'] = X['Weekly Sentiment'].fillna(avg_week)
    return X

def apply_MLP(X_train,X_test,y_train,y_test):
    sc_X = StandardScaler()
    X_trainscaled=sc_X.fit_transform(X_train)
    X_testscaled=sc_X.transform(X_test)
    reg = MLPRegressor(hidden_layer_sizes=(5,15,5),activation="relu" ,random_state=1, max_iter=2000).fit(X_trainscaled, y_train)
    y_pred=reg.predict(X_testscaled)
    #print("The Score with ", (r2_score(y_test, y_pred)))
    y_pred = pd.DataFrame(y_pred)
    out = pd.concat([y_test.reset_index(drop=True),y_pred.reset_index(drop=True)], axis=1)
    out = out.rename(columns={0:"Prediction"})
    #print("The Score with out ", (r2_score(out['Ground Truth'], out['Prediction'])))
    return out


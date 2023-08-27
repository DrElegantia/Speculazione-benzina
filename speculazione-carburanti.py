import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import seaborn as sns
import numpy as np
prezzi= pd.read_csv('https://dgsaie.mise.gov.it/open_data_export.php?export-id=2&export-type=csv', sep=',',on_bad_lines='warn', header=0)
prezzi['Date']=pd.to_datetime(prezzi['DATA_RILEVAZIONE'])
prezzi.index=pd.to_datetime(prezzi['Date'])
del prezzi['GASOLIO_AUTO']
del prezzi['GPL']
del prezzi['GASOLIO_RISCALDAMENTO']
del prezzi['O.C._FLUIDO_BTZ']
del prezzi['O.C._DENSO_BTZ']	
#importiamo i vari dati da yfinance

#importiamo i vari dati da yfinance

wti_ticker = yf.Ticker("WTI")
wti_df = wti_ticker.history(period="max")
wti_df['Mediana_7_WTI'] = wti_df['Close'].rolling(window=7).median()
brent_ticker = yf.Ticker("BZ=F")
brent_df = brent_ticker.history(period="max")
brent_df['Mediana_7_brent'] = brent_df['Close'].rolling(window=7).median()
eurusd_ticker = yf.Ticker("EURUSD=x")
eurusd_df = eurusd_ticker.history(period="max")
eurusd_df['Mediana_7_eurdol'] = eurusd_df['Close'].rolling(window=7).median()

#convertiamo gli indici in formato data=formato data mise

eurusd_df.index=pd.to_datetime(eurusd_df.index).date
brent_df.index=pd.to_datetime(brent_df.index).date
wti_df.index=pd.to_datetime(wti_df.index).date

#
del eurusd_df['Open']
del eurusd_df['High']
del eurusd_df['Low']
del eurusd_df['Volume']
del eurusd_df['Dividends']
del eurusd_df['Stock Splits']
brent_eur= pd.merge(eurusd_df, brent_df, left_index=True, right_index=True)
brent_eur_ben= pd.merge(brent_eur, prezzi, left_index=True, right_index=True)
df_brent_eur_ben=brent_eur_ben[['Mediana_7_eurdol', 'Mediana_7_brent', 'BENZINA']]
df=df_brent_eur_ben.rename(columns={'Mediana_7_eurdol':'EurDol', 'Mediana_7_brent':'brent'})

df['brent_eur']=df['brent']/df['EurDol']
df['ben1000']=df['BENZINA']/1000
df['rap_BEN_brent']=df['ben1000']/(df['brent_eur']/158.99)

finestra=5

df['rap_BEN_brent_mean'] = df['rap_BEN_brent'].rolling(window=finestra).mean()
df['rap_BEN_brent_std'] = df['rap_BEN_brent'].rolling(window=finestra).std()

df['rap_BEN_brent_1']= df['rap_BEN_brent_mean'] + df['rap_BEN_brent_std'] 
df['rap_BEN_brent_2']= df['rap_BEN_brent_mean'] - df['rap_BEN_brent_std'] 
df['rap_BEN_brent_3']= df['rap_BEN_brent_mean'] + 2*df['rap_BEN_brent_std'] 
df['rap_BEN_brent_4']= df['rap_BEN_brent_mean'] - 2*df['rap_BEN_brent_std'] 
df['rap_BEN_brent_5']= df['rap_BEN_brent_mean'] + 3*df['rap_BEN_brent_std'] 
df['rap_BEN_brent_6']= df['rap_BEN_brent_mean'] - 3*df['rap_BEN_brent_std'] 


plt.figure(figsize=(16,10))

plt.plot(df.index, df['rap_BEN_brent'], color='blue', linewidth=4, label='Rapporto in € fra Benzina senza accise e brent')
plt.plot(df.index, df['rap_BEN_brent_mean'], label=f'Media mobile a {finestra} settimane', linestyle='--', color='red', linewidth=4)
plt.fill_between(df.index,df['rap_BEN_brent_1'], df['rap_BEN_brent_2'], alpha=0.2, label='+1 sigma')
plt.fill_between(df.index,df['rap_BEN_brent_3'], df['rap_BEN_brent_4'], alpha=0.2, label='+2 sigma')
plt.fill_between(df.index,df['rap_BEN_brent_5'], df['rap_BEN_brent_6'], alpha=0.2, label='+3 sigma')
plt.legend()
plt.grid(visible=True, linewidth=0.5)
plt.show()


#Qui printo un altro grafico per avere anche una anlisi sul prezzo della benzina italiana

# Calcola i rendimenti logaritmici
df['log_returns'] = np.log(df['ben1000'] / df['ben1000'].shift(1))

# Rimuovi la prima riga (NaN)
df = df.dropna()

# Calcola la media mobile e la deviazione standard mobile dei rendimenti logaritmici
mean_log_returns = df['log_returns'].mean()
std_log_returns = df['log_returns'].std()

# Rappresenta i rendimenti logaritmici
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['log_returns'], label='Rendimenti Logaritmici', color='blue', linewidth=1)

plt.axhline(mean_log_returns + std_log_returns, color='green', linestyle='dashed', label='Sigma 1')
plt.axhline(mean_log_returns - std_log_returns, color='green', linestyle='dashed')
plt.axhline(mean_log_returns + 2 * std_log_returns, color='orange', linestyle='dashed', label='Sigma 2')
plt.axhline(mean_log_returns - 2 * std_log_returns, color='orange', linestyle='dashed')
plt.axhline(mean_log_returns + 3 * std_log_returns, color='purple', linestyle='dashed', label='Sigma 3')
plt.axhline(mean_log_returns - 3 * std_log_returns, color='purple', linestyle='dashed')
plt.title('Rendimenti Logaritmici del prezzo nazionale settimanale benzina')
plt.xlabel('Data')
plt.ylabel('Rendimenti Logaritmici')
plt.grid(True)
plt.legend()
plt.show()


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Calcola i rendimenti logaritmici
df['log_returns'] = np.log(df['ben1000'] / df['ben1000'].shift(1))

# Rimuovi la prima riga (NaN)
df = df.dropna()

# Calcola la media mobile e la deviazione standard mobile dei rendimenti logaritmici
mean_log_returns_rolling = df['log_returns'].rolling(window=finestra).mean()
std_log_returns_rolling = df['log_returns'].rolling(window=finestra).std()

# Aggiungi le colonne corrette al DataFrame originale usando .loc
df.loc[:, 'ben_1'] = mean_log_returns_rolling + std_log_returns_rolling
df.loc[:, 'ben_2'] = mean_log_returns_rolling - std_log_returns_rolling
df.loc[:, 'ben_3'] = mean_log_returns_rolling + 2 * std_log_returns_rolling
df.loc[:, 'ben_4'] = mean_log_returns_rolling - 2 * std_log_returns_rolling
df.loc[:, 'ben_5'] = mean_log_returns_rolling + 3 * std_log_returns_rolling
df.loc[:, 'ben_6'] = mean_log_returns_rolling - 3 * std_log_returns_rolling

# Rappresenta i rendimenti logaritmici
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['log_returns'], label='Rendimenti Logaritmici', color='blue', linewidth=1)
plt.plot(df.index, mean_log_returns_rolling, label=f'Media mobile a {finestra} settimane', linestyle='--', color='red', linewidth=1)
plt.fill_between(df.index, df['ben_1'], df['ben_2'], alpha=0.2, label='+1 sigma')
plt.fill_between(df.index, df['ben_3'], df['ben_4'], alpha=0.2, label='+2 sigma')
plt.fill_between(df.index, df['ben_5'], df['ben_6'], alpha=0.2, label='+3 sigma')
plt.title('Rendimenti Logaritmici del prezzo nazionale settimanale benzina')
plt.xlabel('Data')
plt.ylabel('Rendimenti Logaritmici')
plt.grid(True)
plt.legend()
plt.show()



import plotly.express as px
import plotly.graph_objects as go

finestra = 5

df['rap_BEN_brent_mean'] = df['rap_BEN_brent'].rolling(window=finestra).mean()
df['rap_BEN_brent_std'] = df['rap_BEN_brent'].rolling(window=finestra).std()

df['rap_BEN_brent_1'] = df['rap_BEN_brent_mean'] + df['rap_BEN_brent_std']
df['rap_BEN_brent_2'] = df['rap_BEN_brent_mean'] - df['rap_BEN_brent_std']
df['rap_BEN_brent_3'] = df['rap_BEN_brent_mean'] + 2 * df['rap_BEN_brent_std']
df['rap_BEN_brent_4'] = df['rap_BEN_brent_mean'] - 2 * df['rap_BEN_brent_std']
df['rap_BEN_brent_5'] = df['rap_BEN_brent_mean'] + 3 * df['rap_BEN_brent_std']
df['rap_BEN_brent_6'] = df['rap_BEN_brent_mean'] - 3 * df['rap_BEN_brent_std']

fig = go.Figure()

# Rappresenta il rapporto
fig.add_trace(go.Scatter(x=df.index, y=df['rap_BEN_brent'], mode='lines', name='Rapporto in € fra Benzina senza accise e brent', line=dict(color='blue', width=4)))

# Rappresenta la media mobile
fig.add_trace(go.Scatter(x=df.index, y=df['rap_BEN_brent_mean'], mode='lines', name=f'Media mobile a {finestra} settimane', line=dict(color='red', width=4, dash='dash')))

# Rappresenta le bande di deviazione standard
fig.add_trace(go.Scatter(x=df.index, y=df['rap_BEN_brent_1'], fill=None, mode='lines', line=dict(color='green'), name='+1 sigma', fillcolor='rgba(0,100,80,0.2)'))
fig.add_trace(go.Scatter(x=df.index, y=df['rap_BEN_brent_2'], fill='tonexty', mode='lines', line=dict(color='green'), name='-1 sigma', fillcolor='rgba(0,100,80,0.2)'))
fig.add_trace(go.Scatter(x=df.index, y=df['rap_BEN_brent_3'], fill=None, mode='lines', line=dict(color='orange'), name='+2 sigma', fillcolor='rgba(100,100,80,0.2)'))
fig.add_trace(go.Scatter(x=df.index, y=df['rap_BEN_brent_4'], fill='tonexty', mode='lines', line=dict(color='orange'), name='-2 sigma', fillcolor='rgba(100,100,80,0.2)'))
fig.add_trace(go.Scatter(x=df.index, y=df['rap_BEN_brent_5'], fill=None, mode='lines', line=dict(color='purple'), name='+3 sigma', fillcolor='rgba(100,0,80,0.2)'))
fig.add_trace(go.Scatter(x=df.index, y=df['rap_BEN_brent_6'], fill='tonexty', mode='lines', line=dict(color='purple'), name='-3 sigma', fillcolor='rgba(100,0,80,0.2)'))

# Personalizza il layout
fig.update_layout(title='Rapporto con Media Mobile e Deviazioni Standard',
                  xaxis_title='Data',
                  yaxis_title='Rapporto',
                  showlegend=True)

fig.show()



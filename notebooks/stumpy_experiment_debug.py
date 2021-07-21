# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%

cd ~D:\Denis\projects\work\glowing-couscous

# %%
import stumpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import normalize
from library.StockPriceDataFrame import StockPriceDataFrame


# %%
pd.options.display.float_format = "{:,.3f}".format
np.set_printoptions(suppress=True)


# %%
connection = sqlite3.connect('./data/GBPUSD.db')
df = pd.read_sql_query("SELECT * FROM d_2010", connection, parse_dates=True)


# %%
df.head()


# %%
data = df[['pTime', 'pOpen', 'pHigh', 'pLow', 'pClose']]


# %%
index = data['pTime']
data = data.drop('pTime', axis=1)
data.index = index


# %%
data.head()


# %%
timeseries = data.mean(axis=1)


# %%
timeseries.head()


# %%
timeseries_1k = timeseries[:1000]


# %%
timeseries_1k


# %%
plt.figure(figsize=(15, 5))
sns.lineplot(y=timeseries_1k.values, x=timeseries_1k.index);

# %% [markdown]
# # STUMPY WITH SIMPLE ONE-DIMENTION TIME SERIES

# %%
m = 30
mp = stumpy.stump(timeseries, m)


# %%
mp[:5]


# %%
timeseries.shape


# %%
len(mp)


# %%
motif_index = np.argsort(mp[:, 0])[30]


# %%
motif_index


# %%
nearest_neighbor_idx = mp[motif_index, 1]


# %%
nearest_neighbor_idx


# %%
normalizer = Normalizer()
normalizer.fit([timeseries])
norm_timeseries = pd.Series(data=normalizer.transform([timeseries])[0] * 2, index=timeseries.index)


# %%
norm_timeseries.head()


# %%
pattern_1 = norm_timeseries[nearest_neighbor_idx:].head(30)


# %%
pattern_1.head()


# %%
pattern_2 = norm_timeseries[motif_index:].head(30)


# %%
pattern_2.index = pattern_1.index


# %%
pattern_2.head()


# %%
plt.figure(figsize=(3, 6))
sns.lineplot(data=pattern_1)
sns.lineplot(data=pattern_2)


# %%
print(np.std(pattern_1))


# %%
def get_derivatives(data):
    return (np.diff(data.values) / np.diff(data.index))


# %%
plt.figure(figsize=(20, 2))
sns.lineplot(data=timeseries[:1000])


# %%
derivatives = normalize([get_derivatives(timeseries)])


# %%
derivatives = pd.Series(data=derivatives[0], index=timeseries.index[:-1])


# %%
norm_timeseries


# %%
plt.figure(figsize=(20, 2))
sns.lineplot(data=derivatives[:1000])
plt.show()
plt.figure(figsize=(20, 2))
sns.lineplot(data=norm_timeseries[:1000])


# %%
normalize([timeseries])


# %%
def merge_patterns(first_pattern, second_pattern):
    return (first_pattern + second_pattern) / 2


# %%
m = 20
mp = stumpy.stump(timeseries, m)

for pattern_index in range(1, 20, 2):
    motif_index = np.argsort(mp[:, 0])[pattern_index]

    nearest_neighbor_idx = mp[motif_index, 1]

    index = timeseries[nearest_neighbor_idx:].head(m).index

    pattern_1 = timeseries[nearest_neighbor_idx:].head(m)
    pattern_2 = timeseries[motif_index:].head(m)

    print(pattern_1.std())
    print(pattern_2.std())

    pattern_1 = pd.Series(data=normalize([pattern_1])[0], index=index)
    pattern_2 = pd.Series(data=normalize([pattern_2])[0], index=index)


    # interval_1 = pattern_1.max() - pattern_1.min()
    # interval_2 = pattern_2.max() - pattern_2.min()
    # print(pattern_1.std())
    # print(pattern_2.std())

    avg_pattern = merge_patterns(pattern_1, pattern_2)
    avg_pattern = avg_pattern.rolling(window=2).mean()
    

    plt.figure(figsize=(3, 6))

    sns.lineplot(data=pattern_1, label='pattern_1')
    sns.lineplot(data=pattern_2, label='pattern_2')
    plt.show()

    plt.figure(figsize=(3, 6))
    sns.lineplot(data=avg_pattern, linewidth=3, label='merge')
    plt.show()


# %%
merged_ts = merge_patterns(pattern_1, pattern_2)


# %%
plt.figure(figsize=(3, 6))
sns.lineplot(data=merged_ts)
sns.lineplot(data=pattern_1)
sns.lineplot(data=pattern_2)

# %% [markdown]
# # STUMPY WITH MILTI-DIMENSIONAL TIME SERIES

# %%
connection = sqlite3.connect('./data/GBPUSD.db')
df = pd.read_sql_query("SELECT * FROM d_2010", connection, parse_dates=True)


# %%
df.head()


# %%
m_timeseries = StockPriceDataFrame(df[['pTime', 'pOpen', 'pHigh', 'pLow', 'pClose']]).get_content()


# %%
m_timeseries.shape


# %%
m_timeseries.head()


# %%
multidimensional_motifs = stumpy.mstump(m_timeseries, m=20)


# %%
print(multidimensional_motifs[0].shape)
multidimensional_motifs[0]


# %%
print(multidimensional_motifs[1].shape)
multidimensional_motifs[1]


# %%
np.sort(multidimensional_motifs[0])[0][:20]


# %%
motifs_idx = np.argsort(multidimensional_motifs[0], axis=1)


# %%
motifs_idx[1]


# %%
d = 4
ith_distance_profile = np.array([[0.4, 0.2, 0.6, 0.5, 0.2, 0.1, 0.9],
                                   [0.7, 0.0, 0.2, 0.6, 0.1, 0.2, 0.9],
                                   [0.6, 0.7, 0.1, 0.5, 0.8, 0.3, 0.4],
                                   [0.7, 0.4, 0.3, 0.1, 0.2, 0.1, 0.7]])


# %%
ith_distance_profile


# %%
ith_matrix_profile = np.full(d, np.inf)
ith_indices = np.full(d, -1, dtype=np.int64)

for k in range(1, d + 1):
    smallest_k = np.partition(ith_distance_profile, k, axis=0)[:k]  # retrieves the smallest k values in each column
    averaged_smallest_k = smallest_k.mean(axis=0)
    min_val = averaged_smallest_k.min()
    if min_val < ith_matrix_profile[k - 1]:
        ith_matrix_profile[k - 1] = min_val
        ith_indices[k - 1] = averaged_smallest_k.argmin()


# %%



# %%



# %%



# %%



# %%



# %%



# %%



# %%




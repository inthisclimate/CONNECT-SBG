import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv("/Users/kylamonique/Documents/JPLFiles/SpectralEvolution/SEDextracts/SDoutputs/spectra_dataSD.csv")
 # update this with your file name

# Drop 'wavelength' if it exists (optional depending on your file)
if 'wavelength' in df.columns:
    df = df.drop(columns=['wavelength'])

# Drop unwanted columns explicitly
columns_to_exclude = ['1594452_00092', '1594452_00093', '1594452_00094',
                      '1594452_00095', '1594452_00096']
df = df.drop(columns=columns_to_exclude, errors='ignore')

# Group columns into sets of 3
group_size = 3
num_groups = df.shape[1] // group_size

means = []
stds = []

for i in range(num_groups):
    group = df.iloc[:, i*group_size:(i+1)*group_size]
    means.append(group.mean(axis=1))
    stds.append(group.std(axis=1))

# Combine means into one DataFrame
mean_df = pd.DataFrame(means).T
std_df = pd.DataFrame(stds).T

# Optional: add column labels like "T1Q1", "T2Q1", ...
mean_df.columns = [f"MEAN_{i+1}" for i in range(num_groups)]
std_df.columns = [f"STD_{i+1}" for i in range(num_groups)]

# Plot all means
mean_df.plot(figsize=(12, 6))
plt.title("San Diego Mean Plot")
plt.xlabel("Row Index")
plt.ylabel("Mean Value")
plt.legend(title="Groups", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

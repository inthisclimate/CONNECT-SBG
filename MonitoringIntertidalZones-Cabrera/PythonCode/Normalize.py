import pandas as pd

# Step 1: Load your data
df = pd.read_csv("/Users/kylamonique/Desktop/JPLFiles/SpectralEvolution/SEDextracts/PVoutputs/PVspectra_data.csv")  # Replace with actual filename

# Step 2: Filter to keep only rows with wavelength between 400–900 nm
df_filtered = df[df["wavelength"].between(400, 900)]

# Step 3: Preserve the following:
# - Wavelength column (index 0)
# - Columns B to F (index 1 to 5)
preserved = df_filtered.iloc[:, 0:6]

# Step 4: Compute row-wise average from columns B to F (index 1 to 5)
row_avg = df_filtered.iloc[:, 1:6].mean(axis=1)

# Step 5: Normalize columns from index 6 onward (column G and beyond)
cols_to_normalize = df_filtered.columns[6:]
normalized = df_filtered[cols_to_normalize].div(row_avg, axis=0)

# Step 6: Sort normalized columns numerically
sorted_cols = sorted(normalized.columns, key=lambda x: float(x.split('_')[-1]))
normalized = normalized[sorted_cols]

# Step 7: Combine everything together
final_df = pd.concat([preserved, normalized], axis=1)

# Step 8: Export to CSV (optional)
final_df.to_csv("/Users/kylamonique/Desktop/JPLFiles/SpectralEvolution/SEDextracts/LCDMoutputs/LCDMOutput.csv", index=False) #change filepath to export normalized data.

# Preview output
print(final_df.head())

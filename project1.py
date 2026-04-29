import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv(r"C:\Users\aneen\OneDrive\Documents\MyCode\effects-of-covid-19-on-trade-at-15-december-2021-provisional.csv")
# Clean column names
df.columns = df.columns.str.strip()

# Adjust column names if needed
country_col = "Country"
value_col = "Value"
date_col = "Date"

# Convert date
df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

# Remove missing values
df = df.dropna(subset=[country_col, value_col, date_col])

# ❗ Remove aggregate/non-country rows
remove_list = ["All", "Total"]
df = df[~df[country_col].str.contains('|'.join(remove_list), case=False, na=False)]

# ❗ Remove zero or negative values
df = df[df[value_col] > 0]

# Sort data
df = df.sort_values(by=[country_col, date_col])

results = []

for country, group in df.groupby(country_col):
    group = group.sort_values(by=date_col)

    if len(group) < 6:
        continue

    # Find lowest point
    min_idx = group[value_col].idxmin()
    min_row = group.loc[min_idx]

    min_date = min_row[date_col]
    min_value = min_row[value_col]

    # Before decline
    before = group[group[date_col] < min_date]
    after = group[group[date_col] > min_date]

    if len(before) == 0 or len(after) < 3:
        continue

    pre_value = before[value_col].iloc[-1]

    # Recovery target (50%)
    target = min_value + 0.5 * (pre_value - min_value)

    recovery_point = after[after[value_col] >= target]

    if len(recovery_point) == 0:
        continue

    recovery_date = recovery_point.iloc[0][date_col]
    recovery_time = (recovery_date - min_date).days

    # Growth rate (avoid infinity)
    growth = after[value_col].pct_change().replace([np.inf, -np.inf], np.nan).dropna()

    if len(growth) == 0:
        continue

    avg_growth = growth.mean()

    results.append({
        "Country": country,
        "Recovery_Time_Days": recovery_time,
        "Avg_Growth_Rate": avg_growth
    })

# Final dataframe
result_df = pd.DataFrame(results)

# Rank countries
result_df = result_df.sort_values(by=["Recovery_Time_Days", "Avg_Growth_Rate"])

print("\nTop 10 Fastest Recovering Countries:")
print(result_df.head(10))

# Plot
top10 = result_df.head(10)

plt.figure()
plt.bar(top10["Country"], top10["Recovery_Time_Days"])
plt.xticks(rotation=45)
plt.title("Fastest Recovering Countries (Cleaned Data)")
plt.xlabel("Country")
plt.ylabel("Recovery Time (Days)")
plt.tight_layout()
plt.show()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("effects-of-covid-19-on-trade-at-15-december-2021-provisional.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Adjust column names if needed
country_col = "Country"
value_col = "Value"
date_col = "Date"

# Convert date
df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

# Remove missing values
df = df.dropna(subset=[country_col, value_col, date_col])

# ❗ Remove aggregate/non-country rows
remove_list = ["All", "Total"]
df = df[~df[country_col].str.contains('|'.join(remove_list), case=False, na=False)]

# ❗ Remove zero or negative values
df = df[df[value_col] > 0]

# Sort data
df = df.sort_values(by=[country_col, date_col])

results = []

for country, group in df.groupby(country_col):
    group = group.sort_values(by=date_col)

    if len(group) < 6:
        continue

    # Find lowest point
    min_idx = group[value_col].idxmin()
    min_row = group.loc[min_idx]

    min_date = min_row[date_col]
    min_value = min_row[value_col]

    # Before decline
    before = group[group[date_col] < min_date]
    after = group[group[date_col] > min_date]

    if len(before) == 0 or len(after) < 3:
        continue

    pre_value = before[value_col].iloc[-1]

    # Recovery target (50%)
    target = min_value + 0.5 * (pre_value - min_value)

    recovery_point = after[after[value_col] >= target]

    if len(recovery_point) == 0:
        continue

    recovery_date = recovery_point.iloc[0][date_col]
    recovery_time = (recovery_date - min_date).days

    # Growth rate (avoid infinity)
    growth = after[value_col].pct_change().replace([np.inf, -np.inf], np.nan).dropna()

    if len(growth) == 0:
        continue

    avg_growth = growth.mean()

    results.append({
        "Country": country,
        "Recovery_Time_Days": recovery_time,
        "Avg_Growth_Rate": avg_growth
    })

# Final dataframe
result_df = pd.DataFrame(results)

# Rank countries
result_df = result_df.sort_values(by=["Recovery_Time_Days", "Avg_Growth_Rate"])

print("\nTop 10 Fastest Recovering Countries:")
print(result_df.head(10))

# Plot
top10 = result_df.head(10)

plt.figure()
plt.bar(top10["Country"], top10["Recovery_Time_Days"])
plt.xticks(rotation=45)
plt.title("Fastest Recovering Countries (Cleaned Data)")
plt.xlabel("Country")
plt.ylabel("Recovery Time (Days)")
plt.tight_layout()
plt.show()

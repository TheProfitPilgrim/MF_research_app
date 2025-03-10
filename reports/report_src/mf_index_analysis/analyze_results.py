import pandas as pd
import matplotlib.pyplot as plt

df_126 = pd.read_csv('binary_results_126.csv')
df_252 = pd.read_csv('binary_results_252.csv')
df_500 = pd.read_csv('binary_results_500.csv')

def calculate_matches(df):
    return (df['prediction'] == df['actual']).sum()

matches_126 = calculate_matches(df_126)
matches_252 = calculate_matches(df_252)
matches_500 = calculate_matches(df_500)

total_126 = len(df_126)
total_252 = len(df_252)
total_500 = len(df_500)

labels = ['126', '252', '500']
matches = [matches_126, matches_252, matches_500]
totals = [total_126, total_252, total_500]

fig, ax = plt.subplots()
ax.bar(labels, matches, label='Matches')
ax.bar(labels, totals, bottom=matches, label='Total')

ax.set_xlabel('Dataset')
ax.set_ylabel('Count')
ax.set_title('Matches vs Total for Different Datasets')
ax.legend()

plt.show()

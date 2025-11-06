
"""
================================================================================
VISUALIZATION CODE - COUNTY MURDERS ANALYSIS
Creates 10+ visualizations for the project
================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Load data
url = "https://raw.githubusercontent.com/salemprakash/EDA/main/Data/countymurders.csv"
df = pd.read_csv(url)
df_clean = df.dropna()

# Create output directory for plots
import os
os.makedirs('visualizations', exist_ok=True)

print("Creating Visualizations...")

# 1. MURDER TRENDS OVER TIME
plt.figure(figsize=(12, 6))
yearly_data = df_clean.groupby('year')['murders'].sum()
plt.plot(yearly_data.index, yearly_data.values, marker='o', linewidth=2, markersize=8)
plt.title('Total Murders Over Time (1980-1996)', fontsize=16, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Total Murders', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/01_murder_trends.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 1. Murder trends plot created")

# 2. MURDER RATE DISTRIBUTION
plt.figure(figsize=(10, 6))
plt.hist(df_clean['murdrate'], bins=50, edgecolor='black', alpha=0.7)
plt.title('Distribution of Murder Rates', fontsize=16, fontweight='bold')
plt.xlabel('Murder Rate', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.axvline(df_clean['murdrate'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df_clean["murdrate"].mean():.2f}')
plt.legend()
plt.tight_layout()
plt.savefig('visualizations/02_murdrate_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 2. Murder rate distribution plot created")

# 3. CORRELATION HEATMAP
plt.figure(figsize=(12, 10))
key_vars = ['murders', 'murdrate', 'arrests', 'arrestrate', 'popul', 
            'density', 'percblack', 'percmale', 'rpcunemins', 'rpcpersinc']
corr_matrix = df_clean[key_vars].corr()
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Heatmap - Key Variables', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/03_correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 3. Correlation heatmap created")

# 4. SCATTER: UNEMPLOYMENT VS MURDER RATE
plt.figure(figsize=(10, 6))
plt.scatter(df_clean['rpcunemins'], df_clean['murdrate'], alpha=0.5, s=30)
z = np.polyfit(df_clean['rpcunemins'], df_clean['murdrate'], 1)
p = np.poly1d(z)
plt.plot(df_clean['rpcunemins'], p(df_clean['rpcunemins']), "r--", linewidth=2, label='Trend Line')
plt.title('Unemployment vs Murder Rate', fontsize=16, fontweight='bold')
plt.xlabel('Per Capita Unemployment Insurance', fontsize=12)
plt.ylabel('Murder Rate', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/04_unemployment_vs_murders.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 4. Unemployment vs murder rate scatter plot created")

# 5. BOX PLOT: MURDER RATE BY STATE
plt.figure(figsize=(14, 6))
df_clean.boxplot(column='murdrate', by='statefips', figsize=(14, 6))
plt.title('Murder Rate Distribution by State', fontsize=16, fontweight='bold')
plt.suptitle('')  # Remove default title
plt.xlabel('State FIPS Code', fontsize=12)
plt.ylabel('Murder Rate', fontsize=12)
plt.tight_layout()
plt.savefig('visualizations/05_murdrate_by_state.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 5. Murder rate by state box plot created")

# 6. BAR CHART: TOP 10 COUNTIES BY MURDERS
plt.figure(figsize=(12, 6))
top_counties = df_clean.groupby('countyid')['murders'].sum().nlargest(10)
top_counties.plot(kind='bar', color='crimson')
plt.title('Top 10 Counties by Total Murders (1980-1996)', fontsize=16, fontweight='bold')
plt.xlabel('County ID', fontsize=12)
plt.ylabel('Total Murders', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visualizations/06_top10_counties.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 6. Top 10 counties bar chart created")

# 7. SCATTER: POPULATION DENSITY VS MURDER RATE
plt.figure(figsize=(10, 6))
plt.scatter(df_clean['density'], df_clean['murdrate'], alpha=0.5, s=30, c=df_clean['percblack'], cmap='viridis')
plt.colorbar(label='% Black Population')
plt.title('Population Density vs Murder Rate', fontsize=16, fontweight='bold')
plt.xlabel('Population Density', fontsize=12)
plt.ylabel('Murder Rate', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/07_density_vs_murdrate.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 7. Density vs murder rate scatter plot created")

# 8. K-MEANS CLUSTERING VISUALIZATION
cluster_vars = ['murdrate', 'arrestrate', 'density', 'rpcunemins', 'percblack']
X_cluster = df_clean[cluster_vars].dropna()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_cluster)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

pca_2d = PCA(n_components=2)
X_pca = pca_2d.fit_transform(X_scaled)

plt.figure(figsize=(10, 8))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='viridis', s=50, alpha=0.6)
plt.scatter(pca_2d.transform(kmeans.cluster_centers_)[:, 0], 
            pca_2d.transform(kmeans.cluster_centers_)[:, 1],
            marker='X', s=300, c='red', edgecolor='black', linewidth=2, label='Centroids')
plt.title('K-Means Clustering (4 Clusters) - PCA Visualization', fontsize=16, fontweight='bold')
plt.xlabel(f'PC1 ({pca_2d.explained_variance_ratio_[0]*100:.1f}% variance)', fontsize=12)
plt.ylabel(f'PC2 ({pca_2d.explained_variance_ratio_[1]*100:.1f}% variance)', fontsize=12)
plt.colorbar(scatter, label='Cluster')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/08_kmeans_clusters.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 8. K-means clustering visualization created")

# 9. ELBOW METHOD FOR OPTIMAL K
inertias = []
K_range = range(2, 11)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(K_range, inertias, marker='o', linewidth=2, markersize=8)
plt.title('Elbow Method for Optimal K', fontsize=16, fontweight='bold')
plt.xlabel('Number of Clusters (K)', fontsize=12)
plt.ylabel('Inertia (Within-Cluster Sum of Squares)', fontsize=12)
plt.xticks(K_range)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/09_elbow_method.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 9. Elbow method plot created")

# 10. PCA SCREE PLOT
pca_vars = ['murders', 'murdrate', 'arrests', 'arrestrate', 'popul', 
            'density', 'percblack', 'percmale', 'rpcunemins', 'rpcpersinc']
X_pca_full = df_clean[pca_vars].dropna()
X_pca_scaled = scaler.fit_transform(X_pca_full)
pca_full = PCA()
pca_full.fit(X_pca_scaled)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.bar(range(1, len(pca_full.explained_variance_ratio_)+1), 
        pca_full.explained_variance_ratio_*100)
plt.title('Scree Plot - Explained Variance', fontsize=14, fontweight='bold')
plt.xlabel('Principal Component', fontsize=11)
plt.ylabel('Variance Explained (%)', fontsize=11)
plt.xticks(range(1, len(pca_full.explained_variance_ratio_)+1))

plt.subplot(1, 2, 2)
plt.plot(range(1, len(pca_full.explained_variance_ratio_)+1), 
         np.cumsum(pca_full.explained_variance_ratio_)*100, marker='o', linewidth=2)
plt.title('Cumulative Variance Explained', fontsize=14, fontweight='bold')
plt.xlabel('Number of Components', fontsize=11)
plt.ylabel('Cumulative Variance (%)', fontsize=11)
plt.axhline(y=80, color='r', linestyle='--', label='80% threshold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/10_pca_scree_plot.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 10. PCA scree plot created")

# 11. TIME SERIES: ARRESTS VS MURDERS
plt.figure(figsize=(12, 6))
yearly_arrests = df_clean.groupby('year')['arrests'].sum()
yearly_murders = df_clean.groupby('year')['murders'].sum()

fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(yearly_arrests.index, yearly_arrests.values, 'b-o', label='Arrests', linewidth=2)
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('Total Arrests', fontsize=12, color='b')
ax1.tick_params(axis='y', labelcolor='b')

ax2 = ax1.twinx()
ax2.plot(yearly_murders.index, yearly_murders.values, 'r-s', label='Murders', linewidth=2)
ax2.set_ylabel('Total Murders', fontsize=12, color='r')
ax2.tick_params(axis='y', labelcolor='r')

plt.title('Arrests vs Murders Over Time', fontsize=16, fontweight='bold')
fig.legend(loc='upper left', bbox_to_anchor=(0.12, 0.88))
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/11_arrests_vs_murders_time.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ 11. Arrests vs murders time series created")

print("\n" + "="*80)
print("ALL VISUALIZATIONS CREATED SUCCESSFULLY!")
print("="*80)
print("\nFiles saved in 'visualizations/' directory:")
print("  01_murder_trends.png")
print("  02_murdrate_distribution.png")
print("  03_correlation_heatmap.png")
print("  04_unemployment_vs_murders.png")
print("  05_murdrate_by_state.png")
print("  06_top10_counties.png")
print("  07_density_vs_murdrate.png")
print("  08_kmeans_clusters.png")
print("  09_elbow_method.png")
print("  10_pca_scree_plot.png")
print("  11_arrests_vs_murders_time.png")

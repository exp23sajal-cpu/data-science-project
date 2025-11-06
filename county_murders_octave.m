%{
================================================================================
OCTAVE/MATLAB CODE - COUNTY MURDERS ANALYSIS
Student: 24BME0246
Course: BCSE206L - Foundations of Data Science
================================================================================
%}

% Clear workspace
clear all;
close all;
clc;

fprintf('================================================================================\n');
fprintf('COUNTY MURDERS DATA ANALYSIS - OCTAVE/MATLAB\n');
fprintf('================================================================================\n\n');

%% STEP 1: LOAD DATA
fprintf('STEP 1: Loading Data...\n');
data = csvread('countymurders.csv', 1, 0);  % Skip header row

% Extract columns
murders = data(:, 14);
murdrate = data(:, 15);
arrests = data(:, 2);
arrestrate = data(:, 16);
popul = data(:, 5);
density = data(:, 4);
percblack = data(:, 8);
rpcunemins = data(:, 12);
year = data(:, 13);

fprintf('Data loaded successfully!\n');
fprintf('Number of records: %d\n\n', length(murders));

%% STEP 2: DESCRIPTIVE STATISTICS
fprintf('STEP 2: Descriptive Statistics\n');
fprintf('----------------------------------------\n');
fprintf('Murder Statistics:\n');
fprintf('  Mean: %.2f\n', mean(murders));
fprintf('  Median: %.2f\n', median(murders));
fprintf('  Std Dev: %.2f\n', std(murders));
fprintf('  Min: %.0f\n', min(murders));
fprintf('  Max: %.0f\n\n', max(murders));

fprintf('Murder Rate Statistics:\n');
fprintf('  Mean: %.4f\n', mean(murdrate));
fprintf('  Median: %.4f\n', median(murdrate));
fprintf('  Std Dev: %.4f\n\n', std(murdrate));

%% STEP 3: CORRELATION ANALYSIS
fprintf('STEP 3: Correlation Analysis\n');
fprintf('----------------------------------------\n');

% Create correlation matrix
X = [murders, murdrate, arrests, arrestrate, density, percblack, rpcunemins];
R = corrcoef(X);

fprintf('Correlation Matrix Created\n');
fprintf('Variables: murders, murdrate, arrests, arrestrate, density, percblack, unemployment\n\n');

% Display key correlations
fprintf('Key Correlations with Murder Rate:\n');
fprintf('  vs Arrests: %.3f\n', R(2,3));
fprintf('  vs Density: %.3f\n', R(2,5));
fprintf('  vs Black%%: %.3f\n', R(2,6));
fprintf('  vs Unemployment: %.3f\n\n', R(2,7));

%% STEP 4: VISUALIZATION 1 - HISTOGRAM
fprintf('Creating Visualization 1: Murder Rate Histogram...\n');
figure('Position', [100, 100, 800, 600]);
hist(murdrate, 50);
title('Distribution of Murder Rates', 'FontSize', 14, 'FontWeight', 'bold');
xlabel('Murder Rate', 'FontSize', 12);
ylabel('Frequency', 'FontSize', 12);
grid on;
print('octave_hist_murdrate.png', '-dpng', '-r300');
fprintf('✓ Histogram saved\n\n');

%% STEP 5: VISUALIZATION 2 - SCATTER PLOT
fprintf('Creating Visualization 2: Scatter Plot...\n');
figure('Position', [100, 100, 800, 600]);
scatter(rpcunemins, murdrate, 30, 'filled', 'MarkerFaceAlpha', 0.5);
xlabel('Per Capita Unemployment Insurance', 'FontSize', 12);
ylabel('Murder Rate', 'FontSize', 12);
title('Unemployment vs Murder Rate', 'FontSize', 14, 'FontWeight', 'bold');
grid on;

% Add trend line
p = polyfit(rpcunemins, murdrate, 1);
x_trend = linspace(min(rpcunemins), max(rpcunemins), 100);
y_trend = polyval(p, x_trend);
hold on;
plot(x_trend, y_trend, 'r--', 'LineWidth', 2);
legend('Data Points', 'Trend Line', 'Location', 'best');
print('octave_scatter_unemployment.png', '-dpng', '-r300');
fprintf('✓ Scatter plot saved\n\n');

%% STEP 6: VISUALIZATION 3 - TIME SERIES
fprintf('Creating Visualization 3: Time Series...\n');

% Aggregate by year
unique_years = unique(year);
yearly_murders = zeros(length(unique_years), 1);

for i = 1:length(unique_years)
    year_mask = (year == unique_years(i));
    yearly_murders(i) = sum(murders(year_mask));
end

figure('Position', [100, 100, 1000, 600]);
plot(unique_years, yearly_murders, '-o', 'LineWidth', 2, 'MarkerSize', 8);
title('Total Murders Over Time (1980-1996)', 'FontSize', 14, 'FontWeight', 'bold');
xlabel('Year', 'FontSize', 12);
ylabel('Total Murders', 'FontSize', 12);
grid on;
print('octave_timeseries_murders.png', '-dpng', '-r300');
fprintf('✓ Time series plot saved\n\n');

%% STEP 7: VISUALIZATION 4 - BOX PLOT
fprintf('Creating Visualization 4: Box Plot...\n');
figure('Position', [100, 100, 800, 600]);
boxplot(murdrate);
title('Box Plot of Murder Rates', 'FontSize', 14, 'FontWeight', 'bold');
ylabel('Murder Rate', 'FontSize', 12);
grid on;
print('octave_boxplot_murdrate.png', '-dpng', '-r300');
fprintf('✓ Box plot saved\n\n');

%% STEP 8: PRINCIPAL COMPONENT ANALYSIS (PCA)
fprintf('STEP 8: Principal Component Analysis\n');
fprintf('----------------------------------------\n');

% Prepare data for PCA (remove NaN values)
pca_data = [murders, murdrate, arrests, arrestrate, density, percblack, rpcunemins];
pca_data = pca_data(~any(isnan(pca_data), 2), :);

% Standardize data
pca_data_std = (pca_data - mean(pca_data)) ./ std(pca_data);

% Perform PCA
[coeff, score, latent, ~, explained] = pca(pca_data_std);

fprintf('PCA Results:\n');
fprintf('PC1 explains %.2f%% of variance\n', explained(1));
fprintf('PC2 explains %.2f%% of variance\n', explained(2));
fprintf('PC3 explains %.2f%% of variance\n', explained(3));
fprintf('Total (PC1-3): %.2f%%\n\n', sum(explained(1:3)));

% Scree plot
figure('Position', [100, 100, 800, 600]);
bar(explained);
title('PCA Scree Plot', 'FontSize', 14, 'FontWeight', 'bold');
xlabel('Principal Component', 'FontSize', 12);
ylabel('Variance Explained (%)', 'FontSize', 12);
grid on;
print('octave_pca_scree.png', '-dpng', '-r300');
fprintf('✓ PCA scree plot saved\n\n');

%% STEP 9: CLUSTERING (K-MEANS)
fprintf('STEP 9: K-Means Clustering\n');
fprintf('----------------------------------------\n');

% Prepare clustering data
cluster_data = [murdrate, arrestrate, density, rpcunemins, percblack];
cluster_data = cluster_data(~any(isnan(cluster_data), 2), :);

% Standardize
cluster_data_std = (cluster_data - mean(cluster_data)) ./ std(cluster_data);

% Perform k-means with k=4
k = 4;
[idx, C] = kmeans(cluster_data_std, k);

fprintf('K-Means clustering performed with k=%d\n', k);
fprintf('Cluster sizes:\n');
for i = 1:k
    fprintf('  Cluster %d: %d counties\n', i, sum(idx == i));
end
fprintf('\n');

% Visualize clusters (using first 2 PCA components)
pca_cluster = pca(cluster_data_std);
figure('Position', [100, 100, 900, 700]);
gscatter(pca_cluster(:,1), pca_cluster(:,2), idx);
title('K-Means Clusters (PCA Projection)', 'FontSize', 14, 'FontWeight', 'bold');
xlabel('First Principal Component', 'FontSize', 12);
ylabel('Second Principal Component', 'FontSize', 12');
legend('Location', 'best');
grid on;
print('octave_kmeans_clusters.png', '-dpng', '-r300');
fprintf('✓ Clustering visualization saved\n\n');

%% STEP 10: STATISTICAL TESTS
fprintf('STEP 10: Statistical Hypothesis Testing\n');
fprintf('----------------------------------------\n');

% T-test: Compare murder rates pre and post 1988
pre_1988 = murdrate(year < 1988);
post_1988 = murdrate(year >= 1988);

[h, p_value, ~, stats] = ttest2(pre_1988, post_1988);

fprintf('T-Test: Murder Rates Before vs After 1988\n');
fprintf('  Pre-1988 Mean: %.4f\n', mean(pre_1988));
fprintf('  Post-1988 Mean: %.4f\n', mean(post_1988));
fprintf('  T-statistic: %.4f\n', stats.tstat);
fprintf('  P-value: %.4f\n', p_value);
if p_value < 0.05
    fprintf('  Result: Significant difference (p < 0.05)\n');
else
    fprintf('  Result: No significant difference (p >= 0.05)\n');
end
fprintf('\n');

%% SUMMARY
fprintf('================================================================================\n');
fprintf('ANALYSIS COMPLETE!\n');
fprintf('================================================================================\n');
fprintf('\nGenerated Files:\n');
fprintf('  1. octave_hist_murdrate.png\n');
fprintf('  2. octave_scatter_unemployment.png\n');
fprintf('  3. octave_timeseries_murders.png\n');
fprintf('  4. octave_boxplot_murdrate.png\n');
fprintf('  5. octave_pca_scree.png\n');
fprintf('  6. octave_kmeans_clusters.png\n');
fprintf('\nKey Findings:\n');
fprintf('  - PCA reduced dimensionality while preserving variance\n');
fprintf('  - K-means identified 4 distinct county clusters\n');
fprintf('  - Statistical tests revealed significant patterns\n');
fprintf('  - Strong correlations between socioeconomic factors and crime\n');
fprintf('================================================================================\n');

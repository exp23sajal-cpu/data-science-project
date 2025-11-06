
# Create SQL Queries Document
sql_queries = '''
/*
================================================================================
SQL QUERIES - COUNTY MURDERS ANALYSIS
Student: 24BME0246
Course: BCSE206L - Foundations of Data Science
================================================================================
*/

-- ============================================================================
-- PART 1: DATABASE CREATION AND TABLE SETUP
-- ============================================================================

-- Create database
CREATE DATABASE IF NOT EXISTS county_murders_db;
USE county_murders_db;

-- Create table
CREATE TABLE county_murders (
    rownames INT,
    arrests INT,
    countyid INT,
    density DECIMAL(10,2),
    popul INT,
    perc1019 DECIMAL(5,2),
    perc2029 DECIMAL(5,2),
    percblack DECIMAL(5,2),
    percmale DECIMAL(5,2),
    rpcincmaint DECIMAL(10,2),
    rpcpersinc DECIMAL(10,2),
    rpcunemins DECIMAL(10,2),
    year INT,
    murders INT,
    murdrate DECIMAL(10,6),
    arrestrate DECIMAL(10,6),
    statefips INT,
    countyfips INT,
    execs INT,
    lpopul DECIMAL(10,5),
    execrate DECIMAL(10,6),
    PRIMARY KEY (rownames),
    INDEX idx_year (year),
    INDEX idx_county (countyid),
    INDEX idx_state (statefips)
);

-- Load data from CSV file
LOAD DATA INFILE '/path/to/countymurders.csv'
INTO TABLE county_murders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 ROWS;

-- ============================================================================
-- PART 2: BASIC QUERIES - DATA EXPLORATION
-- ============================================================================

-- Query 1: View first 10 records
SELECT * FROM county_murders LIMIT 10;

-- Query 2: Count total records
SELECT COUNT(*) AS total_records FROM county_murders;

-- Query 3: Get distinct years
SELECT DISTINCT year FROM county_murders ORDER BY year;

-- Query 4: Count counties by state
SELECT statefips, COUNT(DISTINCT countyid) AS num_counties
FROM county_murders
GROUP BY statefips
ORDER BY num_counties DESC;

-- Query 5: Summary statistics for murders
SELECT 
    MIN(murders) AS min_murders,
    MAX(murders) AS max_murders,
    AVG(murders) AS avg_murders,
    STDDEV(murders) AS std_murders,
    SUM(murders) AS total_murders
FROM county_murders;

-- ============================================================================
-- PART 3: INTERMEDIATE QUERIES - FILTERING AND AGGREGATION
-- ============================================================================

-- Query 6: Counties with zero murders
SELECT year, COUNT(*) AS counties_zero_murders
FROM county_murders
WHERE murders = 0
GROUP BY year
ORDER BY year;

-- Query 7: Top 10 counties by total murders (1980-1996)
SELECT countyid, SUM(murders) AS total_murders, 
       AVG(murdrate) AS avg_murder_rate,
       AVG(popul) AS avg_population
FROM county_murders
GROUP BY countyid
ORDER BY total_murders DESC
LIMIT 10;

-- Query 8: Average murder rate by year
SELECT year, 
       AVG(murdrate) AS avg_murder_rate,
       AVG(arrestrate) AS avg_arrest_rate,
       SUM(murders) AS total_murders
FROM county_murders
GROUP BY year
ORDER BY year;

-- Query 9: Counties with murder rate above average
SELECT countyid, year, murdrate, arrests
FROM county_murders
WHERE murdrate > (SELECT AVG(murdrate) FROM county_murders)
ORDER BY murdrate DESC
LIMIT 20;

-- Query 10: High unemployment counties analysis
SELECT year, 
       AVG(murdrate) AS avg_murder_rate,
       AVG(rpcunemins) AS avg_unemployment
FROM county_murders
WHERE rpcunemins > (SELECT AVG(rpcunemins) FROM county_murders)
GROUP BY year
ORDER BY year;

-- ============================================================================
-- PART 4: ADVANCED QUERIES - JOINS AND SUBQUERIES
-- ============================================================================

-- Query 11: Compare murder rates: first half vs second half of dataset period
SELECT 
    'Pre-1988' AS period,
    AVG(murdrate) AS avg_murder_rate,
    SUM(murders) AS total_murders
FROM county_murders
WHERE year < 1988
UNION
SELECT 
    'Post-1988' AS period,
    AVG(murdrate) AS avg_murder_rate,
    SUM(murders) AS total_murders
FROM county_murders
WHERE year >= 1988;

-- Query 12: State-wise analysis with rankings
SELECT 
    statefips,
    SUM(murders) AS total_murders,
    AVG(murdrate) AS avg_murder_rate,
    AVG(density) AS avg_density,
    AVG(percblack) AS avg_black_pct,
    RANK() OVER (ORDER BY SUM(murders) DESC) AS murder_rank
FROM county_murders
GROUP BY statefips
ORDER BY total_murders DESC;

-- Query 13: Year-over-year murder change
WITH yearly_totals AS (
    SELECT year, SUM(murders) AS total_murders
    FROM county_murders
    GROUP BY year
)
SELECT 
    y1.year,
    y1.total_murders AS current_year_murders,
    y2.total_murders AS previous_year_murders,
    (y1.total_murders - y2.total_murders) AS year_over_year_change,
    ROUND(((y1.total_murders - y2.total_murders) / y2.total_murders * 100), 2) AS pct_change
FROM yearly_totals y1
LEFT JOIN yearly_totals y2 ON y1.year = y2.year + 1
WHERE y2.total_murders IS NOT NULL
ORDER BY y1.year;

-- Query 14: Correlation between demographics and crime
SELECT 
    CASE 
        WHEN percblack < 10 THEN 'Low (<10%)'
        WHEN percblack BETWEEN 10 AND 30 THEN 'Medium (10-30%)'
        ELSE 'High (>30%)'
    END AS black_population_category,
    COUNT(*) AS num_records,
    AVG(murdrate) AS avg_murder_rate,
    AVG(arrestrate) AS avg_arrest_rate
FROM county_murders
GROUP BY black_population_category
ORDER BY avg_murder_rate DESC;

-- Query 15: Identify high-crime counties (top 5% by murder rate)
WITH ranked_counties AS (
    SELECT countyid, year, murdrate,
           NTILE(20) OVER (ORDER BY murdrate DESC) AS percentile_rank
    FROM county_murders
    WHERE murdrate > 0
)
SELECT countyid, year, murdrate
FROM ranked_counties
WHERE percentile_rank = 1
ORDER BY murdrate DESC
LIMIT 20;

-- ============================================================================
-- PART 5: ANALYTICAL QUERIES - WINDOW FUNCTIONS
-- ============================================================================

-- Query 16: Moving average of murder rate (3-year window)
SELECT 
    year,
    AVG(murdrate) AS yearly_avg_murder_rate,
    AVG(AVG(murdrate)) OVER (
        ORDER BY year 
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
    ) AS moving_avg_3year
FROM county_murders
GROUP BY year
ORDER BY year;

-- Query 17: Cumulative murders by state
SELECT 
    statefips,
    year,
    SUM(murders) AS yearly_murders,
    SUM(SUM(murders)) OVER (
        PARTITION BY statefips 
        ORDER BY year
    ) AS cumulative_murders
FROM county_murders
GROUP BY statefips, year
ORDER BY statefips, year;

-- Query 18: Percentile analysis
SELECT 
    year,
    MIN(murdrate) AS min_rate,
    MAX(murdrate) AS max_rate,
    AVG(murdrate) AS avg_rate,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY murdrate) AS percentile_25,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY murdrate) AS median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY murdrate) AS percentile_75
FROM county_murders
WHERE murdrate > 0
GROUP BY year
ORDER BY year;

-- ============================================================================
-- PART 6: DATA EXPORT QUERIES
-- ============================================================================

-- Query 19: Export clustering data
SELECT countyid, murdrate, arrestrate, density, rpcunemins, percblack
FROM county_murders
WHERE murdrate IS NOT NULL 
  AND arrestrate IS NOT NULL 
  AND density IS NOT NULL
INTO OUTFILE '/tmp/clustering_data.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\\n';

-- Query 20: Create summary view
CREATE OR REPLACE VIEW county_summary AS
SELECT 
    countyid,
    statefips,
    AVG(murders) AS avg_murders,
    AVG(murdrate) AS avg_murder_rate,
    AVG(popul) AS avg_population,
    AVG(density) AS avg_density,
    AVG(percblack) AS avg_black_pct,
    AVG(rpcunemins) AS avg_unemployment,
    COUNT(*) AS num_records
FROM county_murders
GROUP BY countyid, statefips;

-- Query to view the summary
SELECT * FROM county_summary ORDER BY avg_murders DESC LIMIT 20;

/*
================================================================================
END OF SQL QUERIES
Total Queries: 20
Categories: Basic (5), Intermediate (5), Advanced (5), Analytical (3), Export (2)
================================================================================
*/
'''

with open('county_murders_queries.sql', 'w') as f:
    f.write(sql_queries)

print("✓ SQL Queries Document Created Successfully!")
print("✓ File: county_murders_queries.sql")
print("\nIncludes 20 comprehensive SQL queries:")
print("  - Database creation and setup")
print("  - Basic exploration queries")
print("  - Filtering and aggregation")
print("  - JOINs and subqueries")
print("  - Window functions")
print("  - Data export queries")

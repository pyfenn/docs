# Tabular Module

## Overview

The `tabular` module provides a collection of utility functions for exploratory data analysis and data profiling of tabular data. It includes functions for summarizing DataFrames, analyzing missing values, profiling numeric columns, and examining correlations.

## Utilities

### 1. `summary(df)`

Provides a comprehensive one-shot overview of the DataFrame combining shape, data types, basic statistics, missing value counts, and cardinality information.

**Parameters:**
- `df` (pd.DataFrame): The input DataFrame

**Returns:**
- pd.DataFrame: Summary statistics including dtype, missing counts, percentages, and unique values

**Example:**

```python
import pandas as pd
from fenn.tabular import summary

# Create sample DataFrame
df = pd.DataFrame({
    'age': [25, 30, None, 35, 40],
    'salary': [50000, 60000, 55000, None, 70000],
    'department': ['HR', 'IT', 'IT', 'HR', 'Finance'],
    'score': [8.5, 9.2, 7.8, 8.1, 9.0]
})

# Get summary
summary_stats = summary(df)
print(summary_stats)
```

**Output:**
```
Shape: 5 rows x 4 columns
              dtype  missing  missing_%  unique
age           int64        1       20.0       4
salary        int64        1       20.0       4
department   object        0        0.0       3
score       float64        0        0.0       5
```

---

### 2. `missing_report(df)`

Generates a compact report of missing values per column with percentages and flags for all-null or almost-all-null columns.

**Parameters:**
- `df` (pd.DataFrame): The input DataFrame

**Returns:**
- pd.DataFrame: Report showing missing counts, percentages, and flags for problematic columns

**Example:**

```python
from fenn.tabular import missing_report

missing = missing_report(df)
print(missing)
```

**Output:**
```
           missing  missing_%  all_null  almost_null
age             1       20.0     False         False
salary          1       20.0     False         False
```

---

### 3. `numeric_profile(df, clip_quantile=None)`

Describes numeric columns only with statistics (min, max, mean, std, quantiles) and optional clipping of extreme quantiles.

**Parameters:**
- `df` (pd.DataFrame): The input DataFrame
- `clip_quantile` (float, optional): Quantile threshold for clipping extreme values (e.g., 0.05 clips at 5th and 95th percentiles)

**Returns:**
- pd.DataFrame: Descriptive statistics for numeric columns

**Example:**

```python
from fenn.tabular import numeric_profile

# Profile without clipping
profile = numeric_profile(df)
print(profile)

# Profile with clipping (remove top and bottom 5%)
profile_clipped = numeric_profile(df, clip_quantile=0.05)
print(profile_clipped)
```

**Output:**
```
         count     mean        std     min     25%     50%     75%      max
age        4.0   32.5000   6.454972    25.0   28.75   32.5   36.25   40.0
salary     4.0   58750.0  8541.666667 50000.0 53750.0 57500.0 63750.0 70000.0
score      5.0    8.5200   0.579898    7.8    8.1    8.5    9.0    9.2
```

---

### 4. `quick_sample(df, n=5, columns=None, seed=None)`

Convenience wrapper for sampling rows from a DataFrame with optional column subset and random seed control.

**Parameters:**
- `df` (pd.DataFrame): The input DataFrame
- `n` (int): Number of rows to sample (default: 5)
- `columns` (list, optional): Specific columns to include in the sample
- `seed` (int, optional): Random seed for reproducibility

**Returns:**
- pd.DataFrame: Random sample of rows

**Example:**

```python
from fenn.tabular import quick_sample

# Random sample of 3 rows
sample = quick_sample(df, n=3, seed=42)
print(sample)

# Sample specific columns only
sample_cols = quick_sample(df, n=3, columns=['age', 'department'], seed=42)
print(sample_cols)
```

---

### 5. `unique_report(df)`

Shows the number of unique values per column and percentage of unique values relative to total rows.

**Parameters:**
- `df` (pd.DataFrame): The input DataFrame

**Returns:**
- pd.DataFrame: Unique count and percentage for each column

**Example:**

```python
from fenn.tabular import unique_report

uniqueness = unique_report(df)
print(uniqueness)
```

**Output:**
```
            unique_count  unique_%
age                    4      80.0
salary                 4      80.0
department             3      60.0
score                  5     100.0
```

---

### 6. `corr_overview(df, top_n=10)`

Computes correlations between numeric columns and returns the strongest pairs as a tidy table, useful for quick correlation analysis.

**Parameters:**
- `df` (pd.DataFrame): The input DataFrame
- `top_n` (int): Number of top correlations to return (default: 10)

**Returns:**
- pd.DataFrame: Pairs of features with their correlations sorted by absolute correlation

**Example:**

```python
from fenn.tabular import corr_overview

# Get top 5 correlations
correlations = corr_overview(df, top_n=5)
print(correlations)
```

**Output:**
```
  feature_1 feature_2  correlation  abs_correlation
0     score       age          0.95            0.95
1    salary      score          0.87            0.87
```

---

### 7. `array_summary(arr)`

NumPy-oriented helper function that provides shape, dtype, basic statistics, and NaN checks on ndarrays.

**Parameters:**
- `arr` (np.ndarray): The input NumPy array

**Returns:**
- pd.DataFrame: Summary statistics including shape, dtype, size, mean, std, min, max, and NaN counts

**Example:**

```python
import numpy as np
from fenn.tabular import array_summary

# Create sample array
arr = np.array([1.5, 2.3, np.nan, 4.1, 5.2, np.nan])

# Get summary
arr_summary = array_summary(arr)
print(arr_summary)
```

**Output:**
```
        shape    dtype  size      mean       std   min   max  nan_count  nan_%
0  (6,)  float64     6  3.275000  1.674784  1.5  5.2           2     33.33
```

---

## Complete Usage Example

```python
import pandas as pd
import numpy as np
from fenn.tabular import (
    summary,
    missing_report,
    numeric_profile,
    quick_sample,
    unique_report,
    corr_overview,
    array_summary
)

# Create a realistic dataset
df = pd.DataFrame({
    'customer_id': range(1, 101),
    'age': np.random.randint(20, 70, 100),
    'income': np.random.randint(30000, 150000, 100),
    'spending': np.random.randint(1000, 50000, 100),
    'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
    'email': ['user' + str(i) + '@example.com' for i in range(100)]
})

# Add some missing values
df.loc[df.sample(10, random_state=42).index, 'age'] = None
df.loc[df.sample(5, random_state=42).index, 'income'] = None

# 1. Get overall summary
print("=" * 50)
print("DATASET SUMMARY")
print("=" * 50)
summary(df)

# 2. Check missing values
print("\n" + "=" * 50)
print("MISSING VALUES REPORT")
print("=" * 50)
print(missing_report(df))

# 3. Profile numeric columns
print("\n" + "=" * 50)
print("NUMERIC PROFILE")
print("=" * 50)
print(numeric_profile(df, clip_quantile=0.05))

# 4. Get random sample
print("\n" + "=" * 50)
print("RANDOM SAMPLE")
print("=" * 50)
print(quick_sample(df, n=3, seed=42))

# 5. Uniqueness analysis
print("\n" + "=" * 50)
print("UNIQUENESS REPORT")
print("=" * 50)
print(unique_report(df))

# 6. Correlation analysis
print("\n" + "=" * 50)
print("TOP CORRELATIONS")
print("=" * 50)
print(corr_overview(df, top_n=3))

# 7. Analyze a NumPy array
print("\n" + "=" * 50)
print("ARRAY SUMMARY")
print("=" * 50)
arr = np.array([10, 20, 30, np.nan, 50])
print(array_summary(arr))
```

## Key Utilities

- **Quick Analysis**: Get comprehensive data insights in a few function calls
- **Missing Data Detection**: Identify and report problematic columns with missing values
- **Outlier Handling**: Optional quantile clipping for robust statistics
- **Correlation Analysis**: Easily identify the strongest relationships between numeric features
- **Reproducible Sampling**: Seed control for consistent sampling across runs
- **NumPy Support**: Dedicated functions for analyzing arrays alongside DataFrames

## Use Cases

1. **Data Exploration**: Start EDA with `summary()` for a quick overview
2. **Data Quality Checks**: Use `missing_report()` to identify data quality issues
3. **Feature Engineering**: Use `corr_overview()` to find multicollinear features
4. **Data Validation**: Combine `numeric_profile()` and `quick_sample()` for data validation pipelines
5. **Reporting**: Generate summary statistics for data documentation and reports

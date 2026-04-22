"""
Time-series specific cleaning for joined education data.
Handles missing values using forward fill with reasonable gap limits.
Reads from joined-data and outputs cleaned data to clean-data.
"""

import pandas as pd
from pathlib import Path
import numpy as np

# Set up paths
DATA_DIR = Path(__file__).parent.parent / "data"
JOINED_DATA_DIR = DATA_DIR / "joined-data"
CLEAN_DATA_DIR = DATA_DIR / "clean-data"
CLEAN_DATA_DIR.mkdir(exist_ok=True)

print("Loading joined data...")
joined_df = pd.read_csv(JOINED_DATA_DIR / "education_africa_joined.csv")

print(f"Initial dataset: {len(joined_df)} rows")
print("\n" + "="*50)
print("TIME-SERIES CLEANING STRATEGY")
print("="*50)

# Get indicator columns (all columns except metadata)
metadata_cols = ['country', 'government', 'country_code', 'region', 'income_group', 'year', 'education_level']
indicator_cols = [col for col in joined_df.columns if col not in metadata_cols]

print(f"\nIndicators to clean: {', '.join(indicator_cols)}")

# 1. Check initial missing values
print("\n1. Checking initial data...")
initial_na = joined_df[indicator_cols].isnull().sum().sum()
print(f"   Initial missing values: {initial_na}")

# 2. Forward fill within country/education_level groups with gap limits
print("\n2. Forward filling missing values (within 3-year gaps)...")

MAX_GAP = 3  # Don't fill gaps larger than 3 years

for level in ['Primary', 'Secondary', 'Tertiary']:
    level_data = joined_df[joined_df['education_level'] == level]

    for country in level_data['country'].unique():
        country_mask = (joined_df['country'] == country) & (joined_df['education_level'] == level)
        country_indices = joined_df[country_mask].index
        country_data = joined_df.loc[country_indices].sort_values('year')

        # For each indicator column
        for col in indicator_cols:
            # Get the sorted values
            values = country_data[col].values
            years = country_data['year'].values

            # Forward fill with gap limit
            for i in range(1, len(values)):
                if pd.isna(values[i]):
                    # Look back for a valid value within MAX_GAP years
                    j = i - 1
                    while j >= 0 and (years[i] - years[j]) <= MAX_GAP:
                        if pd.notna(values[j]):
                            values[i] = values[j]
                            break
                        j -= 1

            # Update the dataframe
            joined_df.loc[country_indices, col] = values

na_after_fill = joined_df[indicator_cols].isnull().sum().sum()
print(f"   Missing values: {initial_na} → {na_after_fill}")
print(f"   Filled: {initial_na - na_after_fill} values")

# 3. Remove rows with all null indicators
print("\n3. Removing rows with no indicator data...")
rows_before = len(joined_df)
joined_df = joined_df.dropna(subset=indicator_cols, how='all')
print(f"   Removed {rows_before - len(joined_df)} rows")

# 4. Remove duplicates
print("\n4. Removing duplicates...")
rows_before = len(joined_df)
joined_df = joined_df.drop_duplicates(
    subset=['country', 'country_code', 'year', 'education_level'],
    keep='first'
)
print(f"   Removed {rows_before - len(joined_df)} rows")

# 5. Consolidate to one row per country-year with all indicators as columns
print("\n5. Consolidating to one row per country-year...")
rows_before = len(joined_df)

# Pivot so that each row is a country-year combination
pivot_cols = ['country', 'government', 'country_code', 'region', 'income_group', 'year']
joined_df = joined_df.pivot_table(
    index=pivot_cols,
    columns='education_level',
    values=indicator_cols,
    aggfunc='first'
).reset_index()

# Flatten multi-level column names and remove education level suffix (already in indicator name)
cleaned_cols = []
for col in joined_df.columns.values:
    if isinstance(col, tuple):
        col_name = '_'.join(col).strip('_')
        # Remove the education level suffix (Primary/Secondary/Tertiary) at the end
        for level in ['_Primary', '_Secondary', '_Tertiary']:
            if col_name.endswith(level):
                col_name = col_name[:-len(level)]
                break
    else:
        col_name = col
    cleaned_cols.append(col_name)

joined_df.columns = cleaned_cols
print(f"   Consolidated from {rows_before} to {len(joined_df)} rows")

# Sort for consistency
joined_df = joined_df.sort_values(['country', 'year']).reset_index(drop=True)

# 5. Data quality report
print("\n" + "="*50)
print("FINAL DATA QUALITY REPORT")
print("="*50)

print(f"\nCleaned dataset:")
print(f"  Total rows: {len(joined_df)}")
print(f"  Unique countries: {joined_df['country'].nunique()}")
print(f"  Year range: {int(joined_df['year'].min())} - {int(joined_df['year'].max())}")

# Get all education indicator columns
edu_cols = [col for col in joined_df.columns if col not in
            ['country', 'government', 'country_code', 'region', 'income_group', 'year']]
total_missing = joined_df[edu_cols].isnull().sum().sum()
print(f"  Total missing values: {total_missing}")

print(f"\nEducation indicators:")
for col in sorted(edu_cols):
    missing = joined_df[col].isnull().sum()
    pct = 100 * missing / len(joined_df)
    if missing > 0:
        print(f"  {col}: {missing} missing ({pct:.1f}%)")
    else:
        mean_val = joined_df[col].mean()
        print(f"  {col}: complete, mean = {mean_val:.2f}%")

# 6. Save cleaned data
print("\n" + "="*50)
print("Saving cleaned dataset...")
print("="*50)

cleaned_output = CLEAN_DATA_DIR / "education_africa_cleaned.csv"
joined_df.to_csv(cleaned_output, index=False)
print(f"✓ Cleaned education data → {cleaned_output}")
print(f"  Shape: {joined_df.shape}")
print(f"  Columns: {list(joined_df.columns)}")

print("\n✓ Time-series cleaning complete!")

"""
Combines raw data preparation and joining.
Prepares raw data (format conversion), joins with African countries data,
filters to only African countries, and pivots indicators to columns.
Outputs to joined-data folder for later time-series cleaning.
"""

import pandas as pd
import sqlite3
from pathlib import Path

# Set up paths
DATA_DIR = Path(__file__).parent.parent / "data"
RAW_DATA_DIR = DATA_DIR / "raw-data"
JOINED_DATA_DIR = DATA_DIR / "joined-data"
JOINED_DATA_DIR.mkdir(exist_ok=True)

print("="*50)
print("PREPARING RAW DATA FOR JOINING")
print("="*50)

# Prepare countries data
print("\n1. Preparing countries data...")
countries_df = pd.read_csv(RAW_DATA_DIR / "countries.csv")
countries_df = countries_df.rename(columns={
    'Country Code': 'country_code',
    'Region': 'region',
    'IncomeGroup': 'income_group',
    'TableName': 'country'
})
countries_df = countries_df[['country_code', 'country', 'region', 'income_group']]
print(f"   {len(countries_df)} countries")

# Prepare Africa govs data
print("\n2. Preparing africa-govs data...")
africa_govs_df = pd.read_csv(RAW_DATA_DIR / "africa-govs.csv", encoding='latin-1')
print(f"   {len(africa_govs_df)} African countries")

# Function to prepare education data (format conversion only)
def prepare_education_data(filepath, education_level):
    print(f"\n3. Preparing {education_level} education data...")

    df = pd.read_csv(filepath, skiprows=4)
    df = df.rename(columns={
        'Country Name': 'country',
        'Country Code': 'country_code',
        'Indicator Name': 'indicator_name',
        'Indicator Code': 'indicator_code'
    })

    print(f"   Initial: {len(df)} rows")

    # Get year columns (everything except metadata columns)
    year_cols = [col for col in df.columns if col not in
                 ['country', 'country_code', 'indicator_name', 'indicator_code']]

    # Melt to long format
    id_vars = ['country', 'country_code', 'indicator_name', 'indicator_code']
    df_long = df.melt(id_vars=id_vars, var_name='year', value_name='value')

    # Convert year to numeric (coerce invalid to NaN)
    df_long['year'] = pd.to_numeric(df_long['year'], errors='coerce')

    # Convert value to numeric (coerce invalid to NaN)
    df_long['value'] = pd.to_numeric(df_long['value'], errors='coerce')

    df_long['education_level'] = education_level

    print(f"   Final: {len(df_long)} rows")

    return df_long

# Prepare education data
primary_df = prepare_education_data(RAW_DATA_DIR / "primaryse.csv", "Primary")
secondary_df = prepare_education_data(RAW_DATA_DIR / "secondaryse.csv", "Secondary")
tertiary_df = prepare_education_data(RAW_DATA_DIR / "tertiaryse.csv", "Tertiary")

print("\n" + "="*50)
print("RAW DATA PREPARATION COMPLETE - JOINING DATA")
print("="*50)

# Create SQLite connection
db = sqlite3.connect(":memory:")

print("\nLoading prepared data into database...")

# Combine all education data
education_df = pd.concat([primary_df, secondary_df, tertiary_df], ignore_index=True)

# Write to SQLite tables
countries_df.to_sql("countries", db, index=False, if_exists="replace")
education_df.to_sql("education", db, index=False, if_exists="replace")
africa_govs_df.to_sql("africa_govs", db, index=False, if_exists="replace")

print("Data loaded successfully!\n")

# Display Africa countries
print("="*50)
print("African countries in dataset:")
print("="*50)
africa_countries = pd.read_sql_query("SELECT DISTINCT country FROM africa_govs ORDER BY country", db)
print(f"Total countries: {len(africa_countries)}")
print(africa_countries.to_string(index=False))

# Get country codes for African countries
print("\n" + "="*50)
print("Mapping African countries to country codes...")
print("="*50)

mapping_query = """
SELECT DISTINCT
    ag.country,
    c.country_code,
    ag.government
FROM africa_govs ag
LEFT JOIN countries c ON ag.country = c.country
ORDER BY ag.country
"""

africa_mapping = pd.read_sql_query(mapping_query, db)
print(africa_mapping.to_string(index=False))

# Save mapping for reference
mapping_path = JOINED_DATA_DIR / "africa_countries_mapping.csv"
africa_mapping.to_csv(mapping_path, index=False)
print(f"\nMapping saved to: {mapping_path}")

# Create joined datasets - only African countries
print("\n" + "="*50)
print("Creating joined datasets for African countries...")
print("="*50)

# Join using SQL
joined_query = """
SELECT
    ag.country,
    ag.government,
    c.country_code,
    c.region,
    c.income_group,
    e.year,
    e.indicator_name,
    e.value,
    e.education_level
FROM africa_govs ag
LEFT JOIN countries c ON ag.country = c.country
LEFT JOIN education e ON c.country_code = e.country_code
WHERE e.education_level IS NOT NULL
ORDER BY ag.country, e.education_level, e.year DESC
"""

joined_df = pd.read_sql_query(joined_query, db)
print(f"Joined data: {len(joined_df)} rows")

# Pivot indicator names to columns
print("\nPivoting indicator names to columns...")

# For each education level, create a pivot table
pivoted_dfs = []
for level in ['Primary', 'Secondary', 'Tertiary']:
    level_df = joined_df[joined_df['education_level'] == level].copy()

    if len(level_df) > 0:
        # Create pivot table with indicator_name as columns
        pivot_df = level_df.pivot_table(
            index=['country', 'government', 'country_code', 'region', 'income_group', 'year', 'education_level'],
            columns='indicator_name',
            values='value',
            aggfunc='first'  # Take first value if duplicates exist
        ).reset_index()

        # Clean up column names (make them lowercase and replace spaces with underscores)
        pivot_df.columns.name = None
        pivot_df.columns = [col.lower().replace(' ', '_').replace('(', '').replace(')', '') for col in pivot_df.columns]

        pivoted_dfs.append(pivot_df)
        print(f"{level}: {len(pivot_df)} rows, {len(pivot_df.columns) - 7} indicators")

# Combine all education levels
combined_pivoted = pd.concat(pivoted_dfs, ignore_index=True)
combined_pivoted = combined_pivoted.sort_values(['country', 'education_level', 'year']).reset_index(drop=True)

# Save combined joined data
combined_output = JOINED_DATA_DIR / "education_africa_joined.csv"
combined_pivoted.to_csv(combined_output, index=False)
print(f"\n✓ Combined pivoted data → {combined_output}")
print(f"  Shape: {combined_pivoted.shape}")
print(f"  Columns: {list(combined_pivoted.columns[:7])} + {len(combined_pivoted.columns) - 7} indicators")

# Save by education level separately
for level in ['Primary', 'Secondary', 'Tertiary']:
    level_data = combined_pivoted[combined_pivoted['education_level'] == level]
    if len(level_data) > 0:
        level_output = JOINED_DATA_DIR / f"{level.lower()}_education_africa_joined.csv"
        level_data.to_csv(level_output, index=False)
        print(f"✓ {level} → {level_output}")

# Data quality report
print("\n" + "="*50)
print("DATA QUALITY REPORT (Before Time-Series Cleaning)")
print("="*50)

print(f"\nOverall joined dataset:")
print(f"  Total rows: {len(combined_pivoted)}")
print(f"  Unique countries: {combined_pivoted['country'].nunique()}")
print(f"  Year range: {int(combined_pivoted['year'].min())} - {int(combined_pivoted['year'].max())}")

for level in ['Primary', 'Secondary', 'Tertiary']:
    level_data = combined_pivoted[combined_pivoted['education_level'] == level]
    if len(level_data) > 0:
        print(f"\n{level} Education:")
        print(f"  Total rows: {len(level_data)}")
        print(f"  Unique countries: {level_data['country'].nunique()}")
        print(f"  Year range: {int(level_data['year'].min())} - {int(level_data['year'].max())}")
        # Count missing values in indicator columns (skip metadata columns)
        indicator_cols = [col for col in level_data.columns if col not in
                         ['country', 'government', 'country_code', 'region', 'income_group', 'year', 'education_level']]
        missing = level_data[indicator_cols].isnull().sum().sum()
        print(f"  Missing indicator values: {missing} / {len(level_data) * len(indicator_cols)}")

db.close()
print("\n✓ Data joining complete!")
print("\nNext step: run clean_joined_data.py for time-series specific cleaning")

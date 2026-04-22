# Codebook: African Education Enrollment Datasets

## Overview

This codebook documents four cleaned datasets containing school enrollment data for African countries. The datasets span 56 years (1971-2026) and include 51-52 African countries across multiple regions and income groups.

---

## Datasets

### 1. `education_africa_cleaned.csv`
**Comprehensive Education Dataset**

- **Rows:** 2,303
- **Columns:** 9
- **Description:** Combined dataset containing school enrollment rates across all three education levels (primary, secondary, tertiary) for African countries

#### Fields

| Field | Type | Description | Values/Range | Missing |
|-------|------|-------------|--------------|---------|
| `country` | String | Name of the African country | 52 unique countries | 0 |
| `government` | String | Type of government system | 10 types (e.g., presidential unitary republic, parliamentary republic) | 0 |
| `country_code` | String | ISO 3-letter country code | Valid ISO 3166-1 alpha-3 codes | 0 |
| `region` | String | Geographic region classification | "Middle East & North Africa", "Sub-Saharan Africa" | 0 |
| `income_group` | String | World Bank income classification | "High income", "Upper middle income", "Lower middle income", "Low income" | 0 |
| `year` | Float | Calendar year of observation | 1971–2026 (56 unique values) | 0 |
| `school_enrollment,_primary_%_gross` | Float | Primary education gross enrollment rate (%) | 0–150+% | 110 (4.8%) |
| `school_enrollment,_secondary_%_gross` | Float | Secondary education gross enrollment rate (%) | 0–150+% | 614 (26.7%) |
| `school_enrollment,_tertiary_%_gross` | Float | Tertiary education gross enrollment rate (%) | 0–50+% | 790 (34.3%) |

#### Notes
- Gross enrollment rates can exceed 100% due to over-age and under-age students
- Missing values indicate data unavailability for that country-year combination
- Primary data has highest completeness; tertiary data has significant gaps

---

### 2. `primary_education_africa_cleaned.csv`
**Primary Education Dataset**

- **Rows:** 2,193
- **Columns:** 10
- **Description:** Primary-level education enrollment data with education level explicitly marked

#### Fields

| Field | Type | Description | Values/Range | Missing |
|-------|------|-------------|--------------|---------|
| Country/Government/Code/Region/Income Group | *Same as above* | *Same as above* | *Same as above* | 0 |
| `education_level` | String | Education level classification | "Primary" (constant) | 0 |
| `school_enrollment,_primary_%_gross` | Float | Primary education enrollment rate (%) | 0–150+% | 0 |
| `school_enrollment,_secondary_%_gross` | Float | Secondary enrollment rate | N/A | 2,193 (100%) |
| `school_enrollment,_tertiary_%_gross` | Float | Tertiary enrollment rate | N/A | 2,193 (100%) |

#### Notes
- All records have education_level = "Primary"
- Secondary and tertiary columns are entirely missing (by design)
- No missing values for countries: 51 countries included (one country removed from combined dataset)

---

### 3. `secondary_education_africa_cleaned.csv`
**Secondary Education Dataset**

- **Rows:** 1,689
- **Columns:** 10
- **Description:** Secondary-level education enrollment data

#### Fields

| Field | Type | Description | Values/Range | Missing |
|-------|------|-------------|--------------|---------|
| Country/Government/Code/Region/Income Group | *Same as above* | *Same as above* | *Same as above* | 0 |
| `education_level` | String | Education level classification | "Secondary" (constant) | 0 |
| `school_enrollment,_primary_%_gross` | Float | Primary enrollment rate | N/A | 1,689 (100%) |
| `school_enrollment,_secondary_%_gross` | Float | Secondary education enrollment rate (%) | 0–150+% | 0 |
| `school_enrollment,_tertiary_%_gross` | Float | Tertiary enrollment rate | N/A | 1,689 (100%) |

#### Notes
- All records have education_level = "Secondary"
- Primary and tertiary columns are entirely missing (by design)
- Only includes country-year combinations with non-null secondary data
- 51 countries included

---

### 4. `tertiary_education_africa_cleaned.csv`
**Tertiary Education Dataset**

- **Rows:** 1,513
- **Columns:** 10
- **Description:** Tertiary-level education enrollment data

#### Fields

| Field | Type | Description | Values/Range | Missing |
|-------|------|-------------|--------------|---------|
| Country/Government/Code/Region/Income Group | *Same as above* | *Same as above* | *Same as above* | 0 |
| `education_level` | String | Education level classification | "Tertiary" (constant) | 0 |
| `school_enrollment,_primary_%_gross` | Float | Primary enrollment rate | N/A | 1,513 (100%) |
| `school_enrollment,_secondary_%_gross` | Float | Secondary enrollment rate | N/A | 1,513 (100%) |
| `school_enrollment,_tertiary_%_gross` | Float | Tertiary education enrollment rate (%) | 0–50+% | 0 |

#### Notes
- All records have education_level = "Tertiary"
- Primary and secondary columns are entirely missing (by design)
- Only includes country-year combinations with non-null tertiary data
- 51 countries included
- Lowest coverage: 1,513 records compared to 2,193 for primary

---

## Variables Across All Datasets

### Country Characteristics

**`government`** (10 unique values)
- parliamentary republic
- parliamentary unitary constitutional monarchy
- presidential federal republic
- semi-presidential republic
- semi-presidential unitary republic
- *(and 5 other variants)*

**`region`** (2 values)
- Middle East & North Africa
- Sub-Saharan Africa

**`income_group`** (4 values)
- High income
- Upper middle income
- Lower middle income
- Low income

### Enrollment Metrics

All enrollment metrics are **gross enrollment rates** (%):
- Definition: Total enrollment at a specific education level, regardless of age, divided by eligible population
- Range: Typically 0–100%, but can exceed 100% due to over-age or under-age enrollment
- Unit: Percentage (%)
- Source: World Bank World Development Indicators

---

## Data Quality Notes

### Completeness by Education Level
| Level | Records | Coverage |
|-------|---------|----------|
| Primary | 2,193 | 95.3% |
| Secondary | 1,689 | 73.3% |
| Tertiary | 1,513 | 65.7% |

### Geographic Coverage
- **Countries:** 51–52 African countries (including Middle East & North Africa region)
- **Year Range:** 1971–2026 (56 years)
- **Regions:** Evenly split between Sub-Saharan Africa and Middle East & North Africa

### Data Integrity
- No missing values in demographic dimensions (country, government, region, income_group, year)
- Missing values occur only in enrollment metrics, reflecting actual data gaps
- Years are complete for all countries included

---

## Relationships Between Datasets

```
education_africa_cleaned (Combined)
├── Contains all country-year-level combinations with available data
├── Superset of all three level-specific datasets
└── May include records where only one education level is available

primary_education_africa_cleaned
├── Subset of education_africa_cleaned
├── Filter: education_level = "Primary"
└── 2,193 unique country-year combinations

secondary_education_africa_cleaned
├── Subset of education_africa_cleaned
├── Filter: education_level = "Secondary"
└── 1,689 unique country-year combinations

tertiary_education_africa_cleaned
├── Subset of education_africa_cleaned
├── Filter: education_level = "Tertiary"
└── 1,513 unique country-year combinations
```

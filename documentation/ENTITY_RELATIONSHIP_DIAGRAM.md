# Entity-Relationship Diagram

## ER Diagram (ASCII)

```
┌─────────────────────────────────────────┐
│         Country Dimension               │
├─────────────────────────────────────────┤
│ Primary Key:  country_code              │
├─────────────────────────────────────────┤
│ • country (String)                      │
│ • country_code (String, ISO 3166-1)     │
│ • government (String)                   │
│ • region (String)                       │
│ • income_group (String)                 │
└────────────────┬────────────────────────┘
                 │
                 │ 1..N (country_code FK)
                 │
    ┌────────────┴──────────────┐
    │                           │
    ▼                           ▼
┌──────────────────────┐  ┌──────────────────────┐
│  Education Fact      │  │ Time Dimension       │
│  Table (Combined)    │  ├──────────────────────┤
├──────────────────────┤  │ Primary Key: year    │
│ Foreign Keys:        │  ├──────────────────────┤
│ • country_code (FK)  │──│ • year (Float)       │
│ • year (FK)          │──│                      │
├──────────────────────┤  └──────────────────────┘
│ Metrics:             │
│ • primary_enroll (%)  │
│ • secondary_enroll(%) │
│ • tertiary_enroll (%) │
└──────────────────────┘
         │
         │ Can be split into:
    ┌────┼────┬─────────────┐
    │    │    │             │
    ▼    ▼    ▼             ▼
┌─────────┐ ┌──────────┐ ┌──────────┐
│Primary  │ │Secondary │ │ Tertiary │
│Dataset  │ │ Dataset  │ │ Dataset  │
├─────────┤ ├──────────┤ ├──────────┤
│education│ │education │ │education │
│_level:  │ │_level:   │ │_level:   │
│Primary  │ │Secondary │ │Tertiary  │
│+ 1 enr. │ │+ 1 enr.  │ │+ 1 enr.  │
│metric   │ │metric    │ │metric    │
└─────────┘ └──────────┘ └──────────┘
```

## Relational Schema

### Dimension Tables

#### Country Dimension
```
COUNTRY
├── country_code (PRIMARY KEY)
├── country
├── government
├── region
└── income_group
```

#### Time Dimension
```
TIME
├── year (PRIMARY KEY)
```

#### Education Level Dimension
```
EDUCATION_LEVEL
├── education_level (PRIMARY KEY)
│   └── Values: "Primary", "Secondary", "Tertiary"
```

### Fact Tables

#### Education Facts (Combined Dataset)
```
EDUCATION_FACTS
├── country_code (FOREIGN KEY → COUNTRY)
├── year (FOREIGN KEY → TIME)
├── school_enrollment_primary_pct_gross
├── school_enrollment_secondary_pct_gross
└── school_enrollment_tertiary_pct_gross
```

#### Primary Education Facts
```
PRIMARY_EDUCATION_FACTS
├── country_code (FOREIGN KEY → COUNTRY)
├── year (FOREIGN KEY → TIME)
├── education_level: "Primary"
├── school_enrollment_primary_pct_gross
├── school_enrollment_secondary_pct_gross (null)
└── school_enrollment_tertiary_pct_gross (null)
```

#### Secondary Education Facts
```
SECONDARY_EDUCATION_FACTS
├── country_code (FOREIGN KEY → COUNTRY)
├── year (FOREIGN KEY → TIME)
├── education_level: "Secondary"
├── school_enrollment_primary_pct_gross (null)
├── school_enrollment_secondary_pct_gross
└── school_enrollment_tertiary_pct_gross (null)
```

#### Tertiary Education Facts
```
TERTIARY_EDUCATION_FACTS
├── country_code (FOREIGN KEY → COUNTRY)
├── year (FOREIGN KEY → TIME)
├── education_level: "Tertiary"
├── school_enrollment_primary_pct_gross (null)
├── school_enrollment_secondary_pct_gross (null)
└── school_enrollment_tertiary_pct_gross
```

## Data Structure Overview

### Star Schema

The datasets follow a **star schema** pattern with:

- **Fact tables** containing enrollment metrics
- **Dimension tables** containing country attributes and time periods
- **Level-specific tables** separating education levels for specialized analysis

### Cardinality Relationships

| Relationship | Cardinality | Notes |
|---|---|---|
| Country → Years | 1:N | Each country has multiple years of data (up to 56) |
| Year → Countries | 1:N | Each year has data for multiple countries |
| Education Level → Countries | 1:N | Each education level has data for multiple countries |
| Education Level → Years | 1:N | Each education level has multiple years of data |

### Key Statistics

| Dimension | Count | Notes |
|---|---|---|
| Countries | 51–52 | Varies by dataset |
| Years | 56 | 1971–2026 |
| Education Levels | 3 | Primary, Secondary, Tertiary |
| Country-Year Combos (Combined) | 2,303 | Max possible: 52 × 56 = 2,912 |
| Country-Year Combos (Primary) | 2,193 | 75.4% of maximum |
| Country-Year Combos (Secondary) | 1,689 | 58.1% of maximum |
| Country-Year Combos (Tertiary) | 1,513 | 52.0% of maximum |

## Dataset Hierarchy

```
education_africa_cleaned (Full Dataset)
│
├─ Contains: All country-year records with any education level data
├─ Size: 2,303 rows
└─ Structure: Unnormalized (all education levels in one row)
    │
    ├─ Subset: primary_education_africa_cleaned
    │  ├─ Filter: WHERE education_level = 'Primary'
    │  ├─ Size: 2,193 rows
    │  └─ Coverage: ~95% of country-years
    │
    ├─ Subset: secondary_education_africa_cleaned
    │  ├─ Filter: WHERE education_level = 'Secondary'
    │  ├─ Size: 1,689 rows
    │  └─ Coverage: ~73% of country-years
    │
    └─ Subset: tertiary_education_africa_cleaned
       ├─ Filter: WHERE education_level = 'Tertiary'
       ├─ Size: 1,513 rows
       └─ Coverage: ~65% of country-years
```

## Attribute Hierarchies

### Geographic Hierarchy
```
Region (2 levels)
├── Middle East & North Africa
│   └── Countries (variable: 20-25 countries)
│       └── Government Types (variable)
│
└── Sub-Saharan Africa
    └── Countries (variable: 26-31 countries)
        └── Government Types (variable)
```

### Economic Hierarchy
```
Income Group (4 levels)
├── High Income
├── Upper Middle Income
├── Lower Middle Income
└── Low Income
```

### Temporal Hierarchy
```
Year (1971-2026)
├── Decades
│   ├── 1970s, 1980s, 1990s, etc.
│   └── Can be aggregated for trend analysis
└── Individual Years (56 unique values)
```

## Integration Points

### Common Keys Across Datasets

| Key | Data Type | Used For |
|---|---|---|
| country_code | String (ISO 3166-1) | Joining across datasets |
| country | String | Display/filtering |
| year | Float | Time-based filtering/joining |

### Joins Between Datasets

**Primary ↔ Secondary**
```
ON primary.country_code = secondary.country_code
AND primary.year = secondary.year
```

**Primary ↔ Tertiary**
```
ON primary.country_code = tertiary.country_code
AND primary.year = tertiary.year
```

**Any Level-Specific ← Combined Dataset**
```
WHERE education_level IN ('Primary', 'Secondary', 'Tertiary')
```

## Notes on Norma lization

- **Current State:** Partially denormalized (education levels separated into different tables)
- **Rationale:** Separating by education level improves query clarity for level-specific analysis
- **Trade-off:** Introduces redundancy for country and temporal attributes across tables
- **Recommendation:** Use combined dataset for cross-level analysis; use level-specific datasets for focused studies

# Bassmaster Tournament Data Scraper - Complete Package

## What You Have

1. **bassmaster_all_tournaments.csv** - List of all 150 tournaments (2011-2025) with winners  
2. **scrape_bassmaster_complete.py** - Python script to get ALL detailed results for all tournaments
3. **README.md** - This file with instructions

## What the Scraper Will Get

The scraper will visit each tournament detail page and extract:

- **Place** - Finishing position (1st, 2nd, 3rd, etc.)
- **Angler** - Angler's name
- **Angler ID** - Unique ID for each angler
- **Fish** - Number of bass caught
- **Weight (oz)** - Total weight in ounces
- **Big Bag** - Heaviest single day catch (if applicable)
- **Big Bass** - Largest individual bass (if applicable)  
- **Leader Bonus** - Bonus points for leading
- **Fantasy Points** - Points earned in fantasy fishing

Plus tournament details:
- Tournament name
- Year
- Date
- Site/Lake
- State

## Setup Instructions

### 1. Install Python
Make sure you have Python 3.7+ installed.

### 2. Install Required Packages
```bash
pip install beautifulsoup4 requests
```

### 3. Run the Scraper
```bash
python scrape_bassmaster_complete.py
```

## What Happens

The script will:
1. Read the 150 tournaments from `bassmaster_all_tournaments.csv`
2. Visit each tournament's detail page (e.g., `https://bassmasterfantasy.com/TournamentDetails.aspx?periodId=10&year=2025`)
3. Extract data for ALL anglers (typically 50-100+ per tournament)
4. Save individual CSV files per tournament in `tournament_results/` folder
5. Create a master CSV `bassmaster_all_detailed_results.csv` with ALL anglers from ALL tournaments

## Expected Results

- **Total tournaments**: 150
- **Expected total anglers**: ~10,000-15,000 angler results across all tournaments
- **Runtime**: 2-3 minutes (0.5 second delay between requests to be respectful)

## Output Files

After running, you'll have:

```
bassmaster_all_detailed_results.csv  (Master file with all data)
tournament_results/
  ├── 2025_Bassmaster_Elite_at_Mississippi_River.csv
  ├── 2025_Bassmaster_Elite_at_Lake_St_Clair.csv
  ├── 2024_Bassmaster_Elite_at_St_Lawrence_River.csv
  └── ... (150 total files)
```

## CSV Format

Each CSV will have these columns:

```csv
tournament,year,date,site,state,place,angler,angler_id,fish,weight_oz,big_bag,big_bass,leader_bonus,fantasy_points
```

Example row:
```csv
2025 Bassmaster Elite at Mississippi River,2025,August 21-24 2025,Mississippi River,WI,1,Pat Schlapper,440,20,1061,,5,305
```

## Data Analysis Ideas

With this comprehensive dataset, you can:

- **Performance analysis**: Track angler performance over time
- **Lake/site analysis**: Which lakes produce the biggest catches?
- **Seasonal patterns**: When do anglers catch more/bigger bass?
- **Consistency metrics**: Which anglers are most consistent?
- **Predictive modeling**: Build models to predict tournament outcomes
- **Big bass analysis**: Who catches the biggest fish and where?
- **Weight trends**: Are average weights increasing or decreasing over time?

## Troubleshooting

### Script runs but no results
- Check your internet connection
- The website might be temporarily down
- Rate limiting - try increasing the sleep time in the script

### Some tournaments fail
- Normal - some older tournaments may have different page structures
- The script will continue and report success/failure counts

### Want more data?
The TournamentDetails pages show summary stats. For daily weights (Day 1, Day 2, etc.), you may need to look for additional pages or endpoints on the Bassmaster Fantasy site.

## Next Steps

1. Run the scraper to get all the data
2. Load the master CSV into your analysis tool (Python pandas, R, Excel, etc.)
3. Start exploring the data!
4. Build visualizations and statistical models

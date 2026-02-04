#!/usr/bin/env python3
"""
Bassmaster Fantasy - Comprehensive Tournament Results Scraper
Extracts ALL anglers and their detailed stats from all tournaments
"""

import csv
import re
import time
from pathlib import Path

# For the actual scraping
try:
    import requests
    from bs4 import BeautifulSoup
    SCRAPING_AVAILABLE = True
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'beautifulsoup4', 'requests', '--break-system-packages'])
    import requests
    from bs4 import BeautifulSoup
    SCRAPING_AVAILABLE = True

def fetch_tournament_details(url):
    """Fetch tournament detail page"""
    try:
        print(f"    Fetching: {url}")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"    ⚠ Error: {e}")
        return None

def parse_tournament_results(html, tournament_info):
    """Parse tournament results from the HTML table"""
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    
    # Find the table with tournament results
    # The table has headers: Place, Angler, Fish, Weight (oz), Big Bag, Big Bass, Leader Bonus, Fantasy Points
    tables = soup.find_all('table')
    
    for table in tables:
        headers = table.find_all('th')
        if not headers:
            continue
        
        # Check if this is the results table
        header_text = [h.get_text(strip=True).lower() for h in headers]
        if 'place' in header_text and 'angler' in header_text:
            print(f"    ✓ Found results table")
            
            # Parse each row
            rows = table.find_all('tr')[1:]  # Skip header row
            for row in rows:
                cells = row.find_all('td')
                if len(cells) < 8:  # Need all columns
                    continue
                
                try:
                    # Extract angler name from the link
                    angler_cell = cells[1]
                    angler_link = angler_cell.find('a')
                    angler_name = angler_link.get_text(strip=True) if angler_link else angler_cell.get_text(strip=True)
                    
                    # Get angler ID from the link if available
                    angler_id = ''
                    if angler_link and 'playerId=' in angler_link.get('href', ''):
                        angler_id = re.search(r'playerId=(\d+)', angler_link['href']).group(1)
                    
                    result = {
                        'tournament': tournament_info['Tournament'],
                        'year': tournament_info['Year'],
                        'date': tournament_info['Date'],
                        'site': tournament_info['Site'],
                        'state': tournament_info['State'],
                        'place': cells[0].get_text(strip=True),
                        'angler': angler_name,
                        'angler_id': angler_id,
                        'fish': cells[2].get_text(strip=True),
                        'weight_oz': cells[3].get_text(strip=True),
                        'big_bag': cells[4].get_text(strip=True),
                        'big_bass': cells[5].get_text(strip=True),
                        'leader_bonus': cells[6].get_text(strip=True),
                        'fantasy_points': cells[7].get_text(strip=True),
                    }
                    results.append(result)
                    
                except Exception as e:
                    print(f"    ⚠ Error parsing row: {e}")
                    continue
            
            print(f"    ✓ Extracted {len(results)} anglers")
            break
    
    return results

def scrape_all_tournaments():
    """Main function to scrape all tournaments"""
    
    # Read tournament list
    tournaments_file = 'bassmaster_all_tournaments.csv'
    if not Path(tournaments_file).exists():
        print(f"Error: {tournaments_file} not found!")
        return
    
    with open(tournaments_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        tournaments = list(reader)
    
    print(f"\n{'='*80}")
    print(f"BASSMASTER COMPREHENSIVE SCRAPER - ALL TOURNAMENT DETAILS")
    print(f"{'='*80}")
    print(f"Found {len(tournaments)} tournaments to scrape\n")
    
    # Create output directory
    output_dir = Path('tournament_results')
    output_dir.mkdir(exist_ok=True)
    
    all_results = []
    successful = 0
    failed = 0
    
    for i, tournament in enumerate(tournaments, 1):
        print(f"\n[{i}/{len(tournaments)}] {tournament['Tournament']}")
        
        if not tournament.get('Tournament_URL'):
            print("    ⚠ No URL, skipping")
            failed += 1
            continue
        
        # Fetch the page
        html = fetch_tournament_details(tournament['Tournament_URL'])
        if not html:
            failed += 1
            continue
        
        # Parse results
        results = parse_tournament_results(html, tournament)
        
        if results:
            successful += 1
            
            # Save individual tournament file
            year = tournament['Year']
            tournament_slug = re.sub(r'[^\w\s-]', '', tournament['Tournament']).strip().replace(' ', '_')
            output_file = output_dir / f"{year}_{tournament_slug}.csv"
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
            
            all_results.extend(results)
        else:
            print(f"    ⚠ No results extracted")
            failed += 1
        
        # Be respectful - wait between requests
        time.sleep(0.5)
    
    # Save master combined file
    if all_results:
        master_file = 'bassmaster_all_detailed_results.csv'
        with open(master_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
            writer.writeheader()
            writer.writerows(all_results)
        
        print(f"\n{'='*80}")
        print(f"SCRAPING COMPLETE!")
        print(f"{'='*80}")
        print(f"✓ Successfully scraped: {successful} tournaments")
        print(f"✗ Failed: {failed} tournaments")
        print(f"✓ Total angler results: {len(all_results):,}")
        print(f"\nOutput files:")
        print(f"  - Master file: {master_file}")
        print(f"  - Individual files: {output_dir}/")
        print(f"\nData fields in each row:")
        if all_results:
            for key in all_results[0].keys():
                print(f"  - {key}")
    else:
        print(f"\n⚠ No results scraped!")

if __name__ == "__main__":
    scrape_all_tournaments()

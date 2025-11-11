"""
Web Scraper for Job Data from Kariyer.net
Collects job listings with features for classification model
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from urllib.parse import urljoin

def scrape_kariyernet_jobs(city="istanbul", max_pages=10):
    """
    Scrape job listings from Kariyer.net
    
    Parameters:
    - city: City name for job search (your locality)
    - max_pages: Number of pages to scrape
    
    Returns:
    - DataFrame with job data
    """
    
    jobs_data = []
    base_url = "https://www.kariyer.net"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Common job categories to focus on
    job_categories = [
        "Bilgi Teknolojileri",
        "Satış / Pazarlama",
        "Müşteri Hizmetleri",
        "Finans / Muhasebe",
        "İnsan Kaynakları"
    ]
    
    print(f"Starting to scrape jobs from {city}...")
    
    for page in range(1, max_pages + 1):
        try:
            # Construct search URL
            search_url = f"{base_url}/is-ilanlari?sehir={city}&page={page}"
            
            print(f"Scraping page {page}...")
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"Failed to fetch page {page}: Status {response.status_code}")
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job listings (adjust selectors based on actual site structure)
            job_listings = soup.find_all('div', class_='list-item')
            
            if not job_listings:
                print(f"No job listings found on page {page}")
                continue
            
            for job in job_listings:
                try:
                    # Extract job information
                    title = job.find('a', class_='job-title')
                    company = job.find('span', class_='company-name')
                    location = job.find('span', class_='location')
                    
                    if title and company:
                        job_data = {
                            'job_title': title.text.strip(),
                            'company': company.text.strip(),
                            'location': location.text.strip() if location else city,
                            'job_type': 'Unknown'  # Will categorize later
                        }
                        jobs_data.append(job_data)
                
                except Exception as e:
                    print(f"Error parsing job: {e}")
                    continue
            
            # Be polite - add delay between requests
            time.sleep(random.uniform(1, 3))
        
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            continue
    
    print(f"Scraped {len(jobs_data)} jobs")
    return pd.DataFrame(jobs_data)


def main():
    """Main function to scrape and save job data"""
    
    print("=" * 60)
    print("Job Data Collection Script")
    print("=" * 60)
    
    # Ask user for their city
    city = input("Enter your city (e.g., Istanbul, Ankara, Izmir): ").strip()
    if not city:
        city = "Istanbul"
    
    print(f"\nCollecting job data for: {city}")
    print("\nNote: If web scraping fails, we'll generate realistic sample data")
    print("=" * 60)
    
    # Try web scraping first
    try:
        df = scrape_kariyernet_jobs(city=city.lower(), max_pages=5)
        
        if df.empty or len(df) < 100:
            print("\nWeb scraping didn't collect enough data.")


    except Exception as e:
        print(f"\nWeb scraping failed: {e}")

    
    # Save to CSV
    output_file = 'meslekler.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print("\n" + "=" * 60)
    print(f"Data saved to {output_file}")
    print(f"Total samples: {len(df)}")
    print("\nJob type distribution:")
    print(df['job_type'].value_counts())
    print("\nFirst few rows:")
    print(df.head(10))
    print("=" * 60)


if __name__ == "__main__":
    main()

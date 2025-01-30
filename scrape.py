import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import os

BASE_URL = "https://anilschool.weebly.com/"
OUTPUT_DIR = "scraped_data"

def get_all_pages():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all navigation links
    nav_links = soup.select('.wsite-menu-default a')
    pages = set()
    
    for link in nav_links:
        href = link.get('href')
        if href and not href.startswith('http'):
            full_url = urljoin(BASE_URL, href)
            pages.add(full_url)
    
    return list(pages)

def scrape_page(url):
    print(f"Scraping: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract page title
    title = soup.find('h1', class_='wsite-content-title').get_text(strip=True) if soup.find('h1', class_='wsite-content-title') else "Untitled"
    
    # Extract main content
    sections = []
    for section in soup.select('.wsite-content'):
        for elem in section.children:
            if elem.name == 'h2':
                sections.append({
                    'type': 'heading',
                    'content': elem.get_text(strip=True)
                })
            elif elem.name == 'div' and 'paragraph' in elem.get('class', []):
                sections.append({
                    'type': 'text',
                    'content': elem.get_text(strip=True, separator='\n')
                })
            elif elem.name == 'div' and 'wsite-image' in elem.get('class', []):
                img = elem.find('img')
                if img:
                    sections.append({
                        'type': 'image',
                        'src': img.get('src'),
                        'alt': img.get('alt', '')
                    })
    
    # Extract staff members (if available)
    staff = []
    if 'overview' in url:
        for img in soup.select('.wsite-image div img'):
            member = {
                'name': img.get('alt', '').strip(),
                'image': urljoin(BASE_URL, img.get('src'))
            }
            next_para = img.find_parent().find_next_sibling('p')
            if next_para:
                member['role'] = next_para.get_text(strip=True)
            staff.append(member)
    
    # Debugging print to verify extracted data
    print(f"Title: {title}")
    print(f"Sections: {json.dumps(sections, indent=2)}")
    print(f"Staff: {json.dumps(staff, indent=2)}")
    
    return {
        'url': url,
        'title': title,
        'sections': sections,
        'staff': staff
    }

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_data = []
    
    pages = get_all_pages()
    for page_url in pages:
        page_data = scrape_page(page_url)
        all_data.append(page_data)
    
    with open(os.path.join(OUTPUT_DIR, 'website_data.json'), 'w') as f:
        json.dump(all_data, f)
    
    print(f"Scraped {len(pages)} pages. Data saved to {OUTPUT_DIR}/website_data.json")

if __name__ == "__main__":
    main()

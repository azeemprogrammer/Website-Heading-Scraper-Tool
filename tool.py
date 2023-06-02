import csv
import requests
from bs4 import BeautifulSoup

def scrape_headings(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    headings = set()  # Use a set to store unique headings
    for tag in soup.find_all(['h2', 'h3', 'h4']):
        heading_text = tag.get_text().strip()
        if heading_text not in headings:  # Check for duplicates
            headings.add(heading_text)

    return headings

def combine_headings(urls):
    all_headings = set()  # Use a set to store unique headings
    for url in urls:
        headings = scrape_headings(url)
        all_headings.update(headings)  # Use 'update' method to merge sets

    return all_headings

def save_to_csv(headings, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Headings'])
        writer.writerows(zip(headings))

# Example usage
article_urls = input("Enter the URLs (comma-separated): ").split(',')
combined_headings = combine_headings(article_urls)

csv_filename = input("Enter the CSV filename to save the headings: ")
save_to_csv(combined_headings, csv_filename)

print(f"Headings saved to {csv_filename} successfully.")

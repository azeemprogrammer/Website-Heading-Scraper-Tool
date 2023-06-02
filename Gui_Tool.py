import csv
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog, messagebox

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

def browse_files():
    filenames = filedialog.askopenfilenames()
    entry_urls.delete(1.0, tk.END)
    entry_urls.insert(tk.END, ', '.join(filenames))

def scrape_and_save():
    urls = entry_urls.get(1.0, tk.END).strip().split(',')
    csv_filename = entry_csv_filename.get().strip()

    if not urls or not csv_filename:
        messagebox.showerror('Error', 'Please provide URLs and CSV filename.')
        return

    try:
        combined_headings = combine_headings(urls)
        save_to_csv(combined_headings, csv_filename)
        messagebox.showinfo('Success', f'Headings saved to {csv_filename} successfully.')
    except:
        messagebox.showerror('Error', 'An error occurred while scraping and saving headings.')

# Create the main window
window = tk.Tk()
window.title("Website Heading Scraper Tool By Prog Expo")

# Create and place the URL input label and text area
label_urls = tk.Label(window, text="Enter the URLs (comma-separated):")
label_urls.pack()
entry_urls = tk.Text(window, height=5)
entry_urls.pack()



# Create and place the CSV filename input label and entry field
label_csv_filename = tk.Label(window, text="Enter the CSV filename headings.csv:")
label_csv_filename.pack()
entry_csv_filename = tk.Entry(window)
entry_csv_filename.pack()

# Create and place the Browse button
button_browse = tk.Button(window, text="Browse", command=browse_files)
button_browse.pack()

# Create and place the Scrape and Save button
button_scrape_save = tk.Button(window, text="Scrape and Save", command=scrape_and_save)
button_scrape_save.pack()

# Run the main event loop
window.mainloop()

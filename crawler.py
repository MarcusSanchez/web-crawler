import requests
from bs4 import BeautifulSoup
import os
from collections import deque
from urllib.parse import urljoin


def clean_text(text):
    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    # Remove empty lines and ensure maximum one empty line between content
    cleaned_lines = []
    prev_line_empty = False
    for line in lines:
        if line or not prev_line_empty:
            cleaned_lines.append(line)
            prev_line_empty = (line == '')
    return '\n'.join(cleaned_lines)


def crawl(start_url, substring):
    queue = deque([start_url])
    visited = set()

    temp_file_path = os.path.join(os.getcwd(), 'crawl_results.txt')

    with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
        while queue:
            url = queue.popleft()
            if url in visited:
                continue

            visited.add(url)

            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                # Save content to the temp file with URL as comment
                content = clean_text(soup.get_text())
                temp_file.write(f"### {url} ###\n\n{content}\n\n")
                print(f"Content from {url} saved to {temp_file_path}")

                # Find links and add to queue
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(url, href)
                    if full_url.startswith(substring):
                        queue.append(full_url)

            except Exception as e:
                print(f"Error crawling {url}: {e}")

    print("Crawling complete")
    print(f"All content saved to {temp_file_path}")

    # Final cleanup of the entire file
    with open(temp_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    cleaned_content = clean_text(content)

    with open(temp_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

    print("File cleanup complete")


# Example usage
start_url = "https://example.com"
substring = "https://example.com/"  # Only crawl URLs that start with this substring
crawl(start_url, substring)

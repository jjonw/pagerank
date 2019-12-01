import os

from bs4 import BeautifulSoup


def get_links_to(file):
    """
    Returns where page points to
    """
    with open(file, "rb") as f:
        page = f.read()

    page_soup = BeautifulSoup(page, "html.parser")

    links = []
    for page in page_soup.find_all('a', href = True):
        links.append(page['href'])

    return links

def parse_files(pages_directory):
    pages_directory = os.path.join(os.getcwd(), pages_directory)
    nodes = []
    edges = []
    
    for path, dirs, files in os.walk(pages_directory):
        for file in files:
            abs_file = os.path.join(path, file)
            filename = file.replace('.html', '')
            nodes.append(filename)

            # For each edge builds a link between nodes 
            every_edge = get_links_to(abs_file)
            for edge in every_edge:
                e = edge.replace('.html', '')
                edges.append([filename, e])

    return nodes, edges
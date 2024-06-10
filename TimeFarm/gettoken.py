import urllib.parse

def extract_tgWebAppData(url):
    parsed_url = urllib.parse.urlparse(url)
    fragment = parsed_url.fragment
    parsed_fragment = urllib.parse.parse_qs(fragment)
    if 'tgWebAppData' in parsed_fragment:
        tgWebAppData = parsed_fragment['tgWebAppData'][0]
        return tgWebAppData
    else:
        return None

# Open both output files
with open('tokens.txt', 'w') as tokens_file, open('tokens_timefarm.txt', 'w') as tokens_blum_file:
    with open('urls.txt', 'r') as file:
        for line in file:
            url = line.strip()
            tgWebAppData = extract_tgWebAppData(url)
            if tgWebAppData:
                # Write to both files
                tokens_file.write(f"{tgWebAppData}\n")
                tokens_blum_file.write(f"{tgWebAppData}\n")
            else:
                # Write error to both files
                tokens_file.write(f"Error {url}\n")
                tokens_blum_file.write(f"Error {url}\n")

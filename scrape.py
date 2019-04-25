#!/usr/bin/env python3

import requests
import sys
import csv
from bs4 import BeautifulSoup


def main():
    fieldnames = ["location", "year", "grantee", "description", "amount", "term", "program"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    url_pattern = "https://www.publicwelfare.org/grants/?pagenum={}"

    for i in range(1, 68):
        url = url_pattern.format(i)
        print("Downloading " + url, file=sys.stderr)
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 '
                                              '(X11; Linux x86_64) AppleWebKit/537.36 '
                                              '(KHTML, like Gecko) '
                                              'Chrome/63.0.3239.132 Safari/537.36'})
        soup = BeautifulSoup(response.content, "lxml")
        for grant in soup.find_all("li", {"class": "grant_items"}):
            location_date = grant.find("div", {"class": "grant-heading"}).text
            grantee = grant.h2.text
            description = grant.find("div", {"class": "excerpt"}).text
            amount = grant.find("div", {"class": "grant-amount"}).text
            term = grant.find("div", {"class": "grant-term"}).text
            program = grant.find("div", {"class": "grant-program"}).text
            writer.writerow({
                "location": location_date.split("//")[0].strip(),
                "year": location_date.split("//")[1].strip(),
                "grantee": grantee,
                "description": description,
                "amount": amount,
                "term": term,
                "program": program,
            })


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import csv
import sys
import re

import pdb

from proc import CAUSE_AREAS, CAUSE_AREA_URLS

def main():
    with open(sys.argv[1], newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        print("""insert into donations (donor, donee, amount, donation_date, donation_date_precision, donation_date_basis, cause_area, donor_cause_area_url, url, notes, affected_countries, affected_regions) values""")
        first = True

        for row in reader:
            assert row["amount"].startswith("$")
            amount = row["amount"].replace("$", "").replace(",", "")

            location = row["location"]
            # Having this pattern means we're basically dealing just with "City
            # Name, STATE CODE" instances. This means we don't have to check for
            # multiple locations, so no need to separate by pipes.
            if location == "Los Angeles":
                location = "Los Angeles, CA"
            assert location == "" or re.match(r"[A-Za-z. ]+, [A-Z][A-Z]", location), location

            cause_area = CAUSE_AREAS[row["program"]]
            cause_area_url = CAUSE_AREA_URLS[row["program"]]

            notes = "Term: " + row["term"] + ". " + row["description"]
            print(("    " if first else "    ,") + "(" + ",".join([
                mysql_quote("Public Welfare Foundation"),  # donor
                mysql_quote(row["grantee"]),  # donee
                str(amount),  # amount
                mysql_quote(row["year"] + "-01-01"),  # donation_date
                mysql_quote("year"),  # donation_date_precision
                mysql_quote("donation log"),  # donation_date_basis
                mysql_quote(cause_area),  # cause_area
                mysql_quote(cause_area_url),  # donor_cause_area_url
                mysql_quote("https://www.publicwelfare.org/grants/"),  # url
                mysql_quote(notes),  # notes
                mysql_quote("United States"),  # affected_countries
                mysql_quote(location),  # affected_regions
            ]) + ")")
            first = False
        print(";")

def mysql_quote(x):
    """Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    our input is fixed and from a basically trustable source."""
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)

if __name__ == "__main__":
    main()

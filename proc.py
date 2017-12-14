#!/usr/bin/env python3

from bs4 import BeautifulSoup

def main():
    with open("data.html", "r") as f:
        soup = BeautifulSoup(f, "lxml")

    first = True

    for grant in soup.find_all("div", {"class": "grant-single"}):
        # These are just the div tags; what we want is broken down into futher
        # parts inside. Each grant looks like this:
        #   <div class="grant-single">
        #     <div class="grant-single-grantee">
        #       <h4>National Public Radio</h4>
        #       <p>Washington, DC</p>
        #       <p>Support for coverage of workers' rights and other labor
        #       issues.</p>
        #     </div>
        #     <div class="grant-single-amount">
        #       <p>$200,000</p>
        #       <p>Term: 24 months</p>
        #     </div>
        #     <div class="grant-single-year">
        #       2018
        #     </div>
        #     <div class="grant-single-program">
        #       Workers' Rights
        #     </div>
        #     <div class="breakcollapse"></div>
        #   </div>
        grantee = grant.find("div", {"class": "grant-single-grantee"})
        grant_amount = grant.find("div", {"class": "grant-single-amount"})
        year = grant.find("div", {"class": "grant-single-year"})
        program = grant.find("div", {"class": "grant-single-program"})

        donee = grantee.find("h4").text
        notes = grantee.find_all("p")[1].text

        amount, term = grant_amount.find_all("p")
        amount = amount.text.replace("$", "").replace(",", "")
        term = term.text
        assert term.startswith("Term: ")
        term = term[len("Term: "):]

        donation_date = year.text + "-01-01"

        print(("    " if first else "    ,") + "(" + ",".join([
            donee,
            amount,
            term,
            donation_date,
            notes
        ]) + ")")
        first = False


if __name__ == "__main__":
    main()

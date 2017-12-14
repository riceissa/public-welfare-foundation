#!/usr/bin/env python3

from bs4 import BeautifulSoup


# Maps Public Welfare Foundation's cause terminology to Donations List
# Website's
CAUSE_AREAS = {
        "Criminal Justice": "Criminal justice reform",
        "President's Discretionary Fund": "FIXME",
        "Special Initiative: Civil Legal Aid": "FIXME",
        "Special Opportunities": "FIXME",
        "Workers' Rights": "FIXME",
        "Youth Justice": "FIXME",
        }

def mysql_quote(x):
    '''
    Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    whatever; our input is fixed and from a basically trustable source..
    '''
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)


def main():
    with open("data.html", "r") as f:
        soup = BeautifulSoup(f, "lxml")

    first = True

    print("""insert into donations (donor, donee, amount, donation_date,
    donation_date_precision, donation_date_basis, cause_area, url,
    donor_cause_area_url, notes, affected_countries,
    affected_regions) values""")

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

        cause_area = CAUSE_AREAS[program.text]

        print(("    " if first else "    ,") + "(" + ",".join([
            "Public Welfare Foundation",  # donor
            donee,  # donee
            amount,  # amount
            donation_date,  # donation_date
            "year",  # donation_date_precision
            "FIXME",  # donation_date_basis
            cause_area,  # cause_area
            "FIXME",  # url
            "FIXME",  # donor_cause_area_url
            notes,  # notes
            "FIXME",  # affected_countries
            "FIXME",  # affected_regions
        ]) + ")")
        first = False


if __name__ == "__main__":
    main()

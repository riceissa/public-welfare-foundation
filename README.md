# public welfare foundation

This repo is for work on Vipul Naik's [Donations List Website](https://github.com/vipulnaik/donations).

The issue that started this repo is: https://github.com/vipulnaik/donations/issues/2

Data is at http://www.publicwelfare.org/grants-process/our-grants/

## Instructions (NEW)

Download data into CSV:

```bash
# NOTE: make sure to edit the range in the scrape file
# (https://github.com/riceissa/public-welfare-foundation/blob/fe1219f75b97f54434123e0fea61d2647ce27659/scrape.py#L15)
# to match the actual page numbers on the website.
./scrape.py > data.csv
```

Use CSV file to generate SQL file:

```bash
./proc2.py data.csv > out.sql
```

## Getting data.html (OLD; before 2019-04-25)

The table on PWF's website is loaded using JavaScript and the URL doesn't change when paginating
so it's a little annoying to get the data.

The table script itself is pretty simple and you can find it at
<http://www.publicwelfare.org/wp-content/themes/publicwelfare/js/page-grants.js>.

What I ended up doing was sending the following request in Chrome's console,
with the `page` parameter varying from 1–12 (i.e. send the request twelve
times; there could be more pages by the time you read this):

```javascript
jQuery.post("http://www.publicwelfare.org/wp-admin/admin-ajax.php", {
            action: 'grants_load',
            categories: "",
            years: "",
            page: 1,
            nextblock: 0,
            prevblock: 0
        }, function(response){
            if(response) {
                if(response === '0') {
                    /*
                     * Wrong response
                     */
                    jQuery("#grants-content").html("Ups :(<br>Something went wrong");
                }
                else {
                    console.log(response);
                }
            }
        });
```

This produces a command/result dump in console. Right click in the console and
do "Save as …". You then have to remove all the command lines so you get just
the results. Store that in `data.html` and you're done.

There might be a better way to do this. In particular clicking on each page and
saving the DOM once that page has loaded, and repeating that, shouldn't be too
bad.

## License

CC0 for the scripts, not sure about data.

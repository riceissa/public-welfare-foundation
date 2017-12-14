# public welfare foundation

## Getting data.html

The table is loaded using JavaScript and the URL doesn't change when paginating
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

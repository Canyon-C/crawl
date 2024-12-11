var url = "https://catalog.sdsu.edu/content.php?catoid=9&navoid=776"

var x = 2; // Assignment
var keys = ["CS420", "CS240", "CS370"];

var crawler = SCRAPE url; 
var elem = FIND keys IN crawler; // find elements from keys
var filtArr = FILTER text IN elem // find elements by text


export(filtered, "output.csv"); 


# EX 2

var crawler = SCRAPE url;
var titles = FIND tag IN crawler; // Find element by tag
var prices = FIND class IN crawler; // Find element by class

print(prices);

# ex 3

var crawler = SCRAPE url;
var descriptions = GET text IN crawler // Find descriptions from elements containing specific text
for description in descriptions {
    if (description.contains("CS420")) {
        print(description);
    }
    print("No CS420 descriptions")
}









var url = "https://www.dominicdabish.com/#educator";
var crawler = SCRAPE url;

var elem = FIND "p" IN crawler;
print(elem);

export(elem, "sample.html");
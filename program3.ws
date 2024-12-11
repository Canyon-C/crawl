var textElem = GET "Projects" IN crawler;
print(textElem);

for (var index IN 1:textElem) {
    if (textElem.contains('Projects')) {
        print("True");
    }
}
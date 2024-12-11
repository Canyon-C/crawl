from textx import metamodel_from_file
import requests
from bs4 import BeautifulSoup
import bs4
from urllib.parse import urljoin
import webbrowser
import os


crawl_mm = metamodel_from_file('crawl.tx')
crawl_model = crawl_mm.model_from_file('real.ws')

class Crawler:
    def __init__(self):
        self.variables = {}
        self.soup = {}

    def scrape(self, url, path):
        response = requests.get(urljoin(url, path))
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, "html.parser")
        return self.soup

    def find(self, key, source, inline=None, text=None):
        if type(source) == bs4.element.ResultSet:
            result = [element.find(key, class_=inline, string=text) for element in source]
            result = [r for r in result if r is not None]
        else:
            result = source.find_all(key, class_=inline, string=text)
        return result

    def filter(self, filter_type, source):
        return [item for item in source if filter_type in item]
    
    def getElm(self, source, text):
        result = source.find_all(string=text)
        return result

    def export(self, data, filename):
        
        if isinstance(data, list):
            html_content = "\n".join(str(item) for item in data)
        else:
            html_content = str(data)
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html_content)
        full_path = os.path.abspath(filename)
        webbrowser.open(f"file://{full_path}")


    def interpret(self, model):
        for statement in model.statements:
            
            if statement.__class__.__name__ == "VarDeclaration":
                if hasattr(statement.value, 'elements'):
                    self.variables[statement.name] = [v.strip('"') for v in statement.value.elements]
                elif statement.value:
                        self.variables[statement.name] = statement.value
                else:
                    self.variables[statement.name] = None

            elif statement.__class__.__name__ == "ScrapeStatement":
                
                if statement.url in self.variables:
                    resolved_url = self.variables[statement.url]
                else:
                    resolved_url = statement.url.strip('"')
                self.variables[statement.name] = self.scrape(resolved_url, statement.path if statement.path else "")

            elif statement.__class__.__name__ == "FindStatement":
                keys = self.variables.get(statement.elementType, []) if self.variables.get(statement.elementType, []) else statement.elementType
                source = self.variables.get(statement.source)
                text = self.variables.get(statement.text) if self.variables.get(statement.text) else statement.text
                inline = self.variables.get(statement.inline) if self.variables.get(statement.inline) else statement.inline
                self.variables[statement.name] = self.find(keys, source, inline, text)

            elif statement.__class__.__name__ == "FilterStatement":
                filter_type = statement.filterType
                source = self.variables.get(statement.source, [])
                self.variables[statement.name] = self.filter(filter_type, source)

            elif statement.__class__.__name__ == "ExportStatement":
                
                data = self.variables.get(statement.data)
                filename = statement.filename.strip('"')
                self.export(data, filename)

            elif statement.__class__.__name__ == "PrintStatement":
                if statement.log in self.variables:
                    print(self.variables.get(statement.log))
                else:
                    print(statement.log)

            elif statement.__class__.__name__ == "GetStatement":
                text = self.variables.get(statement.text) if self.variables.get(statement.text) else statement.text
                source = self.variables.get(statement.source, {})
                self.variables[statement.name] = self.getElm(source, text)

            elif statement.__class__.__name__ == "LoopStatement":
                collection = self.variables.get(statement.source, [])
                self.variables[statement.varName] = statement.start
                if collection != None:
                    for index in range(statement.start, len(collection)):
                        self.variables[statement.varName] = index
                        nested_model = NestedModel(statement.statements)       
                        self.interpret(nested_model)
                        
                    self.variables[statement.varName] = None
            elif statement.__class__.__name__ == "IfStatement":
                condition = statement.condition
                left = self.variables.get(condition.left)
                operator = condition.operator
                right = condition.right
                if operator == "contains":
                        condition_met = right in left
                if condition_met:
                    nested_model = NestedModel(statements=statement.statements)
                    self.interpret(nested_model)        

            else:
                print(f"Unhandled statement type: {statement.__class__.__name__}")

class NestedModel:
    def __init__(self, statements):
        self.statements = statements 
crawler = Crawler()
crawler.interpret(crawl_model)

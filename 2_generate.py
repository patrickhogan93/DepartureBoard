from templates import *
from bs4 import BeautifulSoup
import json


class DataImport():
    def __init__(self, airportlookup, statuslookup):
        self.airportlookup = airportlookup
        self.statuslookup = statuslookup

    def load_json(self):
        with open(airportlookup, "r") as read_file:
            airportlookup = json.load(read_file)

        with open(statuslookup, "r") as read_file:
            statuslookup = json.load(read_file)

    def lookupairport(self):
        arrivalairport = row['arrivalairport']
        row['arrivalairport'] = airportlookup[arrivalairport]
    
    def rationalisetime(self):
        time_str = row['operationtime']
        row['operationtime'] = time_str[11:16]

    def lookupstatus(self):
        try:
            remarkfreetext = row['remarkfreetext']
            row['remarkfreetext'] = statuslookup[remarkfreetext]
        except KeyError:
            print("No status given")


class TableGenerator():
    def __init__(self, template, source, elements, output):
        self.template = template
        self.source = source
        self.element = elements
        self.output = output

    def read_file(self):
        file = open(self.source, 'r')
        self.content = file.read()

    def fetch_records(self):
        soup = BeautifulSoup(self.content, 'lxml')
        self.records = soup.find_all(elements['parent'])

    def parse_records(self):
        self.context = {'table': []}

        for record in self.records:
            row = {}
            for key in elements['child']:
                try:
                    row[key] = record.find(key).get_text()
                except AttributeError:
                    print("No value found")
                    row['key'] = " "

            lookupairport()
            rationalisetime()
            lookupstatus()

            self.context['table'].append(row)

    def render(self):
        self.rendered = get_template("index.html").render(self.context)

    def write(self):
        file = open(output, "w")
        file.write(self.rendered)
        file.close


source = 'flightinfo.xml'
output = 'output/index.html'
template = 'index.html'
parent = 'flightleg'
child = ['callsign', 'arrivalairport', 'operationtime', 'remarkfreetext']
elements = {'parent': parent, 'child': child }

airportlookup = 'airportlookup.json'
statuslookup = 'statuslookup.json'


generator = TableGenerator(template, source, elements, output)

# xml read/parse
generator.read_file()
generator.fetch_records()
generator.parse_records()

# html template parse/write
generator.render()
generator.write()

from templates import *
from bs4 import BeautifulSoup
import json


class TableGenerator():
    def __init__(self, template, source, elements, output, airportlookup, statuslookup):
        self.template = template
        self.source = source
        self.element = elements
        self.output = output
        self.airportlookup = airportlookup
        self.statuslookup = statuslookup

    def load_json(self):
        with open(airportlookup, "r") as read_file:
            airportlookup = json.load(read_file)

        with open(statuslookup, "r") as read_file:
            statuslookup = json.load(read_file)

    def lookupairport(self):
        arrivalairport = row['arrivalairport']
        self.row['arrivalairport'] = airportlookup[arrivalairport]
    
    def rationalisetime(self):
        time_str = self.row['operationtime']
        self.row['operationtime'] = time_str[11:16]

    def lookupstatus(self):
        try:
            remarkfreetext = self.row['remarkfreetext']
            self.row['remarkfreetext'] = statuslookup[remarkfreetext]
        except KeyError:
            print("No status given")

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

            self.lookupairport()
            self.rationalisetime()
            self.lookupstatus()

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

# time = 

generator = TableGenerator(template, source, elements, output, airportlookup, statuslookup)

# xml read/parse
generator.read_file()
generator.fetch_records()
generator.parse_records()

# html template parse/write
generator.render()
generator.write()


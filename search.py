import os
import pickle
import PySimpleGUI as SE #SE stands for search engine

SE.ChangeLookAndFeel('BlueMono')


class GUI:
# Creating GUI
    def __init__(self):
        self.layout = [[SE.Text('Search Term', size=(10, 1)),
                        SE.Input(size=(50, 1), focus=True, key="TERM"),
                        SE.Radio("Contains", size=(10, 1), group_id="choice", key="CONTAINS", default=True),
                        SE.Radio("StartsWith", size=(10, 1), group_id="choice", key="STARTSWITH"),
                        SE.Radio("EndsWith", size=(10, 1), group_id="choice", key="ENDSWITH")],
                       [SE.Text("Root Path", size=(10, 1)),
                        SE.Input('C:/', size=(50, 1), key="PATH"),
                        SE.FolderBrowse("Browse", size=(10, 1)),
                        SE.Button("Re-Index", size=(10, 1), key="_INDEX_"),
                        SE.Button("Search", size=(10, 1), bind_return_key=True, key="_SEARCH_")],
                       [SE.Output(size=(100, 30))]]

        self.window = SE.Window('Local Search Engine', self.layout, element_justification="left")


class SearchEngine:
# Creating Search Engine
    def __init__(self):
        self.file_index = []
        self.results = []
        self.matches = 0
        self.records = 0

    def new_index(self, values):
# Creates new index and saves to a file
        root_path = values["PATH"]
        self.file_index = [(root, files) for root, dirs, files in os.walk(root_path) if files]

        with open("file_index.pkl", 'wb') as f:
            pickle.dump(self.file_index, f)

    def load_index(self):
# Loads index
        try:
            with open("file_index.pkl", 'rb') as f:
                self.file_index = pickle.load(f)
        except:
            self.file_index = []

    def search(self, values):
# Search term based on how user decides to search, contains, startswith, endswith. saves results to file
        self.results.clear()
        self.matches = 0
        self.records = 0
        term = values["TERM"]

        for path, files in self.file_index:
            for file in files:
                self.records += 1

                if (values['CONTAINS'] and \
                        term.lower() in file.lower() or \
                        values['STARTSWITH'] and \
                        file.lower().startswith(term.lower()) or \
                        values['ENDSWITH'] and \
                        file.lower().endswith(term.lower())):
                    result = '/' + file
                    self.results.append(result)
                    self.matches += 1
                else:
                    print("No results found.")
                    continue

        with open('search_results.txt', 'w') as f:
            for row in self.results:
                f.write(row + '\n')


def main():
    g = GUI()
    s = SearchEngine()
    s.load_index()

    while True:
        event, values = g.window.Read()

        if event is None:
            break

        if event == "_INDEX_":
            s.new_index(values)
            print("New index created. \n")

        if event == " _SEARCH_":
            s.search(values)

            for result in s.results:
                print(result)

            print('There were {:,d} matches out of {:,d} records searched.'.format(s.records, s.matches))
            print('Following matches: \n')

if __name__ == '__main__':
    main()

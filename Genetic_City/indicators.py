from brix import Handler, Indicator
from numpy import log
from collections import Counter

class Diversity(Indicator):

        def setup(self):
                self.name = 'Entropy'

        def load_module(self):
                pass

        def return_indicator(self, geogrid_data):
                uses = [cell['name'] for cell in geogrid_data]
                uses = [use for use in uses if use != 'None']

                frequencies = Counter(uses)

                total = sum(frequencies.values(), 0.0)
                entropy = 0
                for key in frequencies:
                        p = frequencies[key]/total
                        entropy += -p*log(p)

                return entropy

div = Diversity()
H = Handler('geneticcity8')
H.add_indicator(div)
H.listen(new_thread=True)
import unittest
import os

from datetime import datetime

from ogn.parser.parse import parse


class TestStringMethods(unittest.TestCase):
    def test_ogn_client(self):
        with open(os.path.dirname(__file__) + '/valid_beacon_data/oneminute.txt') as f:
            for line in f:
                timestamp = datetime.strptime(line[:26], '%Y-%m-%d %H:%M:%S.%f')
                aprs_string = line[28:]
                message = parse(aprs_string, reference_timestamp=timestamp, calculate_relations=True)
                self.assertFalse(message is None)

    def test_ogn_lib(self):
        from ogn_lib import Parser
        
        with open(os.path.dirname(__file__) + '/valid_beacon_data/oneminute.txt') as f:
            for line in f:
                aprs_string = line[28:]
                if aprs_string.startswith('#'):
                    continue
                
                try:
                    message = Parser.parse_message(aprs_string)
                    self.assertFalse(message is None)
                except Exception:
                    print(aprs_string)



if __name__ == '__main__':
    unittest.main()

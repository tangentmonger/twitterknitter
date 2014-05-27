import unittest
import mock
import knitter24
from pattern24 import Pattern24

class TestKnitter(unittest.TestCase):

    @mock.patch('serial.Serial')
    def test_initialise_serial(self, mock_serial):
        knitter = knitter24.Knitter24()
        mock_serial.assert_called_once_with('/dev/ttyUSB0', 9600)

    #i.e. mock entire class Serial, which is why we don't need to import it
    @mock.patch('serial.Serial') #the entire class
    def test_sends_pattern(self, mock_serial):
        knitter = knitter24.Knitter24()
        pattern = Pattern24([( 1,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0)])
        knitter.send_pattern(pattern)

        #LSB first
        calls = [mock.call(chr(1)), mock.call(chr(8)), mock.call(chr(6)), mock.call(chr(129))]
        mock_serial.return_value.write.assert_has_calls(calls)

if __name__ == "__main__":
    unittest.main()

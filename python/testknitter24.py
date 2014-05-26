import unittest
import mock
import knitter24

class TestKnitter(unittest.TestCase):

    @mock.patch('serial.Serial')
    def testInitialiseSerial(self, mock_serial):
        knitter = knitter24.Knitter24()
        mock_serial.assert_called_once_with('/dev/ttyUSB0', 9600)

    #i.e. mock entire class Serial, which is why we don't need to import it
    @mock.patch('serial.Serial') #the entire class
    def testSendsPattern(self, mock_serial):
        knitter = knitter24.Knitter24()
        knitter.send_pattern([( 1,0,0,0,0,0,0,1,
                                0,0,0,0,0,1,1,0,
                                0,0,0,0,1,0,0,0)])

        #LSB first
        calls = [mock.call(chr(1)), mock.call(chr(8)), mock.call(chr(6)), mock.call(chr(129))]
        mock_serial.return_value.write.assert_has_calls(calls)

        #print(mock_serial) #mock of the whole class
        #print(mock_serial.return_value) #mock of an instance
        #print(mock_serial.return_value.write) #mock of the write method on that instance(?)

if __name__ == "__main__":
    unittest.main()

"""Represents a knitting pattern, 24 stitches across. Provides conversions."""

class Pattern24:
    """Represents a knitting pattern, 24 stitches across"""
    
    @classmethod
    def from_image(cls, image):
        """Creates a Pattern object from a PIL Image"""
        image = image.convert(mode='1')
        if image.mode != '1':
            raise ValueError("Image must be black and white only")
        if image.size[0] is not 24:
            raise ValueError("Image must be exactly 24 pixels wide")
        raw_data = list(image.getdata())
        colors = [x[1] for x in image.getcolors()]
        bw_data = cls._convert_to_bw(raw_data, colors)
        chunked_data = list(cls._chunk_list(bw_data))
        return Pattern24(chunked_data)

    @classmethod
    def _chunk_list(cls, data):
        """Breaks a list into 24-tuples"""
        for i in range(0, len(data), 24):
            yield tuple(data[i:i+24])
    
    @classmethod
    def _convert_to_bw(cls, data, colors):
        """Converts pixel data of any two color values into 0s and 1s"""
        black = min(colors)
        return [0 if x == black else 1 for x in data]

    @classmethod
    def from_test_rows(cls):
        """Creates a Pattern24 for testing row by row"""
        test_row_data =    [(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                            (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
                            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                            (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
                            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                            (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
                            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                            (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
                            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                            (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)]
        return Pattern24(test_row_data)

    @classmethod
    def from_test_columns(cls):
        """Creates a Pattern24 for testing column by column"""
        test_column_data = [(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1),
                            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1),
                            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1),
                            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1),
                            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1),
                            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1),
                            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1),
                            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1),
                            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1),
                            (0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1),
                            (0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1),
                            (0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1),
                            (0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1),
                            (0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
                            (0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
                            (0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
                            (0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
                            (0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
                            (0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
                            (0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
                            (0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
                            (0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
                            (0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1),
                            (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)]
        return Pattern24(test_column_data)

    def __init__(self, data):
        """Expects a list of 24-tuples of ones and zeros"""
        self._pattern_data = data

    def get_pattern(self):
        """Returns pattern data as a list of 24-tuples of 0s and 1s"""
        return self._pattern_data


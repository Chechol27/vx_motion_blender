

class PixelCollection:
    shape: tuple[int, int, int]
    pixel_data = list[float]

    def __init__(self, shape: tuple[int, int, int]):
        self.shape = shape
        self.pixel_data = []

    def append_pixel(self, pixel: tuple):
        self.pixel_data.extend(pixel)

    def pixel_data_length(self):
        return len(self.pixel_data)

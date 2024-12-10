

class PixelCollection:
    shape: tuple[int, int, int]
    pixel_data = list[float]

    def __init__(self, shape: tuple[int, int, int]):
        self.shape = shape
        self.pixel_data = []

    def get_max_pixel_count(self):
        return self.shape[0] * self.shape[1]

    def append_pixel(self, pixel: tuple):
        pixel_count = self.pixel_count()
        max_pixel_count = self.get_max_pixel_count()
        if pixel_count + 1 > self.get_max_pixel_count():
            raise Exception(f"Attempted to write more pixels than expected ({pixel_count + 1} > {max_pixel_count})")
        self.pixel_data.extend(pixel)

    def pixel_count(self):
        return self.pixel_data_length() / self.shape[2]

    def pixel_data_length(self):
        return len(self.pixel_data)

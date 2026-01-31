from python.generate.generate_filler import names_surenames_generator
import pandas as pd

class GenerateGuest:
    def __init__(self, guest_count: int, **kwargs):
        self.guest_count = guest_count
    def generate(self):
        try:
            guests = names_surenames_generator(self.guest_count)

            return guests.to_dict(orient='records')
        except Exception as e:
            print(f"Error while generating guests {e}")

if __name__ == "__main__":

    generator = GenerateGuest(150)
    result = generator.generate()
    print(result)
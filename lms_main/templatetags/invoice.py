import time
from random import *

# print(randint(1, 100))


def generate_invoice_number():
    timestamp = time.strftime("%Y%m%d%H%M%S")
    invoice_number = f"INV{timestamp}{randint(1, 99999)}"
    return invoice_number


# Test the function
# invoice_number = generate_invoice_number()
# print("Generated Invoice Number:", invoice_number)

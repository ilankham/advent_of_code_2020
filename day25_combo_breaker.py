""" Solutions for https://adventofcode.com/2020/day/25 """

# import modules used below.
from math import ceil, sqrt
from dataclasses import dataclass


# Part 1: Using the public encryption keys specified in the provided data file,
# what is the private encryption key established by the key-exchange handshake?


# Create data model for encryption object.
@dataclass
class EncryptionObject:
    """ Data Model for encryption object """
    public_key: int
    base: int = 7
    modulus: int = 20201227

    @property
    def loop_size(self):
        """ Solve base^loop_size ≡ public_key (mod modulus) using baby-step
        giant-step algorithm to compute discrete logarithm, with
        inverse step computed using Fermat's Little Theorem; for definitions,
        see https://en.wikipedia.org/wiki/Baby-step_giant-step """
        m = ceil(sqrt(self.modulus))
        powers_of_base = {
            pow(self.base, j, self.modulus): j
            for j in range(m)
        }
        base_to_the_negative_m = pow(
            self.base,
            (self.modulus - 1) - m,
            self.modulus
        )
        gamma = self.public_key
        for i in range(0, m):
            if gamma in powers_of_base:
                return i * m + powers_of_base[gamma]
            else:
                gamma = (gamma * base_to_the_negative_m) % self.modulus

# Read public keys from data file.
with open('data/day25_combo_breaker-data.txt') as fp:
    card = EncryptionObject(int(fp.readline().rstrip()))
    door = EncryptionObject(int(fp.readline().rstrip()))

# Compute private encryption key, using two different techniques, for Part 1.
private_encryption_key_from_card = pow(
    door.public_key,
    card.loop_size,
    door.modulus
)
private_encryption_key_from_door = pow(
    card.public_key,
    door.loop_size,
    card.modulus
)
print(
    f'Private encryption key, using card as basis, for Part 1: '
    f'{private_encryption_key_from_card}'
)
print(
    f'Private encryption key, using door as basis, for Part 1: '
    f'{private_encryption_key_from_door}'
)


# Part 2: No computation needed for Part 2.

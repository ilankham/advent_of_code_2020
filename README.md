[![Python 3.8](https://img.shields.io/badge/python-3.8-brightgreen.svg)](#prerequisites)  [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

# Advent of Code 2020 Progress

## Getting Started

1. [Clone](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) or [download/unzip](https://github.com/ilankham/advent_of_code_2020/archive/main.zip) this repo.

2. Install packages specified in [requirements.txt](requirements.txt), e.g., from the command line:
```
pip install -r requirements.txt
```

3. Run the solution for a specific day, e.g., from the command line:
```
python day01_report_repair.py
```

4. For context about a specific problem, see <https://adventofcode.com/2020/>


### Prerequisites

Python 3.8 or greater, along with the packages specified in [requirements.txt](requirements.txt):

* [regex](https://pypi.org/project/regex/) is used for recursive regular expressions in the [Day 19](https://adventofcode.com/2020/day/19) solution.

* [sympy](https://www.sympy.org/) is used for its [implementation](https://docs.sympy.org/latest/modules/ntheory.html#sympy.ntheory.modular.crt) of the [Chinese Remainder Theorem](https://en.wikipedia.org/wiki/Chinese_remainder_theorem) in the [Day 13](https://adventofcode.com/2020/day/13) solution.

### License
All repo contents are licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Notes

### Approach

As a first-time Advent of Code (AoC) participant, with no sense of what to expect, the goal was to balance pacing with learning. This led to several shortcuts:

* No unit tests were written.

* Code was not generalized to handle possible corner cases.

* Input-file processing was standardized around container classes storing data as-is, with the goal of Part 1 solutions only needing minor refactoring or extension for Part 2.

* Standard Python data structures (primarily `list`, `dict`, and `set`) were used whenever possible, unless performance became important.

* Third-party Python packages were only used when a standard library solution wasn't available for sub-problems having a potentially tedious implementation.

### Takeaways

Even though this approach failed miserably for a few of the later problems, where Part 2 required completely rethinking data modeling, it was an overwhelming positive experience. I'm incredibly grateful to the AoC team for creating an engaging narrative centered around compelling programming challenges.

Some additional random thoughts:

* With apologies to [Tim Peters](https://www.python.org/dev/peps/pep-0020/), newer Python features like [`dataclasses`](https://docs.python.org/3.8/library/dataclasses.html) and [`:=`](https://www.python.org/dev/peps/pep-0572/) are honking great idea -- let's do more of those!

* For some of the problems, my biggest roadblock was a complete lack of geometric intuition. [Day 20](https://adventofcode.com/2020/day/20) was especially challenging and took a couple of weeks to fully grok. (It wasn't clear from the problem statement that all dihedral group $D_4$ transformations were possible.) Undoubtedly, since tiles are composed of only two pixel types, some clever isomorphic binary representation could transform the problem into a significantly simpler form. Despite this, it did feel productive to struggle with tile data as-is, and to practice spacial reasoning.

* The most unexpectedly enjoyable part? Using number theory for a couple of the problems. Who knew pirates, the canonical subject of applications of the Chinese Remainder Theorem, have something in common with [airport shuttle bus schedules](https://adventofcode.com/2020/day/13)!

## Author
* [ilankham](https://github.com/ilankham)

## Disclaimer

This project is in no way affiliated with [Advent of Code](https://adventofcode.com).

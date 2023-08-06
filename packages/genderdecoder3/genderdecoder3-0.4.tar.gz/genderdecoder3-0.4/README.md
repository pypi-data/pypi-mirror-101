# Gender Decoder

This is a python package for assessing gender-coded words in a job adverts.

It is a fork of the Python 2.x package by [Doteveryone](https://github.com/Doteveryone/genderdecoder), updated to Python 3 by [Rob Bell](https://github.com/robbell). The 2.x package was in turn based on django app [gender-decoder.katmatfield.com](http://gender-decoder.katmatfield.com) / https://github.com/lovedaybrooke/gender-decoder developed by [Kat Matfield](http://www.katmatfield.com) and based the paper ["Evidence That Gendered Wording in Job Advertisements Exists and Sustains Gender Inequality"](http://gender-decoder.katmatfield.com/static/Gaucher-Friesen-Kay-JPSP-Gendered-Wording-in-Job-ads.pdf) by Danielle Gaucher and Justin Friesen and Aaron C. Kay.

## Install

```sh
pip install genderdecoder
```

## Usage

```python
import genderdecoder

job_description = "Example job description text"
print(genderdecoder.assess(job_description))

```

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/helloworldpy)  ![PyPI - Status](https://img.shields.io/pypi/status/helloworldpy)  ![PyPI](https://img.shields.io/pypi/v/helloworldpy) ![PyPI - License](https://img.shields.io/pypi/l/helloworldpy)
# [helloworldpy]

## This is a basic project for learning how to make the PIP([PyPI]) package

### To install the package!
#### On Windows:
```bash 
$ pip install helloworldpy
```
#### On macOS and Linux:
```bash
$ sudo pip3 install helloworldpy
```

# Changelog

Check the [changelog here].
### Example:
```bash
$ helloworldpy -h                                                         
usage: helloworldpy [-h] [-V] [-n [NAME [NAME ...]]] [-ip] [-g]

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program version
  -n [NAME [NAME ...]], --name [NAME [NAME ...]]
                        output Hello Name! or Hello World!
  -ip, --checkip        This will check public IP address of system
  -g, --playgame        You can play Bulls and Cows game
```

# Usage

## helloworldpy --name (with out arguments)
```bash 
$ helloworldpy --name
  Hello World!
```
## helloworldpy --name (with arguments)
```bash 
$ helloworldpy --name py
  Hello Py!
```
## You Can Play [Bulls and Cows] Game
```bash 
$ helloworldpy --playgame
  Hello World Py!

        ##############--->>> Rules: <<---################
        #   Note:                                       #
        #       Bulls = correct code, correct position. #
        #       Cows = correct code, wrong position.    #
        #################################################

how many digits number you need? 2
enter a number you guess: 12
Cow : 0,Bull : 0
enter a number you guess: 34
Cow : 0,Bull : 1
enter a number you guess: 56
Cow : 0,Bull : 0
enter a number you guess: 89
Cow : 0,Bull : 1
enter a number you guess: 94
Cow : 1,Bull : 0
enter a number you guess: 93
Cow : 2,Bull : 0
enter a number you guess: 39
Cow : 0,Bull : 2

                    |-------------------------------|
                                YOU WON!
                      * Answer is "39"
                      * Number of attempts are 7
                    |-------------------------------|


```
## To Check System public IP Address
```bash 
$ helloworldpy --checkip
  Hello World Py!
  Public IP Address: 1▨0.2▨▨.0▨▨.▨3▨
```
# License
[MIT License]

Copyright (c) 2020 [Saketh Chandra]

[PyPI]: https://pypi.org/
[changelog here]: https://github.com/Saketh-Chandra/helloworldpy/releases/
[helloworldpy]: https://pypi.org/project/helloworldpy/
[Bulls and Cows]: https://en.wikipedia.org/wiki/Bulls_and_Cows#The_numerical_version
[MIT License]: https://github.com/Saketh-Chandra/helloworldpy/blob/master/LICENSE
[Saketh Chandra]: https://github.com/Saketh-Chandra/ 
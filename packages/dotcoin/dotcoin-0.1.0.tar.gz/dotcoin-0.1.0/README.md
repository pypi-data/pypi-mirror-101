# DotCoin

## Introduction

DotCoin is an abstract interface build around ccxt to access information on cryptocurrency markets from a variety of
exchanges/platforms, while being accessible to non-coders or coders who don't want to write a program just to check some
basic info.

As of this moment, DotCoin provides a simple cli that can look into the basic stats of some markets and checking their
current order-book. Please bear in mind that DotCoin is currently just a personal project that just started its
development status and needs a lot of time and work to grow.

## Installation

A package with the name "dotcoin" is available in pypi.

````commandline
pip install --user dotcoin 
````

This package has been tested mainly with **Python 3.7.9** on **Windows 10**, but it should work on all platforms since
it only makes use of cross-platform libraries. You may need to prefix this command with *"pip3"*, *"python3 -m pip"* or
*"python -m pip"* instead when running on other platforms or different Python setups.

## General Usage

````commandline
dotcoin -h
````

````text
usage: parity [-h] {exchanges,markets,ticker,book} ...

positional arguments:
  {exchanges,markets,ticker,book}
    exchanges           list supported exchanges
    markets             list supported markets
    ticker              fetch ticker from a given market
    book                fetch book from a given market

optional arguments:
  -h, --help            show this help message and exit
````

## Limited support

As of now, only these exchanges are supported.

* BINANCE
* BITTREX

Although DotCoin is build on top of ccxt, which supports a considerable number of platforms, as interface which targets
the end-user, I consider it's important to provide a stable usability instead of unreliable feature set. This is why
there will be limited support for most exchanges in the meantime, and more will be added once certain level of
reliability is achieved.

## Thanks

I greatly thank the ccxt team for their amazing work on the ccxt library, it's only thanks to the project they've built
that this app is even possible. You can check their work out at their [GitHub](https://github.com/ccxt/ccxt).

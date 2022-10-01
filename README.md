# BitcoinNotifier

A script which alerts the user when the Bitcoin price changes rapidly above or below a given threshold.

[![forthebadge](https://forthebadge.com/images/badges/powered-by-black-magic.svg)](https://forthebadge.com)

The price is fetched from the [_Binance API_](https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md) every 30 seconds and the default currency is USD. These values can be changed at will.

## How to install and run code
### Installation

```console
# clone the repo
$ git clone https://github.com/Calypso-io/BitcoinNotifier

# change the working directory to Bitcoin Notifier
$ cd BitcoinNotifier

# install general requirements
$ pip install -r requirements.txt

# Run this line only on MacOS
$ pip install pyobjc
```
On **Linux** make sure `python3-gst-1.0` is installed by running `sudo apt install python3-gst-1.0`

### Run
```console
$ python alert.py
```

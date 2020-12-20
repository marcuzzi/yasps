# yasps - Yet Another Stock Price Scraper

## Introduction
yasps is another scraper written in python to find articles with limited stock.

It is written Python3 using requests and beautifulsoup libraries. It also uses curses to actively display results. It has some dependencies on Windows libraries (winsound package) which can be easily rewritten for compatibility with other OSes.

## Motivation

Christmas 2020 will go down in history as the crisis of stock of various electronic items:
- AMD Ryzen 5xxx CPUs
- Nvidia RTX 30 and 58xx, 59xx AMD GPUs
- PS5 and Xbox Series X/S new generation consoles

## How to run

1. Clone the repository
2. Run
   ```
   python install.py install
   ```
   Alternatively install all dependencies with `pip install`
   - beautifulsoup4
   - keyboard
   - pynput
   - requests
   - windows-curses
   
   Note: Sound alert function is based on winsound library for Windows systems. This needs to be modified to run this program in other OSes.
   
3. Edit `yasps.py` to include items and URLs to monitor.

   Each monitored item is defined as a `MonitorItemAvailability` with a name, desired price, and a list of `Check` objects.
   
   Each `Check` class implements a scraper for a specific web. Available classes are defined in `scraper\checks.py`.
   
   A function `getCheck` is provided to automatically return an appropriate `Check` class object based on the URL.
   
   Example:
   ```python
   item = 'Ryzen 5600X'
   checks = []
   checks.append(getCheck(item, 'https://www.pccomponentes.com/amd-ryzen-5-5600x-37ghz'))
   checks.append(getCheck(item, 'https://www.vsgamers.es/product/procesador-amd-ryzen-5-5600x-37-ghz'))
   ...
   targetPrice = 325
   monitor_cpu = MonitorItemAvailability(item, targetPrice, checks)
   ```
   
   It is also possible to define generic items (e.g. GPU) with different products:
   ```python
   item = 'RTX 3060'
   checks = []
   checks.append(getCheck('Zotac 3060 Ti D6 Twin Edge 8Gb', 'https://www.pccomponentes.com/zotac-geforce-rtx-3060-ti-d6-twin-edge-8gb-gddr6'))
   checks.append(getCheck('Zotac 3060 Ti D6 Twin Edge OC 8Gb', 'https://www.pccomponentes.com/zotac-geforce-rtx-3060ti-d6-twin-edge-oc-8gb-gddr6'))
   ...
   monitor_gpu = MonitorItemAvailability(item, targetPrice, checks, True)
   ```
   
   All articles to be monitored are included on the `monitors` list:
   ```python
   monitors = [ monitor_cpu, monitor_gpu]
   ```
   
4. Run the edited `yasps.py` file
   ```
   python yasps.py
   ```

### Parameters
Currently only the '-s' parameter can be provided as an argument to run silently (no sound alert).

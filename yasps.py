import scraper.log
logger = scraper.log.setup_custom_logger('yasps')

from scraper.scraper import *
import curses
import sys
import time

#-----------------------------------------------------------------------------------------------------------------  
# CPU Ryzen 5600X
item = 'Ryzen 5600X'
checks = []
checks.append(getCheck(item, 'https://www.pccomponentes.com/amd-ryzen-5-5600x-37ghz'))
checks.append(getCheck(item, 'https://www.vsgamers.es/product/procesador-amd-ryzen-5-5600x-37-ghz'))
checks.append(getCheck(item, 'https://www.wipoid.com/amd-ryzen-5-5600x-3-7ghz.html'))
checks.append(getCheck(item, 'https://www.alternate.es/AMD/100-100000065BOX-Procesador/html/product/1685588'))
checks.append(getCheck(item, 'https://www.neobyte.es/procesador-amd-ryzen-5-5600x-socket-am4-7702.html'))
checks.append(getCheck(item, 'https://www.coolmod.com/amd-ryzen-5-5600x-46ghz-socket-am4-boxed-procesador-precio'))
checks.append(getCheck(item, 'https://www.amazon.es/AMD-Ryzen-5-5600X-Box/dp/B08166SLDF/'))
targetPrice = 325
monitor_cpu = MonitorItemAvailability(item, targetPrice, checks)

#-----------------------------------------------------------------------------------------------------------------  
# GPU RTX 3060
item = 'RTX 3060'
checks = []
checks.append(getCheck('Zotac 3060 Ti D6 Twin Edge 8Gb', 'https://www.pccomponentes.com/zotac-geforce-rtx-3060-ti-d6-twin-edge-8gb-gddr6'))
checks.append(getCheck('Zotac 3060 Ti D6 Twin Edge OC 8Gb', 'https://www.pccomponentes.com/zotac-geforce-rtx-3060ti-d6-twin-edge-oc-8gb-gddr6'))
checks.append(getCheck('MSI 3060 Ti Ventus 2X OC 8Gb', 'https://www.pccomponentes.com/msi-rtx-3060-ti-ventus-2x-oc-8gb-gddr6'))
checks.append(getCheck('MSI 3060 Ti Ventus 3X OC 8Gb', 'https://www.pccomponentes.com/msi-rtx-3060-ti-ventus-3x-oc-8gb-gddr6'))
checks.append(getCheck('Gigabyte 3060 Ti Gaming OC 8Gb','https://www.pccomponentes.com/gigabyte-geforce-rtx-3060-ti-gaming-oc-8gb-gddr6'))
targetPrice = 480
monitor_gpu = MonitorItemAvailability(item, targetPrice, checks, True)

#-----------------------------------------------------------------------------------------------------------------  
# GPU
item = 'MSI RTX 3060 Ti GAMING X TRIO 8GB GDDR6'
checks = []
checks.append(getCheck(item, 'https://www.pccomponentes.com/msi-rtx-3060-ti-gaming-x-trio-8gb-gddr6'))
checks.append(getCheck(item, 'https://www.vsgamers.es/product/tarjeta-grafica-msi-geforce-rtx-3060-ti-gaming-x-trio'))
checks.append(getCheck(item, 'https://www.coolmod.com/msi-geforce-rtx-3060-ti-gaming-x-trio-8gb-gddr6-tarjeta-grafica-precio'))
checks.append(getCheck(item, 'https://www.wipoid.com/msi-geforce-rtx-3060-ti-gaming-x-trio-8gb-gddr6.html'))
targetPrice = 480
monitor_gpumsi = MonitorItemAvailability(item, targetPrice, checks)


monitors = [ monitor_cpu, monitor_gpu, monitor_gpumsi]

# Default parameters
interval_min = 5
interval_max = 20
beep = True

# Get options and run scraper
for i in range(1, len(sys.argv)):
    if (sys.argv[i] == '-s'):
	    beep = False

curses.wrapper(main_curses, monitors, interval_min, interval_max, beep)
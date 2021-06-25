import time
import logdata
import sitehandler
import display

def __init__(filename, delay):
    with open(filename, 'r') as f: # Only need to read the file once to get all the websites
        lines = f.read().splitlines()
    f.close()
    logger = logdata.UpdateLog(None)

    while True:
        sites = sitehandler.SiteHandler(len(lines))
        print('Updating prices...')
        start_time = time.time()
        products = []
        for line in lines:
            product = sites.find_site(line)
            products.append(product)

        displayer = display.Display()
        for product in products:
            print(product.disassemble())
            displayer.generate_console_log(*product.disassemble())
        displayer.print_console_log()
        #sites.displayer.packer.__print__()
        logger.data = displayer.packer.data
        logger.update()
        print(f'Results found ({sites.completed_tasks}/{sites.total_tasks}) in {time.time() - start_time} sec')

        #print(sites.displayer.packer.unpack())

        time.sleep(60*delay)
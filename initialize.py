import time
import logdata
import sitehandler
import display
import datahandler

def __init__(filename, delay):

    logger = logdata.UpdateLog()

    while True:
        # Read the product URLs to be scrapped
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
        f.close()

        sites = sitehandler.SiteHandler(len(lines))
        print('Updating prices...')
        start_time = time.time()

        # Calls find_site on all products and returns the Product class for each product and puts it into a list
        products = []
        for line in lines:
            product = sites.find_site(line)
            if product != None:
                products.append(product)

        # Initializes the display class and packing class
        displayer = display.Display()
        packer = datahandler.Package()

        # Takes each Product class and displays it onto console and packs the data to the Package class
        for product in products:
            data = product.disassemble()
            displayer.generate_console_log(*data)
            packer.pack(*data)
        displayer.print_console_log()

        # Takes the packed data from Package class to update the product history file
        logger.data = packer.data
        logger.update(packer)
        print(f'Results found ({sites.completed_tasks}/{sites.total_tasks}) in {time.time() - start_time} sec')

        time.sleep(60*delay)
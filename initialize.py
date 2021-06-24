import time
import logdata
import sitehandler

def __init__(filename, delay):
    with open(filename, 'r') as f: # Only need to read the file once to get all the websites
        lines = f.read().splitlines()
    f.close()
    logger = logdata.UpdateLog(None)

    while True:
        sites = sitehandler.SiteHandler(len(lines))
        print('Updating prices...')
        start_time = time.time()
        for line in lines:
            sites.find_site(line)
        sites.displayer.print_console_log()
        #sites.displayer.packer.__print__()
        logger.data = sites.displayer.packer.data
        logger.update()
        print(f'Results found ({sites.completed_tasks}/{sites.total_tasks}) in {time.time() - start_time} sec')

        #print(sites.displayer.packer.unpack())

        time.sleep(60*delay)
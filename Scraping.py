from scrapy import cmdline

def run_scrapy():
    cmdline.execute("scrapy runspider scrapy_lib.py".split())  # followall is the spider name
    return True

run_scrapy()
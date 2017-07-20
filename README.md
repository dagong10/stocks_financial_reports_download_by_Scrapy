# stocks_financial_reports_download_by_Scrapy
python+mysql+scrapy\
the main function is to download all Chinese stocks market financial reports from websit by scrapy\
before you download and run this, remember to install mysql and related mysql-python pips\
the work flow is below\
1. Set the urls' pool
2. Scrapy the pool and download the stock financial report .csv files
3. save the csv file content into MySQL
4. when one stock with 3 .csv files downloaded, take all this data to a csv file together
5. Use 'load' .csv files into SQL to fill the related table 
6. Done!

The lite branch is setup for reducing the running time(master branch work 7 to 8 hours).\
Work flow is below.\
The same with master branh's from step 1 to 3.\
The step 4 to 5 could be down by EV.

The test result is good. CPU 8% used by python, 3% by mysqld, 99% Max speed; memory 82% used.   

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

the lite branch is setup for reducing the running time(master branch work 7 to 8 hours)
work flow is below
the same with master branh's 1 and 2
ignore the step 3

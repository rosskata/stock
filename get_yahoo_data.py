#iteratively get all ticker data for S&P500 companies
#import libs
import datetime
import csv
import pandas_datareader as pdr

#startDate = "2022-01-01"
today = datetime.date.today()
startDate= datetime.date.today()

infilename ="snp500_list.csv"
infile = open(infilename,"r")

while True:
    ticker=infile.readline()

    if not ticker:
        break;

    try:
      data = pdr.get_data_yahoo(ticker.strip(),startDate,today)
      outfileName = ticker.strip()
      outfileExt = ".csv"
      outfileNameString = outfileName + outfileExt
      outfile = open(outfileNameString,"w")
      outfile.write(ticker)
      outfile.write(data.to_string(index=False))
      outfile.write("\n")
      outfile.close()
      print("--->", ticker.strip(),"<--- \n ",data,"\n")

    except ValueError:
      print('ValueErrror')


print("---=== GOT ALL TICKER DATA from %s to %s ===---", startDate, today)
infile.close()

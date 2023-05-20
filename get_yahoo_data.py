''' iteratively get all ticker data for S&P500 companies'''

# import libs
import datetime
import pandas_datareader as pdr

STARTDATE = "2012-01-01"
today = datetime.date.today()
# STARTDATE= datetime.date.today()

INFILENAME = "snp500_list.csv"

infile =  open(INFILENAME, "r", encoding="utf-8")

while True:
    ticker = infile.readline()

    if not ticker:
        break

    try:
        data = pdr.get_data_yahoo(ticker.strip(), STARTDATE, today)
        outfileName = ticker.strip()
        outfileNameString = outfileName + ".csv"
        outfile = open(outfileNameString, "w", encoding="utf-8")
        outfile.write(ticker)
        outfile.write(data.to_string(index=False))
        outfile.write("\n")
        outfile.close()
        print("---> Got ", ticker.strip(), " data!")

    except ValueError:
        print('ValueErrror')


print("---=== GOT ALL TICKER DATA from ", STARTDATE, " to ", today, " ===---")
infile.close()

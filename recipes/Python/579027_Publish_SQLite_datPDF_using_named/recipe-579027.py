# SQLiteToPDFWithNamedTuples.py
# Author: Vasudev Ram - http://www.dancingbison.com
# SQLiteToPDFWithNamedTuples.py is a program to demonstrate how to read 
# SQLite database data and convert it to PDF. It uses the Python
# data structure called namedtuple from the collections module of 
# the Python standard library.

from __future__ import print_function
import sys
from collections import namedtuple
import sqlite3
from PDFWriter import PDFWriter

# Helper function to output a string to both screen and PDF.
def print_and_write(pw, strng):
    print(strng)
    pw.writeLine(strng)

try:

    # Create the stocks database.
    conn = sqlite3.connect('stocks.db')
    # Get a cursor to it.
    curs = conn.cursor()

    # Create the stocks table.
    curs.execute('''DROP TABLE IF EXISTS stocks''')
    curs.execute('''CREATE TABLE stocks
                 (date text, trans text, symbol text, qty real, price real)''')

    # Insert a few rows of data into the stocks table.
    curs.execute("INSERT INTO stocks VALUES ('2006-01-05', 'BUY', 'RHAT', 100, 25.1)")
    curs.execute("INSERT INTO stocks VALUES ('2007-02-06', 'SELL', 'ORCL', 200, 35.2)")
    curs.execute("INSERT INTO stocks VALUES ('2008-03-07', 'HOLD', 'IBM', 300, 45.3)")
    conn.commit()

    # Create a namedtuple to represent stock rows.
    StockRecord = namedtuple('StockRecord', 'date, trans, symbol, qty, price')

    # Run the query to get the stocks data.
    curs.execute("SELECT date, trans, symbol, qty, price FROM stocks")

    # Create a PDFWriter and set some of its fields.
    pw = PDFWriter("stocks.pdf")
    pw.setFont("Courier", 12)
    pw.setHeader("SQLite data to PDF with named tuples")
    pw.setFooter("Generated by xtopdf - https://bitbucket.org/vasudevram/xtopdf")

    # Write header info.
    hdr_flds = [ str(hdr_fld).rjust(10) + " " for hdr_fld in StockRecord._fields ]
    hdr_fld_str = ''.join(hdr_flds)
    print_and_write(pw, '=' * len(hdr_fld_str))
    print_and_write(pw, hdr_fld_str)
    print_and_write(pw, '-' * len(hdr_fld_str))

    # Now loop over the fetched data and write it to PDF.
    # Map the StockRecord namedtuple's _make class method
    # (that creates a new instance) to all the rows fetched.
    for stock in map(StockRecord._make, curs.fetchall()):
        row = [ str(col).rjust(10) + " " for col in (stock.date, \
        stock.trans, stock.symbol, stock.qty, stock.price) ]
        # Above line can instead be written more simply as:
        # row = [ str(col).rjust(10) + " " for col in stock ]
        row_str = ''.join(row)
        print_and_write(pw, row_str)

    print_and_write(pw, '=' * len(hdr_fld_str))

except Exception as e:
    print("ERROR: Caught exception: " + e.message)
    sys.exit(1)

finally:
    pw.close()
    conn.close()
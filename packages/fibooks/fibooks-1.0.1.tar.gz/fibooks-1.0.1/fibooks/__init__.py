# fibooks by Timo Kats
# version 0.0.1
# March 2021
# __init__.py

import json
import xlsxwriter

try:
    from fibooks.classes.info import info
    from fibooks.classes.balance_sheet import balance_sheet
    from fibooks.classes.statement_of_cash_flows import statement_of_cash_flows
    from fibooks.classes.statement_of_equity import statement_of_equity
    from fibooks.classes.compute import compute
    print('fibooks was loaded succesfully.')
except:
    from classes.info import info
    from classes.balance_sheet import balance_sheet
    from classes.statement_of_cash_flows import statement_of_cash_flows
    from classes.statement_of_equity import statement_of_equity
    from classes.compute import compute
    print('fibooks was loaded succesfully.')
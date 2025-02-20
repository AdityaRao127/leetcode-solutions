import pandas as pd

def createBonusColumn(employees: pd.DataFrame) -> pd.DataFrame:
    employees['bonus'] = [salary*2 for salary in employees['salary']]
    return employees

import pandas as pd

def modifySalaryColumn(employees: pd.DataFrame) -> pd.DataFrame:
    employees['salary'] = [salary*2 for salary in employees['salary']]
    return employees

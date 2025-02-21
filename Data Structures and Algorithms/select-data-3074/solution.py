import pandas as pd

def selectData(students: pd.DataFrame) -> pd.DataFrame:
    students = students.loc[students['student_id'] == 101, ['name', 'age']]
    return students


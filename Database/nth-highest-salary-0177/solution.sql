CREATE OR REPLACE FUNCTION NthHighestSalary(N INT) RETURNS TABLE (Salary INT) AS $$
BEGIN
IF N < 1 THEN 
    RETURN QUERY(SELECT NULL::INT AS salary);
ELSE
  RETURN QUERY (
    SELECT DISTINCT Employee.salary
      from Employee
      ORDER BY salary DESC
      LIMIT 1
      OFFSET N-1
  );
 END IF;
END;
$$ LANGUAGE plpgsql;

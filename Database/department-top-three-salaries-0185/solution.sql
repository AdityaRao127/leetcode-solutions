-- Write your PostgreSQL query statement below
SELECT Department.name AS "Department", Employee.name AS "Employee", Employee.salary AS "Salary"
FROM Employee
JOIN Department ON Employee.departmentId = Department.id
WHERE Employee.salary IN (
    SELECT DISTINCT salary
    FROM Employee e2
    WHERE e2.departmentId = Employee.departmentId
    ORDER BY salary DESC
    LIMIT 3
)
ORDER BY "Department", "Salary" DESC, "Employee";


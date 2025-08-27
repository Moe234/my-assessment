"""
The database loan.db consists of 5 tables:
   1. customers - table containing customer data
   2. loans - table containing loan data pertaining to customers
   3. credit - table containing credit and creditscore data pertaining to customers
   4. repayments - table containing loan repayment data pertaining to customers
   5. months - table containing month name and month ID data

You are required to make use of your knowledge in SQL to query the database object (saved as loan.db) and return the requested information.
Simply fill in the vacant space wrapped in triple quotes per question (each function represents a question)

NOTE:
The database will be reset when grading each section. Any changes made to the database in the previous `SQL` section can be ignored.
Each question in this section is isolated unless it is stated that questions are linked.
Remember to clean your data

"""


def question_1():
    """
    Make use of a JOIN to find the `AverageIncome` per `CustomerClass`
    """

    qry = """
    SELECT c.CustomerClass,
           AVG(cu.Income) AS AverageIncome
    FROM credit c
    JOIN customers cu ON c.CustomerID = cu.CustomerID
    GROUP BY c.CustomerClass
    """
    return qry


def question_2():
    """
    Make use of a JOIN to return a breakdown of the number of 'RejectedApplications' per 'Province'.
    Ensure consistent use of either the abbreviated or full version of each province, matching the format found in the customer table.
    """

    qry = """
    SELECT cu.Province,
           COUNT(*) AS RejectedApplications
    FROM loans l
    JOIN customers cu ON l.CustomerID = cu.CustomerID
    WHERE l.ApprovalStatus = 'Rejected'
    GROUP BY cu.Province
    """
    return qry


def question_3():
    """
    Making use of the `INSERT` function, create a new table called `financing` which will include the following columns:
    `CustomerID`,`Income`,`LoanAmount`,`LoanTerm`,`InterestRate`,`ApprovalStatus` and `CreditScore`

    Do not return the new table, just create it.
    """

    qry = """
    CREATE TABLE financing (
        CustomerID INT,
        Income REAL,
        LoanAmount REAL,
        LoanTerm INT,
        InterestRate REAL,
        ApprovalStatus TEXT,
        CreditScore INT
    );
    INSERT INTO financing
    SELECT l.CustomerID, cu.Income, l.LoanAmount, l.LoanTerm,
           l.InterestRate, l.ApprovalStatus, c.CreditScore
    FROM loans l
    JOIN customers cu ON l.CustomerID = cu.CustomerID
    JOIN credit c ON c.CustomerID = cu.CustomerID
    """
    return qry


# Question 4 and 5 are linked


def question_4():
    """
    Using a `CROSS JOIN` and the `months` table, create a new table called `timeline` that sumarises Repayments per customer per month.
    Columns should be: `CustomerID`, `MonthName`, `NumberOfRepayments`, `AmountTotal`.
    Repayments should only occur between 6am and 6pm London Time.
    Null values to be filled with 0.

    Hint: there should be 12x CustomerID = 1.
    """

    qry = """
    CREATE TABLE timeline AS
    SELECT c.CustomerID,
           m.MonthName,
           COALESCE(COUNT(r.RepaymentID), 0) AS NumberOfRepayments,
           COALESCE(SUM(r.Amount), 0) AS AmountTotal
    FROM customers c
    CROSS JOIN months m
    LEFT JOIN repayments r
      ON r.CustomerID = c.CustomerID
     AND r.MonthID = m.MonthID
     AND CAST(STRFTIME('%H', r.RepaymentTime) AS INT) BETWEEN 6 AND 17
    GROUP BY c.CustomerID, m.MonthName
    """
    return qry


def question_5():
    """
    Make use of conditional aggregation to pivot the `timeline` table such that the columns are as follows:
    `CustomerID`, `JanuaryRepayments`, `JanuaryTotal`,...,`DecemberRepayments`, `DecemberTotal`,...etc
    MonthRepayments columns (e.g JanuaryRepayments) should be integers

    Hint: there should be 1x CustomerID = 1
    """

    qry = """
    SELECT CustomerID,
           SUM(CASE WHEN MonthName='January'  THEN NumberOfRepayments END) AS JanuaryRepayments,
           SUM(CASE WHEN MonthName='January'  THEN AmountTotal END)       AS JanuaryTotal,
           SUM(CASE WHEN MonthName='February' THEN NumberOfRepayments END) AS FebruaryRepayments,
           SUM(CASE WHEN MonthName='February' THEN AmountTotal END)       AS FebruaryTotal,
           SUM(CASE WHEN MonthName='March'    THEN NumberOfRepayments END) AS MarchRepayments,
           SUM(CASE WHEN MonthName='March'    THEN AmountTotal END)       AS MarchTotal,
           SUM(CASE WHEN MonthName='April'    THEN NumberOfRepayments END) AS AprilRepayments,
           SUM(CASE WHEN MonthName='April'    THEN AmountTotal END)       AS AprilTotal,
           SUM(CASE WHEN MonthName='May'      THEN NumberOfRepayments END) AS MayRepayments,
           SUM(CASE WHEN MonthName='May'      THEN AmountTotal END)       AS MayTotal,
           SUM(CASE WHEN MonthName='June'     THEN NumberOfRepayments END) AS JuneRepayments,
           SUM(CASE WHEN MonthName='June'     THEN AmountTotal END)       AS JuneTotal,
           SUM(CASE WHEN MonthName='July'     THEN NumberOfRepayments END) AS JulyRepayments,
           SUM(CASE WHEN MonthName='July'     THEN AmountTotal END)       AS JulyTotal,
           SUM(CASE WHEN MonthName='August'   THEN NumberOfRepayments END) AS AugustRepayments,
           SUM(CASE WHEN MonthName='August'   THEN AmountTotal END)       AS AugustTotal,
           SUM(CASE WHEN MonthName='September' THEN NumberOfRepayments END) AS SeptemberRepayments,
           SUM(CASE WHEN MonthName='September' THEN AmountTotal END)       AS SeptemberTotal,
           SUM(CASE WHEN MonthName='October'  THEN NumberOfRepayments END) AS OctoberRepayments,
           SUM(CASE WHEN MonthName='October'  THEN AmountTotal END)       AS OctoberTotal,
           SUM(CASE WHEN MonthName='November' THEN NumberOfRepayments END) AS NovemberRepayments,
           SUM(CASE WHEN MonthName='November' THEN AmountTotal END)       AS NovemberTotal,
           SUM(CASE WHEN MonthName='December' THEN NumberOfRepayments END) AS DecemberRepayments,
           SUM(CASE WHEN MonthName='December' THEN AmountTotal END)       AS DecemberTotal
    FROM timeline
    GROUP BY CustomerID
    """
    return qry


# QUESTION 6 and 7 are linked, Do not be concerned with timezones or repayment times for these question.


def question_6():
    """
    The `customers` table was created by merging two separate tables: one containing data for male customers and the other for female customers.
    Due to an error, the data in the age columns were misaligned in both original tables, resulting in a shift of two places upwards in
    relation to the corresponding CustomerID.

    Create a table called `corrected_customers` with columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender`
    Utilize a window function to correct this mistake in the new `CorrectedAge` column.
    Null values can be input manually - i.e. values that overflow should loop to the top of each gender.

    Also return a result set for this table (ie SELECT * FROM corrected_customers)
    """

    qry = """
    CREATE TABLE corrected_customers AS
    SELECT CustomerID,
           Age,
           COALESCE(
             LAG(Age, 2) OVER (PARTITION BY Gender ORDER BY CustomerID),
             FIRST_VALUE(Age) OVER (PARTITION BY Gender ORDER BY CustomerID)
           ) AS CorrectedAge,
           Gender
    FROM customers;
    SELECT * FROM corrected_customers
    """
    return qry


def question_7():
    """
    Create a column in corrected_customers called 'AgeCategory' that categorizes customers by age.
    Age categories should be as follows:
        - `Teen`: CorrectedAge < 20
        - `Young Adult`: 20 <= CorrectedAge < 30
        - `Adult`: 30 <= CorrectedAge < 60
        - `Pensioner`: CorrectedAge >= 60

    Make use of a windows function to assign a rank to each customer based on the total number of repayments per age group. Add this into a "Rank" column.
    The ranking should not skip numbers in the sequence, even when there are ties, i.e. 1,2,2,2,3,4 not 1,2,2,2,5,6
    Customers with no repayments should be included as 0 in the result.

    Return columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender`, `AgeCategory`, `Rank`
    """

    qry = """
    SELECT cc.CustomerID,
           cc.Age,
           cc.CorrectedAge,
           cc.Gender,
           CASE
             WHEN CorrectedAge < 20 THEN 'Teen'
             WHEN CorrectedAge < 30 THEN 'Young Adult'
             WHEN CorrectedAge < 60 THEN 'Adult'
             ELSE 'Pensioner'
           END AS AgeCategory,
           DENSE_RANK() OVER (
               PARTITION BY CASE
                   WHEN CorrectedAge < 20 THEN 'Teen'
                   WHEN CorrectedAge < 30 THEN 'Young Adult'
                   WHEN CorrectedAge < 60 THEN 'Adult'
                   ELSE 'Pensioner'
               END
               ORDER BY COALESCE(r.RepaymentCount,0) DESC
           ) AS Rank
    FROM corrected_customers cc
    LEFT JOIN (
        SELECT CustomerID, COUNT(*) AS RepaymentCount
        FROM repayments
        GROUP BY CustomerID
    ) r ON cc.CustomerID = r.CustomerID
    """
    return qry
# MSSQL / SQL Server Reference

## Key types

- `UNIQUEIDENTIFIER` — UUID/GUID (`NEWID()` or `NEWSEQUENTIALID()`)
- `BIGINT IDENTITY(1,1)` — auto-increment integer PK
- `NVARCHAR(n)` / `NVARCHAR(MAX)` — Unicode strings (use N prefix for literals)
- `DECIMAL(p,s)` — exact decimals
- `DATETIME2` — preferred over `DATETIME` (higher precision, wider range)
- `DATETIMEOFFSET` — timezone-aware timestamps
- `BIT` — boolean (0/1)
- `VARBINARY(MAX)` — binary data

## T-SQL specific syntax

### Variables and blocks

```sql
DECLARE @UserId UNIQUEIDENTIFIER = NEWID();
DECLARE @Count INT;

SELECT @Count = COUNT(*) FROM orders WHERE user_id = @UserId;

IF @Count > 0
BEGIN
    PRINT 'Has orders';
END
ELSE
BEGIN
    PRINT 'No orders';
END
```

### Upsert (MERGE)

```sql
MERGE INTO users AS target
USING (VALUES (@Email, @Name)) AS source (email, name)
ON target.email = source.email
WHEN MATCHED THEN
    UPDATE SET name = source.name, updated_at = GETUTCDATE()
WHEN NOT MATCHED THEN
    INSERT (email, name, created_at, updated_at)
    VALUES (source.email, source.name, GETUTCDATE(), GETUTCDATE())
OUTPUT $action, inserted.id;
```

### Pagination

```sql
-- OFFSET-FETCH (SQL Server 2012+)
SELECT id, email, created_at
FROM users
ORDER BY created_at DESC
OFFSET @PageSize * (@Page - 1) ROWS
FETCH NEXT @PageSize ROWS ONLY;
```

### CTEs

```sql
WITH RecentOrders AS (
    SELECT
        user_id,
        COUNT(*) AS order_count,
        SUM(total) AS total_value
    FROM orders
    WHERE created_at >= DATEADD(DAY, -30, GETUTCDATE())
    GROUP BY user_id
)
SELECT u.email, ISNULL(ro.order_count, 0) AS orders_last_30d
FROM users u
LEFT JOIN RecentOrders ro ON ro.user_id = u.id;
```

### Execution plans

```sql
SET STATISTICS IO ON;
SET STATISTICS TIME ON;

-- Or: view graphical plan
SET SHOWPLAN_XML ON;
GO
SELECT ...
GO
SET SHOWPLAN_XML OFF;
```

## TempDB patterns

```sql
-- Temp table (session-scoped)
CREATE TABLE #TempResults (
    id UNIQUEIDENTIFIER,
    score DECIMAL(10,2)
);
INSERT INTO #TempResults SELECT id, RAND() FROM users;

-- Table variable (lighter, no stats, no parallelism)
DECLARE @Results TABLE (id UNIQUEIDENTIFIER, name NVARCHAR(255));
```

## String functions

```sql
-- Concatenation
SELECT CONCAT(first_name, N' ', last_name) AS full_name FROM users;
-- Or: first_name + N' ' + last_name  (NULL-sensitive)

-- String split (SQL Server 2016+)
SELECT value FROM STRING_SPLIT(@csv, ',');
```

## JSON support (SQL Server 2016+)

```sql
-- Parse JSON
SELECT JSON_VALUE(payload, '$.userId') AS user_id
FROM events;

-- Return as JSON
SELECT id, email FROM users FOR JSON PATH;

-- Check valid JSON
SELECT * FROM events WHERE ISJSON(payload) = 1;
```

## Common naming conventions

- Schema-qualify all objects: `dbo.users`, `dbo.orders`
- Stored procedures: `usp_[Description]`
- Views: `vw_[Description]`
- Triggers: `trg_[Table]_[Action]`
- Indexes: `IX_[Table]_[Columns]`, `UX_[Table]_[Columns]` (unique)

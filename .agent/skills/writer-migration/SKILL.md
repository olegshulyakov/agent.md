---
name: writer-migration
description: >
  Generates database migration scripts with up/down operations, safe for production use, idempotent where
  possible, and including validation queries. Use this skill whenever the user wants to write a database
  migration, add or modify a table or column, rename a field, add an index or constraint, backfill data,
  or asks to "write a migration for this schema change", "create a migration to add this column", "write
  a migration script", "how do I migrate this database change", or "generate an Alembic/Flyway/Liquibase
  migration". Also trigger for "alter this table", "rename this column", "add a foreign key", and "backfill
  this data". Distinct from design-schema (designing structure) and writer-sql (general SQL queries).
---

# writer-migration

Generate **database migration scripts** that are safe for production, include rollback, and follow platform conventions.

## Migration tool detection

Identify the migration tool from context:
1. **Explicit mention**: "Alembic", "Flyway", "Liquibase", "Prisma migrate", "Knex", "TypeORM", "Django migrations", "Rails migrations"
2. **Framework**: FastAPI/SQLAlchemy → Alembic, Django → `manage.py makemigrations`, Spring Boot → Flyway or Liquibase, Rails → `rails generate migration`, Prisma → `prisma migrate`
3. **Default**: Plain SQL with up/down as separate files (most portable)

## Safety principles

Every migration should follow these rules:

**Never drop data in the same step as removing its source:**
```sql
-- ❌ Dangerous: drops column immediately
ALTER TABLE users DROP COLUMN legacy_field;

-- ✅ Safe: deploy in 3 steps
-- Step 1: Stop writing to the column (application change)
-- Step 2: Migration to drop the column
-- Step 3: Clean up old code
```

**Make destructive changes reversible:**
- Drop column → make a down migration to re-add it (even if empty)
- Rename column → use add+copy+drop in phases for zero-downtime

**Large data backfills:**
- Process in batches (never one UPDATE that locks the whole table)
- Include a progress mechanism or log

**Adding NOT NULL columns:**
- Add the column as nullable first, backfill, then add the NOT NULL constraint

## Output format

### Plain SQL (default)

```sql
-- migrations/V20240115_001__add_email_verified_to_users.sql (UP)
-- Description: Add email_verified column to users table with backfill

-- Sanity check: ensure we're running this on the right state
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'users' AND column_name = 'email_verified'
  ) THEN
    -- Add column as nullable first for zero-downtime
    ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;

    -- Backfill existing users (all considered verified since they logged in before)
    UPDATE users SET email_verified = TRUE WHERE created_at < '2024-01-15';

    -- Now add NOT NULL constraint
    ALTER TABLE users ALTER COLUMN email_verified SET NOT NULL;

    -- Add index if queries will filter by this column
    CREATE INDEX CONCURRENTLY idx_users_email_verified ON users(email_verified)
      WHERE email_verified = FALSE;

  END IF;
END $$;
```

```sql
-- migrations/V20240115_001__add_email_verified_to_users.undo.sql (DOWN)
-- Rollback: remove email_verified column

DROP INDEX IF EXISTS idx_users_email_verified;
ALTER TABLE users DROP COLUMN IF EXISTS email_verified;
```

### Alembic (Python)

```python
"""Add email_verified to users

Revision ID: abc123def456
Revises: prev_revision_id
Create Date: 2024-01-15 10:00:00
"""
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    # Add nullable first
    op.add_column('users', sa.Column('email_verified', sa.Boolean(), nullable=True))
    
    # Backfill
    op.execute("UPDATE users SET email_verified = TRUE WHERE created_at < '2024-01-15'")
    op.execute("UPDATE users SET email_verified = FALSE WHERE email_verified IS NULL")
    
    # Apply NOT NULL constraint
    op.alter_column('users', 'email_verified', nullable=False)
    
    # Add index
    op.create_index(
        'idx_users_email_verified',
        'users',
        ['email_verified'],
        postgresql_where=sa.text('email_verified = FALSE')
    )

def downgrade() -> None:
    op.drop_index('idx_users_email_verified', table_name='users')
    op.drop_column('users', 'email_verified')
```

### Prisma migrate

```prisma
// In schema.prisma, add the field:
model User {
  id             Int      @id @default(autoincrement())
  email          String   @unique
  emailVerified  Boolean  @default(false)
  createdAt      DateTime @default(now())
}
// Then run: npx prisma migrate dev --name add_email_verified_to_users
```

### Flyway (Java, SQL)

```sql
-- db/migration/V20240115_001__Add_email_verified_to_users.sql
ALTER TABLE users ADD COLUMN email_verified BOOLEAN NOT NULL DEFAULT FALSE;

UPDATE users SET email_verified = TRUE WHERE created_at < '2024-01-15';

CREATE INDEX CONCURRENTLY idx_users_email_verified ON users(email_verified)
  WHERE email_verified = FALSE;
```

## Common migration patterns

### Add column with NOT NULL and default
```sql
-- Safe pattern for PostgreSQL
ALTER TABLE orders ADD COLUMN status VARCHAR(50);  -- nullable first
UPDATE orders SET status = 'pending' WHERE status IS NULL;
ALTER TABLE orders ALTER COLUMN status SET NOT NULL;
ALTER TABLE orders ALTER COLUMN status SET DEFAULT 'pending';
```

### Rename column (zero-downtime)
```sql
-- Phase 1: Add new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);
UPDATE users SET full_name = name;  -- copy data

-- Phase 2: Deploy app reading from full_name
-- Phase 3: Drop old column
ALTER TABLE users DROP COLUMN name;
```

### Add foreign key safely
```sql
-- Add FK without validating existing data (fast, no lock)
ALTER TABLE orders ADD CONSTRAINT fk_orders_user_id
  FOREIGN KEY (user_id) REFERENCES users(id)
  NOT VALID;  -- PostgreSQL: skips validation of existing rows

-- Validate in a separate step (safe for production)
ALTER TABLE orders VALIDATE CONSTRAINT fk_orders_user_id;
```

### Large table backfill (batched)
```sql
DO $$
DECLARE
  batch_size INT := 1000;
  offset_val INT := 0;
  rows_updated INT;
BEGIN
  LOOP
    UPDATE orders
    SET total_cents = (total * 100)::INT
    WHERE id IN (
      SELECT id FROM orders
      WHERE total_cents IS NULL
      LIMIT batch_size
    );
    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    EXIT WHEN rows_updated = 0;
    PERFORM pg_sleep(0.1);  -- brief pause between batches
  END LOOP;
END $$;
```

## Validation queries to include

Always add a validation query after the migration to verify correctness:

```sql
-- Post-migration validation
SELECT COUNT(*) as total,
       COUNT(*) FILTER (WHERE email_verified IS NULL) as null_count
FROM users;
-- Expected: null_count = 0
```

## Migration checklist

- [ ] Has an up migration
- [ ] Has a down/rollback migration
- [ ] Large tables: uses `CONCURRENTLY` for index creation (PostgreSQL)
- [ ] Large tables: uses batching for backfills
- [ ] NOT NULL columns: nullable → backfill → NOT NULL (not in one step)
- [ ] Includes post-migration validation query
- [ ] Follows team naming convention (V{date}_{sequence}__{description})
- [ ] Tested on a copy of production data volume before deploying

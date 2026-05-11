---
name: strategy-backup
description: >
  Produces a backup and recovery strategy with schedule, retention policy, restore procedures, RPO/RTO
  targets, and tooling recommendations. Use this skill whenever the user wants to design a backup strategy,
  define data recovery objectives, plan disaster recovery for a database, document restore procedures,
  or asks to "create a backup strategy", "design our disaster recovery plan", "define RPO and RTO",
  "what's a good backup retention policy", "how should we back up our database", "write a backup plan",
  "document our restore procedure", or "test our backup strategy". Also trigger for "PITR setup",
  "point-in-time recovery", "continuous backup", "backup testing", and "data retention policy".
  Distinct from writer-runbook (general operational runbook) and setup-infra (IaC provisioning).
---

# strategy-backup

Produce a **backup and recovery strategy** with RPO/RTO objectives, schedule, retention, tooling, and restore procedures.

## What makes a great backup strategy

A backup strategy is only as good as its last successful restore. The most common mistake is planning backups without planning or testing restores. A good strategy is specific enough to be actionable, realistic about RTO given team size and infrastructure, and tested regularly.

## Information gathering

From context, identify:
- **Data stores**: Databases (PostgreSQL, MySQL, MongoDB), object storage, file systems, configs?
- **Data criticality**: What's the cost of an hour of data loss? A day? Compliance requirements?
- **Current backup state**: Existing solution or greenfield?
- **Infrastructure**: Cloud provider (AWS/GCP/Azure)? On-prem? Kubernetes?
- **Team size**: Who's responsible for backup monitoring and restore?

## Output format

```markdown
# Backup & Recovery Strategy: [System / Service Name]

**Date:** [date]
**Owner:** [team]
**Review cycle:** [annually / after major incidents]

---

## Recovery Objectives

| Objective | Target | Rationale |
|-----------|--------|-----------|
| **RPO** (Recovery Point Objective) | [e.g., 1 hour] | Maximum acceptable data loss. Data changes more frequently → lower RPO needed. |
| **RTO** (Recovery Time Objective) | [e.g., 4 hours] | Maximum acceptable downtime. Critical services → lower RTO. |
| **MTTR** (Mean Time To Recovery) | [target] | Actual average recovery time; measure and improve over time. |

**Business context:** [Why these targets — compliance requirement? SLA with customers? Business impact of downtime?]

---

## Data Inventory

| Data Store | Type | Size | Change Rate | Criticality | Location |
|------------|------|------|------------|-------------|----------|
| `orders_db` | PostgreSQL 15 | [X GB] | [high/med/low] | 🔴 Critical | [AWS RDS us-east-1] |
| `user_files` | AWS S3 | [X TB] | [medium] | 🟠 High | [S3 bucket] |
| `config_store` | etcd / Git | [small] | [low] | 🟠 High | [GitHub] |
| `analytics_db` | BigQuery | [X TB] | [medium] | 🟡 Medium | [GCP] |

---

## Backup Schedule

| Data Store | Full Backup | Incremental | WAL/Binlog | Retention |
|------------|-------------|-------------|------------|-----------|
| `orders_db` | Weekly (Sun 02:00 UTC) | Daily (02:00 UTC) | Continuous (15-min archive) | 30 days full, 7 days WAL |
| `user_files` | — | Daily (S3 replication) | — | 90 days versioning |
| `config_store` | On every commit (Git) | — | — | Forever (Git history) |

### Backup types explained

- **Full backup**: Complete snapshot of all data. Slowest to create, fastest to restore.
- **Incremental**: Only changes since last full or incremental. Fast to create, requires chain to restore.
- **WAL/binlog archiving**: Continuous stream of database changes. Enables PITR (point-in-time recovery).
- **Snapshot**: Storage-level copy (e.g., AWS EBS snapshot, RDS automated backup). Near-instant.

---

## Tooling

| Data Store | Backup Tool | Storage | Monitoring |
|------------|------------|---------|------------|
| PostgreSQL | `pg_dump` / `pgBackRest` / AWS RDS automated | S3 bucket (versioned, cross-region) | CloudWatch backup metrics |
| MySQL | `mysqldump` / Percona XtraBackup | S3 | |
| MongoDB | `mongodump` / Atlas backups | Atlas S3 | |
| Files / assets | AWS S3 versioning + CRR | Cross-region S3 | S3 bucket metrics |
| Kubernetes configs | Velero + etcd snapshot | S3 | |

### PostgreSQL backup with pgBackRest

```bash
# Install pgBackRest
apt-get install pgbackrest

# /etc/pgbackrest.conf
[global]
repo1-path=/var/lib/pgbackrest
repo1-retention-full=4          # Keep 4 full backups
repo1-retention-archive=7       # Keep 7 days of WAL
repo1-cipher-type=aes-256-cbc  # Encrypt backups

[mydb]
pg1-path=/var/lib/postgresql/15/main

# Full backup (run weekly via cron)
pgbackrest --stanza=mydb backup --type=full

# Incremental backup (run daily)
pgbackrest --stanza=mydb backup --type=incr

# Enable WAL archiving (postgresql.conf)
archive_mode = on
archive_command = 'pgbackrest --stanza=mydb archive-push %p'
```

---

## Backup Storage

### Storage requirements

| Backup type | Storage estimate | Calculation |
|-------------|-----------------|-------------|
| Full backups | [X] | [DB size × retention weeks] |
| WAL archives | [X] | [daily WAL size × 7 days] |
| Total | [X] | + 20% buffer |

### Storage configuration

```hcl
# Terraform: S3 backup bucket
resource "aws_s3_bucket" "db_backups" {
  bucket = "myorg-db-backups-${var.environment}"
}

resource "aws_s3_bucket_versioning" "db_backups" {
  bucket = aws_s3_bucket.db_backups.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_lifecycle_configuration" "db_backups" {
  bucket = aws_s3_bucket.db_backups.id
  rule {
    id = "backup-retention"
    status = "Enabled"
    expiration { days = 90 }
    transition {
      days = 30
      storage_class = "GLACIER"  # Move to cheaper storage after 30 days
    }
  }
}
```

### Geo-redundancy

- Primary backups: [Region A]
- Replication: [Region B] — replicate within [4 hours]
- Cross-account: Consider separate AWS account for backup isolation

---

## Restore Procedures

### Runbook: Full database restore (PostgreSQL)

**Estimated RTO:** [2–4 hours] | **Prerequisites:** DB instance available, pgBackRest configured

```bash
# Step 1: Stop application servers (prevent new writes)
systemctl stop myapp

# Step 2: List available backups
pgbackrest --stanza=mydb info

# Step 3a: Restore from latest backup
pgbackrest --stanza=mydb restore

# Step 3b: Point-in-time restore (if you know the target time)
pgbackrest --stanza=mydb restore \
  --target="2024-01-15 14:30:00" \
  --target-action=promote

# Step 4: Start PostgreSQL
systemctl start postgresql

# Step 5: Verify data integrity
psql -U postgres -d mydb -c "SELECT count(*) FROM orders;"
psql -U postgres -d mydb -c "SELECT max(created_at) FROM orders;"

# Step 6: Restart application
systemctl start myapp

# Step 7: Monitor error logs for 30 minutes
tail -f /var/log/myapp/error.log
```

### Runbook: Table-level restore (accidental delete)

```bash
# Restore to a separate database at the point just before the accident
pgbackrest --stanza=mydb restore \
  --target="2024-01-15 09:58:00" \
  --target-action=promote \
  --db-path=/var/lib/postgresql/15/restore_temp

# Extract the specific table
pg_dump -U postgres -d restored_db -t orders > orders_recovery.sql

# Apply to production
psql -U postgres -d mydb < orders_recovery.sql
```

---

## Backup Testing

A backup that hasn't been restored is just a hope. Test regularly:

| Test | Frequency | Process | Owner |
|------|-----------|---------|-------|
| **Full restore drill** | Quarterly | Restore to staging environment; verify app works | DBA + DevOps |
| **Automated restore test** | Weekly | Script restores latest backup to temp instance; queries data | CI/CD automation |
| **PITR test** | Monthly | Restore to specific timestamp; verify record counts | DBA |
| **Cross-region restore** | Bi-annually | Restore from geo-replica backup | DevOps |

### Automated restore test (CI/CD)

```bash
#!/bin/bash
# backup_test.sh — run weekly via cron or CI
set -euo pipefail

TEMP_DB="backup_test_$(date +%Y%m%d)"

echo "Testing backup restore..."

# Restore to temp DB
pgbackrest --stanza=mydb restore \
  --db-path=/var/lib/postgresql/15/$TEMP_DB

# Start temp Postgres instance and verify
pg_ctlcluster 15 $TEMP_DB start
RECORD_COUNT=$(psql -U postgres -d mydb -h /tmp -c "SELECT count(*) FROM orders;" -t)

if [ "$RECORD_COUNT" -gt 0 ]; then
  echo "✅ Backup test passed: $RECORD_COUNT orders found"
else
  echo "❌ Backup test FAILED: No records found"
  alert_ops "Backup restore test failed"
  exit 1
fi

# Cleanup
pg_ctlcluster 15 $TEMP_DB stop
pg_dropcluster 15 $TEMP_DB
```

---

## Monitoring & Alerting

| Alert | Trigger | Severity | Response |
|-------|---------|----------|----------|
| Backup missed | No backup in [24h] | 🔴 Critical | Investigate immediately; run manual backup |
| Backup size anomaly | Size changes > 30% | 🟠 High | Investigate data growth or backup corruption |
| Restore test failed | Weekly test fails | 🔴 Critical | Test backup integrity; validate restore chain |
| Replication lag | Cross-region lag > [2h] | 🟠 High | Check network; verify replication is running |
| Storage >80% full | Backup storage >80% | 🟠 High | Clean old backups; increase storage |

---

## Compliance & Retention

| Regulation | Requirement | Implementation |
|------------|-------------|----------------|
| GDPR | Right to erasure | Document backup purge process; automate deletion |
| SOC 2 | Backup monitoring + testing | Keep test logs; audit quarterly |
| HIPAA | Encrypted backups, access logs | AES-256 encryption; CloudTrail logging |
| [Internal policy] | [7-year financial data retention] | Archive to Glacier; separate bucket |

---

## Responsibilities

| Role | Responsibility |
|------|----------------|
| DBA | Configure and maintain backup tools; run restore drills |
| DevOps | Backup storage, monitoring, alerting, CI test |
| Security | Encryption keys, access control |
| Engineering lead | Review strategy annually; approve RPO/RTO targets |
| On-call engineer | Respond to backup failure alerts; initiate restore |
```

## Calibration

- **Managed database (RDS, Cloud SQL)**: Focus on built-in backup features, PITR configuration, cross-region replication
- **On-prem**: More emphasis on tooling selection and manual configuration
- **Compliance-heavy (HIPAA/SOC2)**: Add encryption, audit trail, and retention compliance sections
- **Disaster recovery focus**: Emphasize RTO, geo-redundancy, and full restore drills

# Supabase keepalive runbook

## Purpose

Prevent the Free Supabase project `dialectic-os` from being automatically paused
during periods without normal application traffic.

## Components

- Database probe: `public.system_keepalive`, containing one immutable row.
- Access control: RLS permits `SELECT` to `anon` and `authenticated`; no public
  insert, update, or delete privileges are granted.
- Scheduler: `.github/workflows/supabase-keepalive.yml`.
- Frequency: three database reads per day at 02:17, 10:17, and 18:17 UTC.

The workflow uses the Supabase publishable key. This key is designed for client
exposure and can only perform operations allowed by PostgreSQL grants and RLS.
No `service_role` or secret key is used.

## Validation

A successful workflow run must return exactly:

```json
[{"id":1}]
```

Any HTTP error, timeout, permission failure, missing row, or unexpected response
fails the job. GitHub retains the result in the Actions history.

Scheduled workflows execute from the repository default branch. After this change
is merged, confirm the first scheduled run under **Actions > Supabase Keepalive**.

## Manual execution

Open **Actions > Supabase Keepalive > Run workflow**. The workflow also runs once
when its file is first published on `agent/supabase-keepalive`.

## Removal

Delete the workflow and apply a new migration containing:

```sql
drop table public.system_keepalive;
```

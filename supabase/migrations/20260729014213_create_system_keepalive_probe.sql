create table public.system_keepalive (
  id smallint primary key,
  created_at timestamptz not null default now(),
  constraint system_keepalive_singleton check (id = 1)
);

comment on table public.system_keepalive is
  'Read-only probe used by scheduled external requests to keep the Free project active.';

alter table public.system_keepalive enable row level security;

revoke all on table public.system_keepalive from anon, authenticated;
grant select on table public.system_keepalive to anon, authenticated;

create policy "Allow keepalive probe reads"
on public.system_keepalive
for select
to anon, authenticated
using (id = 1);

insert into public.system_keepalive (id) values (1);

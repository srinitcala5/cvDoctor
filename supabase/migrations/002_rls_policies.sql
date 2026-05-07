-- CVDOC-9: Row-level security — users see only their own rows
-- Enable RLS on both tables
alter table public.resumes enable row level security;
alter table public.scan_results enable row level security;

-- resumes: full CRUD for the owning user only
create policy "resumes: owner select"
    on public.resumes for select
    using (auth.uid() = user_id);

create policy "resumes: owner insert"
    on public.resumes for insert
    with check (auth.uid() = user_id);

create policy "resumes: owner update"
    on public.resumes for update
    using (auth.uid() = user_id)
    with check (auth.uid() = user_id);

create policy "resumes: owner delete"
    on public.resumes for delete
    using (auth.uid() = user_id);

-- scan_results: full CRUD for the owning user only
create policy "scan_results: owner select"
    on public.scan_results for select
    using (auth.uid() = user_id);

create policy "scan_results: owner insert"
    on public.scan_results for insert
    with check (auth.uid() = user_id);

create policy "scan_results: owner update"
    on public.scan_results for update
    using (auth.uid() = user_id)
    with check (auth.uid() = user_id);

create policy "scan_results: owner delete"
    on public.scan_results for delete
    using (auth.uid() = user_id);

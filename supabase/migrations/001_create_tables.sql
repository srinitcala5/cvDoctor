-- CVDOC-9: Create tables with user-scoped ownership
-- resumes: stores uploaded resume text per user
create table if not exists public.resumes (
    id          uuid primary key default gen_random_uuid(),
    user_id     uuid not null references auth.users(id) on delete cascade,
    filename    text not null,
    text        text not null,
    page_count  integer not null default 1,
    created_at  timestamptz not null default now()
);

-- scan_results: stores scoring/analysis outputs per resume
create table if not exists public.scan_results (
    id          uuid primary key default gen_random_uuid(),
    user_id     uuid not null references auth.users(id) on delete cascade,
    resume_id   uuid references public.resumes(id) on delete cascade,
    scan_type   text not null check (scan_type in ('resume_score', 'jd_gap', 'cover_letter', 'linkedin', 'pitch')),
    payload     jsonb not null,
    created_at  timestamptz not null default now()
);

create index if not exists resumes_user_id_idx on public.resumes(user_id);
create index if not exists scan_results_user_id_idx on public.scan_results(user_id);
create index if not exists scan_results_resume_id_idx on public.scan_results(resume_id);

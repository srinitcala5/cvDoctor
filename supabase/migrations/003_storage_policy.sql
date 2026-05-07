-- CVDOC-9: Storage bucket scoped to auth.uid()
-- Run after creating the 'resumes' bucket in the Supabase dashboard.
-- Bucket name: resumes (private, not public)

-- Each user's files live under their own UID prefix: resumes/<uid>/filename.pdf

insert into storage.buckets (id, name, public)
values ('resumes', 'resumes', false)
on conflict (id) do nothing;

-- Users can only read their own files
create policy "storage: owner read"
    on storage.objects for select
    using (
        bucket_id = 'resumes'
        and auth.uid()::text = (storage.foldername(name))[1]
    );

-- Users can only upload to their own prefix
create policy "storage: owner insert"
    on storage.objects for insert
    with check (
        bucket_id = 'resumes'
        and auth.uid()::text = (storage.foldername(name))[1]
    );

-- Users can delete their own files
create policy "storage: owner delete"
    on storage.objects for delete
    using (
        bucket_id = 'resumes'
        and auth.uid()::text = (storage.foldername(name))[1]
    );

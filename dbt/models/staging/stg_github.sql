{{ config(materialized="view") }}

select 
    users,	
    repo_name,
    type,

    cast(id	as integer) as id,
    cast(public	as boolean) as public,
    cast(created_at	as timestamp) as created_at,
    cast(repo_id as integer) as repo_id,
    cast(org_exists	as boolean) as org_exists,
    cast(count_commits as integer) as count_commits	
    
from {{ source("staging", "github_data") }}
{{ config(materialized="table") }}

with gh_2015_data as (
    select 
        *
    from {{ ref("stg_2015_data") }}

),

gh_2020_data as (
    select 
        *
    from {{ ref("stg_2020_data") }}

),

gh_data as (
    select * from gh_2015_data
    UNION ALL
    select * from gh_2020_data
)

select
    gh_data.users,	
    gh_data.repo_name,
    gh_data.type,

    gh_data.id,
    gh_data.public as public_repo,
    gh_data.created_at,
    gh_data.repo_id,
    gh_data.org_exists,
    gh_data.count_commits,

    FORMAT_DATE('%H', created_at) AS hour,
    FORMAT_DATE('%A', created_at) AS dayOfTheWeek,
    FORMAT_DATE('%d', created_at) AS day,
    FORMAT_DATE('%b', created_at) AS month,
    FORMAT_DATE('%G', created_at) AS year

from gh_data


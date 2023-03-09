{{ config(materialized="table") }}

with gh_2015_data as (
    select 
        *
    from {{ ref("stg_2015_data") }}
    limit 10

),

gh_2020_data as (
    select 
        *
    from {{ ref("stg_2020_data") }}
    limit 10

),

gh_data as (
    select * from gh_2015_data
    UNION
    select * from gh_2020_data
    limit 30
)

select
    gh_data.users,	
    gh_data.repo_name,
    gh_data.type,

    gh_data.id
    gh_data.public_repo,
    gh_data.created_at as datetime,
    gh_data.repo_id,
    gh_data.org_exists,
    gh_data.count_commits,

    YEAR(datetime) AS year,
    MONTH(datetime) AS month,
    DAY(datetime) AS day,
    DATEPART(weekday, datetime) as dayOfTheWeek,
    DATEPART(hour, datetime) as hourOfTheDay

from gh_data
limit 50

from omymodels import create_models

ddl = """
drop table if exists v2.entitlement_requests ;
CREATE table v2.entitlement_requests (
    job_id                decimal(21) not null
   ,id                    varchar(100) not null -- group_id or role_id
   ,type                  varchar(50) not null -- if type is 'group' then id column is the group_id, if type is 'role' then id is the role_id
   ,user_id               varchar(100) not null -- the user_id (sso) that wants access
   ,first_name            varchar(100) not null -- first name of user that requests data access
   ,last_name             varchar(100) not null -- last name of user that requests data access
   ,request_time          timestamp not null default now()
   ,status_update_time    timestamp null 
   ,status                varchar(10) not null default 'requested'  -- status is one of: requested, approved, or denied
   ,notes                 varchar(2000) not null default 'none' -- optional requestor notes
   ,requestor_id          varchar(100) not null -- the user_id (sso) who submitted request for himself or on behalf of another user
) ;
create unique index entitlement_requests_pk on v2.entitlement_requests (job_id, id, type) ;
"""
result = create_models(ddl)
print(result)

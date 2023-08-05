from simple_ddl_parser import DDLParser


ddl = """

CREATE table v2.entitlement_requests (
   status                varchar(10) not null default 'requested'  -- inline comment
   ,notes                 varchar(2000) not null default 'none' -- inline comment
   ,id          varchar(100) not null -- inline comment
) ;
"""

result = DDLParser(ddl).run()
import pprint
pprint.pprint(result)

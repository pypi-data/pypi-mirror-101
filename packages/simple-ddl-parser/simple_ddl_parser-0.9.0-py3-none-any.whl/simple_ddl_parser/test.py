from simple_ddl_parser import DDLParser


ddl = """

create table ChildTableName(
        parentTable varchar
        );
ALTER TABLE ChildTableName 
ADD CONSTRAINT "fk_t1_t2_tt"
  FOREIGN KEY ("parentTable")
  REFERENCES parentTable ("columnName")
  ON DELETE CASCADE
  ON UPDATE CASCADE;
"""

result = DDLParser(ddl).run()
import pprint
pprint.pprint(result)
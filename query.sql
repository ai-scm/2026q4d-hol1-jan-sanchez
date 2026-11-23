SELECT * FROM "AwsDataCatalog"."bld-tseed-workshop-jan-sanchez"."jan_sanchez"
WHERE try_cast(age AS integer) > 35 AND languages LIKE '%English%'
-- -----------------------------------------------------------------------------
-- -----------------------------------------------------------------------------
--  Author			: Jesus Baizabal
--  email		        : baizabal.jesus@gmail.com
--  Create date			: October 27, 2022
--  Description			: Build tables , procedures and triggers for bms module
--  TODO		        : clean
--  @Last_patch			: --
--  @license			: MIT License (http://www.opensource.org/licenses/mit-license.php)
--  Database owner		: Jesus Baizabal
--  @status			: Stable
--  @version			: 0.0.1
-- Copyright © 2022, UES devops - portalapps.com, All Rights Reserved
-- -----------------------------------------------------------------------------
-- Description:        This tables controls the behaviour of bms modulo describes the book and set's
-- 		       the inputs way for the user and set it's positions in the page
--		       the components manipulates the forms values and css of the inputs   
-- Call by:            [schema.usp_ProcThatCallsThis -- --> undefined]
--                     [BMS Book Manager System]
--                     [Job -- --> undefined]
--                     [PLC/Interface -- --> undefined]
-- Affected table(s):  [schema.TableModifiedByProc1]
--                     [schema.TableModifiedByProc2]
-- Used By:            Functional Area this is use in :
--                     learner/content/content/{book_id}
-- Parameter(s):       @param1 - description and usage
--                     @param2 - description and usage
-- Usage:              EXEC dbo.usp_DoSomeStuff
--                         @param1 = 1,
--                         @param2 = 3,
--                         @param3 = 2
--                     Additional notes or caveats about this object, like where is can and cannot be run, or
--                     gotchas to watch for when using it.
-- INSTALL mysql --user=user --password=pass db_ediq2021 < mariadb/panamericano/bms.sql
-- -----------------------------------------------------------------------------

-- Static and inherits for all books
-- NOTE

create or replace table `bms_controls_files`(
        `id`                          int unsigned not null auto_increment primary key,
        `user_id`                     int null,
        `labelname`                   char(255) null,
        `file_name`                   varchar(255),
        `pathname`                   char(255) null,
        `extname`                    char(10) null,
        `md5sum`                     varchar(255),
        `file_size`                  char(255),
        `atime`                      varchar(150),
        `mtime`                      varchar(150),
        `ctime`                      varchar(150),
        `username`                   varchar(50),
        `datetime_login`             datetime null,
        `ip_remote`                  varchar(25),
        `created`                     datetime null,
        `modified`                    datetime null,
        `status`                     bool not null default true
)engine=InnoDB default charset=utf8mb4;

select 'building tables';


select 'building tables bms_books ...';
create or replace table `bms_books` (
  `id`                      int unsigned not null auto_increment primary key, 
  `book_id`                 int unsigned not null , -- --> ex: 228
  `pages`                   int null, -- --> 8 total pages
  `book_name`               varchar(255) null, -- --> Guia_UV
  `is_url`		    bool not null default false, -- --> means false is path url/{book_id} else url?book_id={id}&var=foo
  `created`                 datetime,
  `modified`                datetime,
  `status`                  bool not null default true
)engine=InnoDB default charset=utf8mb4;

select 'building tables bms_bookpages ...';

-- UPDATE messages SET message = REPLACE(REPLACE(REPLACE(message,'&','&amp;'),'<', '&lt;'), '>', '&gt;')

create or replace table `bms_bookpages` (
  `id`                      int unsigned not null auto_increment primary key,
  `bms_books_id`            int unsigned not null , 		-- --> ex: 228
  `book_pages`              int not null ,  		-- --> [1,2,3,4,5,6...234] pages per row
-- --> NOTE : when build basename{https:// || /dir/} + pathname 
  `ext_basename`	    varchar(255) null,
  `basename`                varchar(255) null, 		-- --> /src/bms/src
  `pathname`                varchar(255) null, 		-- -->  /book-source/guia/unam/001/pages/36.jpg 
  `created`                 datetime,
  `modified`                datetime,
  `status`                  bool not null default true
)engine=InnoDB default charset=utf8mb4;

-- update basename set basename =  REPLACE(REPLACE(REPLACE(message,'&','&amp;'),'<', '&lt;'), '>', '&gt;') from bms_bookpages 

select 'building tables bms_positions ...';
--  css positions by book and page 
create or replace table `bms_positions` (
  `id`                      int unsigned not null auto_increment primary key,
  `bms_books_id`            int unsigned not null , 		-- --> ex: 228
  `bms_bookpages_id`        int unsigned not null ,   -- --> [1,2,3,4,5,6...234] pages per row
  `page`                    int not null,
  `tagpath`		    varchar(255) null , -- --> .page_x > form > 
  `tag`		    	    varchar(255) null , -- --> tag : #a1
  `top`			    varchar(255) null , -- --> from  upper-left of an element to down to object
  `left`		    varchar(255) null , -- --> from left of a element to left of an object 
  `width`		    varchar(255) null , -- --> whidth of an object {input}
  `css`                     text null,  -- --> fallback code : pages_5 > form > #a{top:70.2%;left:190px;width:3%;}
  `created`                 datetime,
  `modified`                datetime,
  `status`                  bool not null default true
)engine=InnoDB default charset=utf8mb4;

/* color: "DeepSkyBlue" */
/* lineWidth: 1 */
/* source_height: 1445 */
/* source_width: 1170 */
/* type: "text" */
/* x1: 531 */
/* x2: 656 */
/* y1: 541 */
/* y2: 631 */

create or replace table `bms_src_positions`(
  `id`                      int unsigned not null auto_increment primary key,
  `bms_books_id`            int unsigned not null , 		-- --> ex: 228
  `bms_bookpages_id`        int unsigned not null ,   -- --> [1,2,3,4,5,6...234] pages per row
  `color`		    varchar(255) null , -- --> tag : #a1
  `lineWidth`		    int null , -- --> tag : #a1
  `source_width`	    varchar(255) null , -- --> tag : #a1
  `source_height`   	    varchar(255) null , -- --> tag : #a1
  `default_width`   	    varchar(255) null , -- --> tag : #a1
  `default_height`   	    varchar(255) null , -- --> tag : #a1
  `inputType`	    	    varchar(255) null , -- --> tag : #a1
  `page`                    int null,
  `x1`			    decimal(18,6) null , -- --> left
  `y1`			    decimal(18,6) null , -- --> top
  `x2`			    decimal(18,6) null , -- --> width
  `y2`			    decimal(18,6) null , -- --> height
  `created`                 datetime not null default now(),
  `modified`                datetime,
  `status`                  bool not null default true

)engine=InnoDB default charset=utf8mb4;




select 'building tables bms_inputs_ctrls ...';

create or replace table `bms_inputs_ctrls` (
  `id`                      int unsigned not null auto_increment primary key,
  `bms_books_id`            int unsigned not null , 		-- --> ex: 228
  `bms_bookpages_id`        int unsigned not null ,
  `label`                   text null,
  `created`		    datetime,
  `modified`                datetime,
  `status`                  bool not null default true
)engine=InnoDB default charset=utf8mb4;


select 'building tables bms_inputs_pages ...';
-- Define inputs by book and page
create or replace table `bms_inputs_pages` (
  `id`                      int unsigned not null auto_increment primary key,
  `bms_inputs_ctrls_id`     int unsigned not null , 		-- --> ex: 
  `attribute`		    varchar(255) null , -- --> [name,id,autofocus,class,disabled,[fk]value]
  `value`		    varchar(255) null , -- --> [somename,on,saved,true,[fk]{...response}]
  `created`		    datetime,
  `modified`                datetime,
  `status`                  bool not null default true
)engine=InnoDB default charset=utf8mb4;



select 'building tables bms_inputs_values ...';
create or replace table `bms_inputs_values` (
  `id`                      int unsigned not null auto_increment primary key,
  `bms_inputs_ctrls_id`     int unsigned not null , 		-- --> ex: 228
  `user_id` 		    int unsigned not null ,
  `attribute`		    varchar(255) null , -- --> [name,id,autofocus,class,disabled,[fk]value]
  `value`		    text null , -- --> [somename,on,saved,true,[fk]{...response}]
  `created`		    datetime,
  `modified`                datetime,
  `status`                  bool not null default true
)engine=InnoDB default charset=utf8mb4;

-- LOG and CACHE tables 

-- NOTE Users associated with the inputs 

select 'building tables bms_cache_books ...';
create or replace table `bms_cache_books` (
  `id`                      int unsigned not null auto_increment primary key, -- --> Cual es el pedo?
  `book_id`                 varchar(255) not null , -- --> ex: 228
  `pages`                   int null, -- --> 8 total pages
  `book_name`               varchar(255) null, -- --> Guia_UV
  `is_url`		    bool not null default false, -- --> means false is path url/{book_id} else url?book_id={id}&var=foo
  `user_id` 		    int unsigned not null ,
  `created`                 datetime
)engine=InnoDB default charset=utf8mb4;
  

-- select 'building tables bms_cache_inputs_ctrls ...';
-- create or replace table `bms_cache_inputs_ctrls`(
--   `id`                      int unsigned not null auto_increment primary key,
--   `bms_inputs_ctrls_id`     int unsigned not null ,
--   `bms_books_id`	    int unsigned not null , 		-- --> ex: 228
--   `bms_bookpages_id`	    int unsigned not null , 
--   `user_id` 		    int unsigned not null ,
--   `label`                   text null,
--   `created`		    datetime
-- )engine=InnoDB default charset=utf8mb4;
-- 
-- 
-- select 'building tables bms_cache_inputs_pages ...';
-- -- Define cache inputs by book and page
-- create or replace table `bms_cache_inputs_pages` (
--   `id`                      int unsigned not null auto_increment primary key,
--   `bms_inputs_ctrls_id`     int unsigned not null , 		-- --> ex: 228
--   `bms_books_id`            int unsigned not null , 		-- --> ex: 228
--   `bms_bookpages_id`        int unsigned not null ,
--   `user_id` 		    int unsigned not null ,
--   `attribute`		    varchar(255) null , -- --> [name,id,autofocus,class,disabled,[fk]value]
--   `value`		    varchar(255) null , -- --> [somename,on,saved,true,[fk]{...response}]
--   `created`		    datetime
-- )engine=InnoDB default charset=utf8mb4;

-- create or replace table `bms_cache_view_users_inputs` (
--   `id`                      int unsigned not null auto_increment primary key,
--   `input_id`		    int unsigned not null , 
--   `book_id`		    int unsigned not null , 	
--   `bms_bookpages_id`        int unsigned not null ,
--   `label`                   text null,
--   `user_id` 		    int unsigned not null ,
--   `attribute`		    varchar(255) null ,
--   `value`		    varchar(255) null ,
--   `created`		    datetime
-- )engine=InnoDB default charset=utf8mb4;

 select 'Creating the procedures ...';
-- note procedure fro creating the cache table input-usr
-- steps of the procedure 
-- clean the bms_cache_inputs_ctrls
-- insert updated data into
-- release 
-- DELIMITER //
-- TODO Create index for cache tables
CREATE OR REPLACE PROCEDURE bms_proc_build_cache_inp_usr  (
--  OUT param1 CHAR(10) CHARACTER SET 'utf8' COLLATE 'utf8_bin'
 )
 BEGIN
  if (select count(user_id) from `db_ediq2021`.`bms_cache_books`) > 0 then
   truncate table `db_ediq2021`.`bms_cache_books`;
  end if;

  select 'Building bms_cache_books ...';

  insert into `db_ediq2021`.`bms_cache_books`
       select 
	   null            
	  ,`book`.`book_id`       
	  ,`book`.`pages`         
	  ,`book`.`book_name`     
	  ,`book`.`is_url`	
	  ,`usr`.`user_id` 	
	  ,now()
      from 
	  `db_ediq2021`.bms_books as `book`
      cross join 
	  `db_ediq2021`.system_users as `usr`
	on 
	  `usr`.first_name <> 'DEMO';

  -- if (select count(user_id) from `db_ediq2021`.`bms_cache_inputs_ctrls`) > 0 then
  --  truncate table `db_ediq2021`.`bms_cache_inputs_ctrls`;
  -- end if;
  -- 
  -- select 'Building bms_cache_inputs_ctrls ...';
  -- 
  --  insert into `db_ediq2021`.`bms_cache_inputs_ctrls` 
  --     select 
  -- 	 null	
  -- 	,`input`.`id`   -- --> for visualization
  -- 	,`input`.bms_books_id
  -- 	,`input`.bms_bookpages_id
  -- 	,`usr`.user_id 
  -- 	,`input`.label
  -- 	,now()
  --     from 
  -- 	`db_ediq2021`.bms_inputs_ctrls as `input`
  --     cross join 
  -- 	`db_ediq2021`.system_users as `usr`
  --       on 
  -- 	`usr`.first_name <> 'DEMO';
  -- 
  -- -- Layer of inputs pages per usr
  -- 
  -- if (select count(user_id) from `db_ediq2021`.`bms_cache_inputs_pages`) > 0 then
  --  truncate table `db_ediq2021`.`bms_cache_inputs_pages`;
  -- end if;
  -- 
  -- select 'Building bms_cache_inputs_pages ...';
  -- 
  --  insert into `db_ediq2021`.`bms_cache_inputs_pages`
  --   select
  --           null
  -- 	,`input`.bms_inputs_ctrls_id
  -- 	,`input`.bms_books_id
  -- 	,`input`.bms_bookpages_id
  -- 	,`input`.user_id
  --  	,`inpages`.attribute
  --  	,`inpages`.value
  -- 	,now()
  --   from 
  --  	-- `bms_inputs_ctrls` as input  -- `bms_inputs_ctrls` 	
  --  	`bms_cache_inputs_ctrls` as input  -- `bms_inputs_ctrls` 	
  --        left join 
  --  	  `bms_inputs_pages` as inpages
  --  	on `input`.bms_inputs_ctrls_id = `inpages`.bms_inputs_ctrls_id;
  -- 


  -- note bms_view_users_inputs

  -- if (select count(id) from `db_ediq2021`.`bms_cache_view_users_inputs`) > 0 then
  --  truncate table `db_ediq2021`.`bms_cache_view_users_inputs`;
  -- end if;
  -- 
  -- -- NOTE well this is imposible in mysql
  --  select 'Building bms_cache_view_users_inputs ...';
  --  
  --  insert into `db_ediq2021`.`bms_cache_view_users_inputs`
  --     select
  --  	 null
  --  	,`cache_view`.`input_id`		   
  --  	,`cache_view`.`book_id`		   
  --  	,`cache_view`.`bms_bookpages_id`       
  --  	,`cache_view`.`label`                  
  --  	,`cache_view`.`user_id` 		   
  --  	,`cache_view`.`attribute`		   
  --  	,`cache_view`.`value`		   
  --  	,now()
  --     from
  --      `db_ediq2021`.`bms_view_users_inputs` as cache_view;
 
END;
-- //




select 'Creating views ...';
-- NOTE The view 
create or replace view bms_view_inputs as 
    select 
	  ROWNUM() as id
	,`covers`.book_id
	,`covers`.book_name
	,`covers`.is_url
	,`pages`.book_pages
	,concat(`pages`.basename , `pages`.pathname ) as 'path'
	,`pos`.css
    from `bms_books` as covers
      inner join 
	 `bms_bookpages` as pages
	on `covers`.book_id = `pages`.bms_books_id
      left join 
	  `bms_positions` as pos
	on 
	  `covers`.book_id = `pos`.bms_books_id 
      and 
	`pages`.id = `pos`.bms_bookpages_id
      order by `pages`.book_pages;

-- select 'building views bms_view_users_inputs ...';
-- create or replace view bms_view_users_inputs as 
-- -- NOTE first the static map of attributes per user
-- -- TODO optimize this query
--  with usr_input as (
--    select
-- 	 `input`.bms_inputs_ctrls_id as input_id
--  	,`input`.bms_books_id as book_id
--  	,`input`.bms_bookpages_id as bms_bookpages_id
--   	,`input`.label as label
--  	,`input`.user_id as user_id
--   	,`inpages`.attribute as attribute
--   	,`inpages`.value as value
--    from 
--   	`bms_cache_inputs_ctrls` as input	
--  -- NOTE adding inputs an his assosiates values by user	
--         left join -- static inputs attributes
--   	  `bms_cache_inputs_pages` as inpages
--   	on
--  	`input`.bms_inputs_ctrls_id = `inpages`.bms_inputs_ctrls_id
--  	and
--  	  `input`.user_id = `inpages`.user_id
--   	and 
--   	  `input`.bms_books_id = `inpages`.bms_books_id
--   	and
--   	  `input`.bms_bookpages_id = `inpages`.bms_bookpages_id
--  union all
--  select 
-- 	 `input`.id as input_id
--  	,`input`.bms_books_id as book_id
--  	,`input`.bms_bookpages_id as bms_bookpages_id
--   	,`input`.label as label
--   	,`data`.user_id as user_id
--   	,`data`.attribute as attribute
--   	,`data`.value as value
--  from 
--  	`bms_inputs_ctrls` as input
--          inner join 
--  -- NOTE the filter of users_id avoid the multiplication of data
--   	  `bms_inputs_values` as data
--   	on `input`.id = `data`.bms_inputs_ctrls_id
--       )
-- select 
-- 	  rownum() as id
--       	,`input`.input_id
--  	,`input`.book_id
--  	,`input`.bms_bookpages_id
--   	,`input`.label
--   	,`input`.user_id
--   	,`input`.attribute
--   	,`input`.value
-- from 
--     usr_input as input


drop table if exists `bms_cache_inputs_ctrls`,`bms_cache_inputs_pages`,`bms_cache_view_users_inputs`;
drop view if exists `bms_view_users_inputs`;

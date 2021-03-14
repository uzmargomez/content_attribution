library(bigrquery)
library(ChannelAttribution)
library(timeDate)
library(RGA)
library(stringr)
project <- "big-query-144615"
dataset <- "66253034"
bq_auth(path = "rax-datascience-dev-secret_key.json")
create_results<-TRUE
presults <- data.frame()
sql <- paste("
    WITH wtPathing AS (
SELECT
LEADS.CREATED_DATE
,SUM(0) AS BOOKINGS
,ARRAY_TO_STRING(LEADS.FOCUS_AREA,', ') AS FOCUS_AREA
,MAX(IF(LOWER(STATUS) IN ('converted', 'converted to opp'), 1, 0)) AS OPP_FLAG
,LEADS.RACKUID
,STRING_AGG(SESSIONS.SESSION_ID, ' > ' ORDER BY SESSIONS.DATE) AS SESSIONS
,STRING_AGG(
REGEXP_REPLACE(HITS.PAGE,r'((www|cart|blog|go)\\.rackspace\\.com)\\/(([a-z]{2}-[a-z]{2}(\\/|$))|([a-z]{2}(\\/|$))|(?:))((?:.*))','\\\\1/\\\\8' )
,' > ' ORDER BY HITS.DATE
) AS HITS
FROM `big-query-144615.RAX_ABSTRACTION_PROD.LEADS` AS LEADS
LEFT OUTER JOIN `big-query-144615.RAX_ABSTRACTION_PROD.WEB_SESSIONS` AS SESSIONS
ON SESSIONS.RACKUID = LEADS.RACKUID
LEFT OUTER JOIN `big-query-144615.RAX_ABSTRACTION_PROD.WEB_HITS` AS HITS
ON HITS.SESSION_ID = SESSIONS.SESSION_ID
WHERE 1 = 1
AND LEADS.RACKUID IS NOT NULL
AND LOWER(LEADS.RACKUID) NOT IN ('0','00','000','0000','00000','000000','0000000','00000000','000000000000', '000000000000000000','00000000000000000000', '---','1', '100','2','25', '3', '4', '5', '6','7','8','9','10','89','a','call in','chat','site submission','site submissions','site sub', 'na', 's','live person', 'sitesub' )
AND HITS.HOSTNAME IN ('www.rackspace.com', 'blog.rackspace.com', 'cart.rackspace.com', 'go.rackspace.com')
GROUP BY CREATED_DATE, FOCUS_AREA, RACKUID
ORDER BY CREATED_DATE ASC
)
SELECT
HITS AS PAGE_PATH
,SUM(BOOKINGS) AS OPP_AMOUNT
,SUM(OPP_FLAG) AS OPP_COUNT
,FOCUS_AREA
,CREATED_DATE
FROM wtPathing
WHERE 1 = 1
AND FORMAT_DATE('%Y-%m', CREATED_DATE) > '2020-01'
GROUP BY PAGE_PATH, FOCUS_AREA, CREATED_DATE
                 ", sep='')
cat(sql)
tb <- bq_project_query(project, sql)
path <- bq_table_download(tb, max_results = Inf)
M <- markov_model(path, 'PAGE_PATH', 'OPP_COUNT', var_value='OPP_AMOUNT', order = 1,max_step=NULL, out_more=FALSE, sep=">", seed=1)
write.csv(M, "CONTENT_OPP_XP_2020.csv")
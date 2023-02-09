    """

    :param documents: a list of the documents for which URLs and
    :return: dataframe with docids, URLs, titles
    """
    ctx = snowflake.connect(
        user='andy.chakraborty@fiscalnote.com',
        password='Arioch.12',
        account='he00278.us-east-1',
        database="FORGEAI_ARTICLES_V0660",
        schema="ARTICLES_V0660"
    )
    cs =ctx.cursor()
    print('connected')
    #params = [company, date]
    try:
        cs.execute("""
 select node_distance, starting_node, ending_node,array_agg(distinct concat(ievent,' : ', topics.name)) as event_and_topic_pairs, sum(intensity) as intensity
  , round(nvl(avg(codocs.sentiment),0),3) as endnode_sentiment, round(nvl(avg(codocs.financialsentiment),0),3) as endnode_financialsentiment
 , round(nvl(avg(codocs2.sentiment),0),3) as startnode_sentiment, round(nvl(avg(codocs2.financialsentiment),0),3) as startnode_financialsentiment
  from "SCRATCH_FORGEAI"."ANDYC"."KEVINBACON" KB
  left join "PROD_V06XX"."COMPANY_DATASET_V0650"."COMPANYSENTIMENTS" codocs on codocs.uripath = ending_node and codocs.confidence >=0.6 
  left join "PROD_V06XX"."COMPANY_DATASET_V0650"."COMPANYSENTIMENTS" codocs2 on codocs2.uripath = starting_node and codocs.docid = codocs2.docid and codocs2.confidence >=0.6
  left join "PROD_V06XX"."ARTICLES_V0670"."DOCUMENTTOPICS" topics on topics.docid = codocs.docid and topics.score >= .7
  where graph = 'goldman_sachs_group_inc'
  and KB.ievent is not null
  and KB.ievent not in ('Communication', '')
  group by 1 , 2,3 

""")
            #""", params)
        print('success')
        rows_big = cs.fetchall()
    except:
        print('failure')
    finally:
        cs.close()
    ctx.close()
    print('URLs Retrieved')
    mydf = pd.DataFrame(rows_big, columns=['NODE_DISTANCE','STARTING_NODE','ENDING_NODE','EVENT_AND_TOPIC_PAIRS','INTENSITY','ENDNODE_SENTIMENT',
                                           'ENDNODE_FINANCIALSENTIMENT','STARTNODE_SENTIMENT','STARTNODE_FINANCIALSENTIMENT'])
    
    return mydf

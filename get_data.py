from connector import connection
from time import strftime
# curseur de base de données et connexion
cursor, conn = connection()

def get_topics(filter=None):
    sql = ""
    if filter is None:
        sql = """
            SELECT topic_id, topic_message, topic_date, topic_by FROM
            topics
        """
    else:
        sql = """
            SELECT topic_id, topic_message, topic_date, topic_by FROM
            topics
            WHERE lower(topic_message) LIKE '%{filter}%'
        """.format(filter=filter)
    cursor.execute(sql)
    result = cursor.fetchall()
    # print(result)
    topic_data = list()
    for i in result:
        topic_data.append(
            dict(
                topic_id=str(i[0]),
                topic_message=i[1],
                topic_date=i[2].strftime("%d-%m-%Y %H:%M:%S"),
                topic_by=i[3]
            )
        )
        
    # print(topic_data)
    return topic_data

def get_topic_page_data(topic_id, filter=None):
    print('get_topic_page_data')
    sql = """
        SELECT topic_id, topic_message, topic_date, topic_by 
        FROM topics
        WHERE topic_id = {topic_id}
    """.format(topic_id=topic_id)
    cursor.execute(sql)
    i = cursor.fetchone()
    data = dict(
        topic_id=str(i[0]),
        topic_message=i[1],
        topic_date=i[2].strftime("%d-%m-%Y %H:%M:%S"),
        topic_by=i[3]
    )
    # obtenir les revendications du topic_id donné
    data['claims'] = list()
    sql = ""
    if filter is None:
        sql = """
            SELECT claim_id, claim_message, claim_date, claim_by 
            FROM claims
            WHERE topic_id = {topic_id}
            ORDER BY claim_date DESC
        """.format(topic_id=topic_id)
    else:
        sql = """
            SELECT claim_id, claim_message, claim_date, claim_by 
            FROM claims
            WHERE topic_id = {topic_id}
            AND lower(claim_message) LIKE '%{filter}%'
            ORDER BY claim_date DESC
        """.format(topic_id=topic_id, filter=filter)
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        data['claims'].append(dict(
            claim_id=str(i[0]),
            claim_message=i[1],
            claim_date=i[2].strftime("%d-%m-%Y %H:%M:%S"),
            claim_by=i[3]
        ))
    return data

def get_claim_page_data(claim_id, filter=None):
    print('get_claim_page_data')
    sql = """
        SELECT claim_id, claim_message, claim_date, claim_by, topic_id
        FROM claims
        WHERE claim_id = {claim_id}
    """.format(claim_id=claim_id)
    cursor.execute(sql)
    i = cursor.fetchone()
    data = dict(
        claim_id=str(i[0]),
        claim_message=i[1],
        claim_date=i[2].strftime("%d-%m-%Y %H:%M:%S"),
        claim_by=i[3]
    )
    # récupère le topic_message et le topic_by pour un claim_id donné
    sql = """
        SELECT topic_message, topic_by
        FROM topics
        WHERE topic_id = {topic_id}
    """.format(topic_id=i[4])
    cursor.execute(sql)
    res = cursor.fetchone()
    data['topic_message'] = res[0]
    data['topic_by'] = res[1]
    # obtenir les réponses du claim_id donné
    data['replies'] = list()
    sql = ''
    if filter is None:
        sql = """
            SELECT reply_id, reply_message, reply_date, reply_by 
            FROM replies
            WHERE claim_id = {claim_id}
            ORDER BY reply_date DESC
        """.format(claim_id=claim_id)
    else:
        sql = """
            SELECT reply_id, reply_message, reply_date, reply_by 
            FROM replies
            WHERE claim_id = {claim_id}
            AND lower(reply_message) LIKE '%{filter}%'
            ORDER BY reply_date DESC
        """.format(claim_id=claim_id, filter=filter)
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        data['replies'].append(dict(
            reply_id=str(i[0]),
            reply_message=i[1],
            reply_date=i[2].strftime("%d-%m-%Y %H:%M:%S"),
            reply_by=i[3]
        ))
    return data
    

if __name__ == "__main__":
    data = get_claim_page_data(2)
    print(data)


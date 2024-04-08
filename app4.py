from flask import Blueprint, request, jsonify
import os
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.exceptions import CouchbaseException
import couchbase.search as search
from couchbase.options import SearchOptions
from couchbase.vector_search import VectorQuery, VectorSearch
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document

blueprint4 = Blueprint('rag_with_color', __name__)

@blueprint4.route('/rag_with_color', methods=['POST'])
def rag_with_color():
    question_input = request.form['question_input']

    # Run your function here to find the color based on x, y, and z
    
    client = OpenAI()
    pa = PasswordAuthenticator(os.getenv("CB_USERNAME"), os.getenv("CB_PASSWORD"))
    cluster = Cluster("couchbases://" + os.getenv("CB_HOSTNAME") + "/?ssl=no_verify", ClusterOptions(pa))

    # Make sure to change the bucket, scope, and index names to match where you stored the sample data in your database. 
    bucket = cluster.bucket("vector-sample")
    scope = bucket.scope("color")
    search_index = "color-index"
    collection = scope.collection("rgb")


    prompt = hub.pull("rlm/rag-prompt")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)


    prompt = ChatPromptTemplate.from_template("""Answer the following question incorporating the following context:

    <context>
    {context}
    </context>

    Question: {input}""")

    document_chain = create_stuff_documents_chain(llm, prompt)

    try:
        vector = client.embeddings.create(input = [question_input], model="text-embedding-ada-002").data[0].embedding
        search_req = search.SearchRequest.create(search.MatchNoneQuery()).with_vector_search(
        VectorSearch.from_vector_query(VectorQuery('embedding_vector_dot', vector, num_candidates=3)))
        # Change the limit value to return more results. Change the fields array to return different fields from your Search index.
        result = scope.search(search_index, search_req, SearchOptions(limit=13,fields=["description"]))
        res = ''
        for row in result.rows():
            res = res + row.fields['description'] + "\n\n"
            
        invoked_result = document_chain.invoke({
            "input": question_input,
            "context": [Document(page_content=res)]
        })  

        return { 'invoked_result': invoked_result }
    
    except CouchbaseException as ex:
        import traceback
        traceback.print_exc()
        

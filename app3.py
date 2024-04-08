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
import couchbase.subdocument as SD

blueprint3 = Blueprint('add_custom_color', __name__)

@blueprint3.route('/add_custom_color', methods=['POST'])
def add_custom_color():
    x = float(request.form['x'])
    y = float(request.form['y'])
    z = float(request.form['z'])
    color_name = request.form['color_name']
    color_desc = request.form['color_desc']
    color_id = request.form['color_id']


    client = OpenAI()
    pa = PasswordAuthenticator(os.getenv("CB_USERNAME"), os.getenv("CB_PASSWORD"))
    cluster = Cluster("couchbases://" + os.getenv("CB_HOSTNAME") + "/?ssl=no_verify", ClusterOptions(pa))

    # Make sure to change the bucket, scope, and index names to match where you stored the sample data in your database. 
    bucket = cluster.bucket("vector-sample")
    scope = bucket.scope("color")
    collection = scope.collection("rgb")

    try:
        color_vec = client.embeddings.create(input = [color_desc], model="text-embedding-ada-002").data[0].embedding
        
        document = dict(
            brightness=99.99,
            color=color_name,
            colorvect_l2=[x, y, z],
            description=color_desc,
            embedding_model="text-embedding-ada-002-v2",
            embedding_vector_dot=color_vec,
            id=color_id,
            verbs=["protection", "shiled"],
            wheel_pos="other"
        )
        
        collection.upsert(
            color_id,
            document
        )
        
        return { "color": color_name, "color_id": color_id }
    except Exception as e:
        print("exception:", e)
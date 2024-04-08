from flask import Blueprint, request, jsonify
import os
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.exceptions import CouchbaseException
import couchbase.search as search
from couchbase.options import SearchOptions
from couchbase.vector_search import VectorQuery, VectorSearch

run_function_blueprint = Blueprint('run_function', __name__)

@run_function_blueprint.route('/run_function', methods=['POST'])
def run_function():
    print('running function..?')
    x = float(request.form['x'])
    y = float(request.form['y'])
    z = float(request.form['z'])


    # Run your function here to find the color based on x, y, and z
    res = search_color_index([x, y, z])
    return jsonify({'color': res})


def search_color_index(vector):
    # Make sure to change CB_USERNAME, CB_PASSWORD, and CB_HOSTNAME to the username, password, and hostname for your database.
    pa = PasswordAuthenticator(os.getenv("CB_USERNAME"), os.getenv("CB_PASSWORD"))
    cluster = Cluster("couchbases://" + os.getenv("CB_HOSTNAME") + "/?ssl=no_verify", ClusterOptions(pa))
    
    
    # Make sure to change the bucket, scope, and index names to match where you stored the sample data in your database.
    bucket = cluster.bucket("vector-sample")
    scope = bucket.scope("color")
    search_index = "color-index"
    
    try:
        search_req = search.SearchRequest.create(search.MatchNoneQuery()).with_vector_search(
            VectorSearch.from_vector_query(VectorQuery('colorvect_l2', vector, num_candidates=3)))
            # Change the limit value to return more results. Change the fields array to return different fields from your Search index.
        result = scope.search(search_index, search_req, SearchOptions(limit=13,fields=["color", "id"]))
        
        rows_as_strings = []
        for row in result.rows():
         rows_as_strings.append(row.fields['color'])
        
        final_string = ", ".join(rows_as_strings)

        return final_string
        
    except CouchbaseException as ex:
        import traceback
        traceback.print_exc()
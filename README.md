**Use Retrieval Augmentation Generation with Couchbase Vector DB**


Couchbase is a memory-first, performant NoSQL data platform providing services including kv, sql query, full-text & vector search, real-time analytics and mobile capabilities. You can build enterprise grade, scalable applications and innovate faster. 

This app is a simple build-up from the [Couchbase Documentation](https://docs.couchbase.com/cloud/vector-search/vector-search.html) on using Couchbase as vector storage for Similarity Search (with the example of RGB color) and Semantic Search (color  description), borrowing from the great [LangChain](https://www.langchain.com/) library. This example is built with Capella, Couchbase's cloud data platform however the same examples works with Servers (version 7.6 or above) too.   




**Set up**:  

1. On [Couchbase Capella](https://cloud.couchbase.com/sign-in), set up a cluster **versioned 7.6** with at least Data and Search services.
  ![image](https://github.com/sillyjason/rag_with_couchbase/assets/54433200/d87e84b7-d95b-4593-aef3-f045d76bb3ee)

2. Follow the instruction on this [Couchbase documentation](https://docs.couchbase.com/cloud/vector-search/create-vector-search-index-ui.html) to create the "vector-sample" bucket, "color" scope, "rgb" and "rgb_questions" collections. Download the color_data_2vectors.zip file and upload them into the created collections.

3. On the same documentation, create the Vector Search Index. Alternatively, you can download the JSON file under folder "files" and upload in the Advanced Mode of Search Index creation.
<img width="700" alt="image" src="https://github.com/sillyjason/rag_couchbase/assets/54433200/2de92920-0cda-4ebc-96a4-5d557c8ea39b">

4. On the same cluster, at Conenct tab, whitelist IP address so we can initiat SDK calls from applications
![image](https://github.com/sillyjason/rag_with_couchbase/assets/54433200/a125e231-df08-4910-8bad-78f9d8fafb62)
  
5. Stay at the Connect tab, create database access credentials. Take note of the account **username** (I) and **password** (II)
  
6. Take note of the **cluster connection string** (III). 
![image](https://github.com/sillyjason/rag_with_couchbase/assets/54433200/cdf03450-8926-4029-9818-ffd235367f1d)

7. You'll also need an OPENAI account and a valid **OPENAI API Key** (IV). 

8. Clone the repo to a local directory. On the same folder, set up the 4 environment variable mentioened above: CB_USERNAME (I); CB_PASSWORD (II); CB_HOSTNAME (III) but chop off the head "couchbases://". It should start with "cb.xxxx"; OPENAI_API_KEY (IV)





**Demo**: 

We can start off with running vector_search_rgb.py. Here we already defined a vector (a shade of blue, according to GPT), and will run it against the collection of "colors" already imported. We will be querying against the "colorvect_l2" field. 
![image](https://github.com/sillyjason/rag_with_couchbase/assets/54433200/a5278d56-6e2a-4869-9c94-1d3c107f9edc)


Let's be playful and take it further. Take a look at vector_insert_rgb.py. Here we're "creating" a custom color and give it a name and description which will be used in the semantic search later. Feel free to highlight something interesting about any color that carries unique undertones in your culture. Give it an ID (cus_colorid) that won't duplicate with existing documents. The rest of the fields in the dictionary won't matter as much. Run the vector_insert_rgb.py application and the color should be visible in the collection. Here we're using model "text-embedding-ada-002" for embedding. 
![image](https://github.com/sillyjason/rag_with_couchbase/assets/54433200/e14b72a0-a466-4fa6-a4e1-84d66d5fecd3)


Now let's make sure our newly added color can be returned through semantic search. Open the vector_search_rgb_desc.py file. Update the "question" string to be relevant to the description of the color you just defined. Run the file. You should see the result including your custom color and if not, tweak your question to be more relevant to the "description", or increase the "num_candidates" parameter so more colors are returned. This scenario is analogous to catalog search in any e-commerce platform. 


Contrary to the example above where we're more interested in finding the correct catalog item, another powerful scenario for vector store can be RAG (Retrieval Augmented Generation) where as specific contexts need be added to a LLM model to give more accurate, context-aware responses (and stop it from hallucination). Consider building a wikipedia of COLOR that can give color recommendations like a chatbot. This would require a vector store for any color-specific knowlege. 

So, open "rag_chain.py", and update the question in the "rag_chain.invoke" method. Make a question that spans contents mentioned in your custom color but also go beyond and ask something random. The LLM should be able to pull from its pretrained data as well as our added context to answer your question. 

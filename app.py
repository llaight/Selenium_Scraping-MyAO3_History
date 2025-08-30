from flask import Flask, request, jsonify
import joblib
from test_api import predict_work_popularity, fetch_work_details
from dotenv import load_dotenv
import os
from flask_cors import CORS
from supabase import create_client

app = Flask(__name__)
CORS(app)

load_dotenv()
model=joblib.load("model/Gradient Boosting.pkl")

def get_supabase_client():
    url= os.getenv("SUPABASE_URL")
    key= os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("Supabase URL or Key not found in environment variables")
    return create_client(url, key)


@app.route('/predict', methods=['POST'])
def predict():
    data= request.get_json()
    url= data.get("url")

    if not url:
        return jsonify({"error": "url is required!"}), 400 
    
    result= predict_work_popularity(model, url)
    if result is None:
        return jsonify({"error": "Failed to fetch work details or make prediction."}), 500

    #connect to the database
    supabase= get_supabase_client()
    if supabase is None:
        return jsonify({"error": "Failed to connect to Supabase."}), 500

    response= supabase.table("popularity_classifier").insert({"title": result['title'],
                                                     "chapters": result['chapters'],
                                                     "words": result['words'],
                                                      "kudos": result['kudos'],
                                                     "bookmarks": result['bookmarks'],
                                                     "hits": result['hits'],
                                                     "comments": result["comments"],
                                                     "popularity": result["popularity"]
                                                    }).execute()
    
    if response.data:
        return jsonify({
                    "status": "success",
                    "message": "data inserted successfully into the supabase",
                    "inserted_record":{
                        "Title": result['title'],
                        "Chapters": result['chapters'],
                        "Words": result['words'],
                        "Kudos": result['kudos'],
                        "Bookmarks": result['bookmarks'],
                        "Hits": result['hits'],
                        "Comments": result['comments'],
                        "Popularity": result['popularity']
                    }
                }), 201
    else:
        return jsonify({"status": "error",
                        "message": f"failed to insert the data: {response}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)






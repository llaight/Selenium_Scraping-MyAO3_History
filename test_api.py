import AO3
import joblib
import pandas as pd


# Then fetch the work
def fetch_work_details(url):
    workid = AO3.utils.workid_from_url(url)

    work = AO3.Work(workid, load_chapters=False)
    title = work.title
    chapters = work.nchapters
    comments = work.comments
    hits = work.hits
    kudos = work.kudos
    bookmarks = work.bookmarks
    words = work.words

    return {
        'Title': title,
        'Chapters': chapters,
        'Words': words,
        'Kudos': kudos,
        'Bookmarks': bookmarks,
        'Hits': hits,
        'Comments': comments
    }

model = joblib.load("model/Gradient Boosting.pkl")
scaler = joblib.load("model/scaler.pkl")

def predict_work_popularity(model, url):
    features = fetch_work_details(url)
    X = pd.DataFrame([{
        'Chapters': features['Chapters'],
        'Words': features['Words'],
        'Kudos': features['Kudos'],
        'Bookmarks': features['Bookmarks'],
        'Hits': features['Hits'],
        'Comments': features['Comments']
    }])

    X = scaler.transform(X)
    prediction = model.predict(X)[0]
    label = "Popular" if prediction == 1 else "Less Popular"

    return {
        "title": features['Title'],
        "chapters": features['Chapters'],
        "words": features['Words'],
        "kudos": features['Kudos'],
        "bookmarks": features['Bookmarks'],
        "hits": features['Hits'],
        "comments": features['Comments'],
        "popularity": label
    }

# url = "https://archiveofourown.org/works/59571673"
# result = predict_work_popularity(model, url)
# print(f"Title: {result['title']}")
# print(f"Prediction: {result['popularity']}")

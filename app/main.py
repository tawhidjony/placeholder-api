from fastapi import FastAPI

# ডাটাবেস টেবিল তৈরি করুন (প্রথম রানে)
# item.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


# উদাহরণ রাউট
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with PostgreSQL"}

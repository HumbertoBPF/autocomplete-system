from app_factory import create_app
from database.config import connect_mongodb

app = create_app()
connect_mongodb()
app.run(debug=True)

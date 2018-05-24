from app.core import create_app
from app.database import get_db

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        get_db().initialize()

import os

from app import create_app
from app.seed import seed_db

app = create_app()

if __name__ == '__main__':
    if os.environ.get('SEED_DB') == 'true':
        seed_db(app)
    app.run(host='0.0.0.0', port=5000)

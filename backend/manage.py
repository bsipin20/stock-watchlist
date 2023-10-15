from casestudy.app import create_app
import os
from dotenv import load_dotenv

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

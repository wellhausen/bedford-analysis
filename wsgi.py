from app.app import app
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use 5000 as the default port
    app.run(host='0.0.0.0', port=port)

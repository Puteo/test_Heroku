import logging
import sys
import os
from threading import Thread

from app.controllers.app import app

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))



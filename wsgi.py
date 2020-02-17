from tests_backend.app import create_app
from tests_backend.settings import ProdConfig

app = create_app(ProdConfig)

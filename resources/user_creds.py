import os
from dotenv import load_dotenv

load_dotenv()

class SuperAdminCreds:
    USERNAME = os.getenv('SUPER_ADMIN_USERNAME')
    PASSWORD = os.getenv('SUPER_ADMIN_PASSWORD')

    if not USERNAME or not PASSWORD:
        raise RuntimeError("SUPER_ADMIN credentials are not set")


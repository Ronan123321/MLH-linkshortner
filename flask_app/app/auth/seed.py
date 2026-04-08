import hashlib
from app.models.susers import Susers

def get_hash(username, password):
    import hashlib
    hash_pass = hashlib.sha256(password.encode()).hexdigest()

    return hash_pass.strip()



def seed_admin():
    username = "admin"
    password = "yeoldpass"
    password = get_hash(username, password)
    if Susers.get_or_none(Susers.username == username) is None:
        Susers.create(username=username, password=password)



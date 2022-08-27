
def test_main():
    from models.crud import UserCRUD
    salt = UserCRUD.Security.random_salt()
    password = 'admin'
    hash = UserCRUD.Security.hash_password(password, salt)
    salt2, _ = hash.split('$')
    assert salt2 == salt
    assert UserCRUD.Security.check_password(hash, password)

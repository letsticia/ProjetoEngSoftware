import bcrypt

def hash_password(password: str) -> str:
    """
    Gera hash bcrypt da senha
    
    Args:
        password: Senha em texto plano
        
    Returns:
        Hash da senha como string
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha corresponde ao hash
    
    Args:
        plain_password: Senha em texto plano
        hashed_password: Hash armazenado no banco
        
    Returns:
        True se a senha estiver correta, False caso contrário
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )
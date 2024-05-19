import re
def list_all_available_openai_models(openai_client):
    models = openai_client.models.list().data
    return [m.id for m in models]

def sanitize_collection_name(name: str) -> str:
    """
    Sanitizes a given collection name to make it safe for use in a PostgreSQL database.
    
    Parameters:
    - name (str): The user-provided collection name.
    
    Returns:
    - str: A sanitized collection name that is safe for use in the database.
    """
    # Define a regex pattern for valid collection names: start with a letter, followed by letters, digits, or underscores.
    valid_pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

    # Remove any invalid characters by replacing them with underscores
    sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '_', name)

    # Ensure the sanitized name matches the valid pattern, if not, raise an error or handle accordingly
    if not valid_pattern.match(sanitized_name):
        raise ValueError(f"Invalid collection name: {name}")

    # Optionally, check if the name is a reserved SQL keyword
    reserved_keywords = {
        'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'WHERE', 'JOIN', 'CREATE', 'DROP', 'ALTER', 'TABLE', 'DATABASE', 'INDEX',
        'VIEW', 'TRIGGER', 'FUNCTION', 'PROCEDURE', 'GRANT', 'REVOKE', 'COMMIT', 'ROLLBACK', 'SAVEPOINT', 'LOCK', 'UNLOCK'
        # Add more keywords as necessary
    }
    
    if sanitized_name.upper() in reserved_keywords:
        raise ValueError(f"Collection name cannot be a reserved SQL keyword: {sanitized_name}")

    return sanitized_name


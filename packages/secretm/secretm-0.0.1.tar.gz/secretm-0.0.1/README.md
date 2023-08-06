# secrets
A tiny secret manager in python. Adds the secrets file to the `.gitignore`.


## Example
```python
import secrets

# The class takes an optional path for the secrets file
s = secrets.Secrets()

# Write the api key to the secrets file
s['api_key'] = 'abc'

# Print the secret
print(s['api_key'])
```

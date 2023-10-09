# PFC_2023

# Gerenciador de dados de levantamento

## Instruções de Configuração

### Configuração do Backend em Python (Django)

Para configurar o backend em Python (Django), siga estas etapas:

#### Instalação de dependências

```python
npm install
```

#### Configuração do CORS

No arquivo `settings.py` do seu projeto Django, certifique-se de que as configurações do CORS estejam definidas corretamente:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Substitua pela URL do seu frontend React
    # Adicione outras origens permitidas conforme necessário
]

CSRF_TRUSTED_ORIGINS = ['http://localhost:3000'] # Substitua pela URL do seu frontend React
CORS_ALLOW_CREDENTIALS = True
...
EMAIL_HOST = 'smtp.gmail.com' # Substitua pelo provedor de email de administrador
EMAIL_HOST_USER = 'seu_email@gmail.com' # Substitua pelo email de administrador
EMAIL_HOST_PASSWORD = 'sua_senha' # Substitua pela senha de app do email do administrador
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

```

#### Rodar servidor local

No diretório django-react-pfc/pfc_2023/pfc_2023/

```python
python manage.py runserver
```

### Configuração do Frontend em JavaScript (React)

Para configurar o frontend em Javascript (React), siga estas etapas:

O arquivo `Config.js` no seu projeto React é responsável por definir a URL do backend para se conectar ao seu servidor Django. Para configurar o `backendUrl`, siga estas etapas:

1. Abra o diretório do seu projeto React em um editor de código.

2. Navegue até a pasta `src` e, em seguida, encontre o arquivo `Config.js`. Este arquivo contém a definição do `backendUrl`.

3. Abra o arquivo `Config.js` no seu editor de código.

4. Localize a linha que se parece com isto:

   ```javascript
   const backendUrl = "http://localhost:8000"; // Substitua pela URL do seu backend
   ```

#### Instalação de dependências

No diretório django-react-pfc/pfc_2023/react_frontend/

```javascript
npm install
```

#### Rodar servidor local

No diretório django-react-pfc/pfc_2023/react_frontend/

```javascript
npm install
```

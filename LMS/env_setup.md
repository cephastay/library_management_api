<!-- You need to have an environment variable file with these
to successfully use the API -->

# Setting Up Your .env File

To successfully use this API, you need to create a .env file in your local
environment. This file securely stores configuration settings and sensitive
information like secret keys and database URLs. Follow the steps below to
set it up correctly. 

### Why the .env File is Important
The `.env` file:

- Keeps sensitive information out of your source code.
- Simplifies environment-specific configurations (e.g., development vs. production).
- Enhances security and flexibility.

## Step 1: Install Required Dependencies
Before setting up your .env file, ensure all project dependencies are installed.
Use the requirements.txt file to install them:
```
 pip install -r requirements.txt
```

## Step 2: Create Your `.env` File

- Create a file name `.env` in the root directory of your project
- Use the template below as a guide to provide the required variables

### Required Environment Variables

### _Secret_Key_  
This is a unique, random key used for cryptographic signing in Django.
Use an online tool like [djecrety](https://djecrety.ir/) or follow the 
[Django documentation](https://docs.djangoproject.com/en/5.1/ref/settings/#std-setting-SECRET_KEY) on how to generate it.

### _Debug_ 
This Controls whether detailed error messages are shown, set it to True
during development for debugging or false in production for security.
Learn more about this in [Django Debug Guide](https://docs.djangoproject.com/en/5.1/ref/settings/#std-setting-DEBUG)

### _Allowed Hosts_
This setting ensures that only requests from specific domains or IP addresses are
allowed to interact with the application. It helps prevent security vulnerabilities 
like HTTP Host header attacks. This project relies on `python-decouple` 
which your environment variables from the .env file, making it easier to keep
sensitive settings out of version control. For more details on setting up consult
the [python-decouple documentation](https://pypi.org/project/python-decouple/)

### _Database_Production and Database_Development_ : 
These are the url format paths to specify your database URLs for
production and development environments. Use mySQL or PostGress for production and
SQLite for development. They are defined using the format of python package
`dj-database-url`, read more at [dj-database-url documentation](https://pypi.org/project/dj-database-url/)

### Environment 
This variable determines the environment in which the application is running.
It can either be ``development`` or ``production``. The default environment will 
determine how certain configurations (like ``DEBUG`` and ``ALLOWED_HOSTS``) are set 
in your Django settings file. This ensures that development settings are used 
during local development, and production settings are applied in a production environment. 
Set this value to either development or production

### _File Template `.env`_

```
# Secret Key
SECRET_KEY=randomsecret

# Set the environment to 'development' or 'production'
ENVIRONMENT=development  # Change to 'production' when deploying to production

# Allowed Hosts for different environments
ALLOWED_HOSTS_DEVELOPMENT=127.0.0.1,.localhost,172.17.176.1
ALLOWED_HOSTS_PRODUCTION=your-production-domain.com

# Database URLs for different environments
DATABASE_DEVELOPMENT=sqlite:////home/yourusername/desktop/final_work/LMS/db_development.sqlite3
DATABASE_PRODUCTION=mysql://yourusername:your_password@your_host/your_database_name

# Debug Flags for different environments
DEBUG_DEVELOPMENT=True
DEBUG_PRODUCTION=False
```

## Step 4: Verify Your SetUp
- Double check that all your variables are correctly setup
- Run the application locally to confirm that everything works

## Final Thoughts

Keep your .env file private and never upload it to version control systems
like GitHub. Use a .gitignore file to exclude it. If you encounter issues, 
refer to the provided links or raise a query in the project’s issue tracker.
By following these instructions, you ensure a secure and efficient 
setup for your API.
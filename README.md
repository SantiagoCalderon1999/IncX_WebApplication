# Incx Web Application

This Django-based web application demonstrates the capabilities of IncX (**Inc**remental E**x**planations), a method for generating saliency maps and explanations incrementally and in real-time.

## Tech Stack

- **Django**: Web framework for building the application.
- **Docker**: Containerization platform for deployment.
- **Python 3.11**: Programming language used for development.
- **IncX**: IncX is a method for generating saliency maps and explanations. For more detailed information and to explore the project further, visit the [IncX GitHub repository](https://github.com/SantiagoCalderon1999/IncX).
- **OpenCV**: Library used for computer vision tasks.

## Getting Started

To set up and use this project, you will need `pyenv` for managing Python versions and `poetry` for handling dependencies. Follow these instructions to configure your environment.

### Prerequisites

1. **Install Pyenv**  
   Pyenv allows you to manage multiple Python versions on your system. Select your operating system and follow the relevant installation instructions:

   - **Linux and macOS:** Refer to the guide on the [pyenv GitHub repository](https://github.com/pyenv/pyenv#installation).
   - **Windows:** Use [pyenv-win](https://github.com/pyenv-win/pyenv-win#installation) for installation instructions.

2. **Install the Required Python Version**  
   After installing pyenv, use it to install the Python version specified in the `.python-version` file located in the root directory of this project. Execute the following command:

   ```shell
   pyenv install
   ```

3. **Install Poetry**  
   Install poetry by following the instructions on the [poetry installation page](https://python-poetry.org/docs/#installation).

4. **Configure Poetry**  
   Set up poetry to create virtual environments within the project directory. This configuration helps manage isolated environments for different projects:

   ```shell
   poetry config virtualenvs.in-project true
   ```

5. **Install Project Dependencies**  
   Use poetry to install all required dependencies and create a virtual environment:

   ```shell
   poetry install
   ```

## Executing the application locally

To run the application on your local machine, use the following command:

```shell
poetry run py manage.py runserver
```

The application will be accessible at http://localhost:8000/. Open this URL in your web browser to view the application.

You should see a screen similar to this:

![Web Application](https://github.com/SantiagoCalderon1999/IncX_WebApplication/blob/main/blob/web_app_2.PNG?raw=true)

The application is deployed to an Azure Web Application using GitHub Actions.
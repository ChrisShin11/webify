# FROM python:3.11.9-bookworm
FROM python:3.11.9-slim-bookworm

ARG APP_HOME
ARG PYTHON_ENV

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME ${APP_HOME}
ENV PYTHON_ENV ${PYTHON_ENV}
ENV PYTHONPATH ${APP_HOME}

WORKDIR ${APP_HOME}

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./app ${APP_HOME}
RUN mkdir -p ${APP_HOME}/uploads

# Debug: List contents of the working directory and app directory
RUN echo "Contents of ${APP_HOME}:" && ls -R ${APP_HOME}

# Debug: Print Python path and installed packages
RUN echo "Python path:" && python -c "import sys; print('\n'.join(sys.path))" && \
    echo "Installed packages:" && pip list

# Use a shell script to run debug commands and start the application
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]

# # run the app
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--reload"]
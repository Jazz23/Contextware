FROM python:latest

# Install Node.js
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install gemini-cli
RUN npm install -g @google/gemini-cli@preview

# Precache some repositories
RUN git clone https://github.com/astropy/astropy astropy
RUN git clone https://github.com/django/django django
RUN git clone https://github.com/matplotlib/matplotlib matplotlib
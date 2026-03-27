FROM node:20-slim

# Install Python 3 (only stdlib needed — no pip packages)
RUN apt-get update && apt-get install -y python3 --no-install-recommends \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy everything
COPY . .

# Install Node deps and build Next.js
WORKDIR /app/site
RUN npm ci
RUN npm run build

EXPOSE 3000

# next start must run from the site dir; PROJECT_ROOT resolves to /app
CMD ["npm", "run", "start"]

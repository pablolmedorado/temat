FROM node:lts-alpine as build
RUN apk update && apk add --no-cache make gcc g++ python
WORKDIR /usr/src/app/frontend
COPY ./frontend/package*.json ./
RUN npm ci
COPY ./frontend ./
RUN npm run build

FROM python:3.7-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update \
    && apk add --no-cache postgresql-dev gcc musl-dev \
    && pip install --no-cache-dir --trusted-host pypi.python.org pipenv==2018.11.26 psycopg2
WORKDIR /usr/src/app/backend
COPY ./backend/Pipfile* ./
RUN pipenv install --system --deploy
COPY ./backend ./
COPY --from=build /usr/src/app/frontend/dist /usr/src/app/frontend/dist
COPY --from=build /usr/src/app/frontend/config/webpack-stats-production.json /usr/src/app/frontend/config/
RUN python manage.py collectstatic --no-input --link
EXPOSE 8000
CMD [ "pipenv", "run", "serve" ]

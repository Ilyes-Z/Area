FROM node:14.1-alpine as builder

ARG AREA_HOST
ARG APK_PATH

ENV REACT_APP_AREA_HOST=$AREA_HOST
ENV REACT_APP_APK_PATH=$APK_PATH

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY package.json .

RUN npm install

COPY . .

RUN npm run build


FROM nginx:1.19.7-alpine

COPY --from=builder /usr/src/app/build /usr/share/nginx/html

COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
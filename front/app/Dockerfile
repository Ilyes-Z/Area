FROM cirrusci/flutter:1.22.5

WORKDIR /usr/src/app

COPY . .

RUN flutter clean && flutter pub get \
    && flutter build apk --release

RUN mkdir -p /usr/apk

RUN cp /usr/src/app/build/app/outputs/flutter-apk/app-release.apk /usr/apk/area.apk
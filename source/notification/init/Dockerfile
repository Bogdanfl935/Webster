FROM openjdk:11-jre-slim

ARG SOURCE_JAR=target/*.jar

COPY preEntrypoint.sh /msnotification/
COPY ${SOURCE_JAR} /msnotification/msNotificationApp.jar
COPY ./src/main/resources/static /msnotification/src/main/resources/static
COPY ./src/main/resources/templates /msnotification/src/main/resources/templates

WORKDIR /msnotification/

ENTRYPOINT ["./preEntrypoint.sh", "java", "-jar", "./msNotificationApp.jar"]
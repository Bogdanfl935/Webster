FROM openjdk:11-jre-slim

ARG SOURCE_JAR=target/*.jar

COPY preEntrypoint.sh /msauth/
COPY ${SOURCE_JAR} /msauth/msAuthApp.jar

WORKDIR /msauth/

ENTRYPOINT ["./preEntrypoint.sh", "java", "-jar", "./msAuthApp.jar"]
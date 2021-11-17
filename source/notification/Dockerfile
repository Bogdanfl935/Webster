FROM openjdk:11-jre-slim

ARG CORE_DIR_PATH=core
ARG INIT_DIR_PATH=init
ARG SOURCE_JAR=${CORE_DIR_PATH}/target/*.jar
ARG DOCKER_DIR_PATH=/msnotification

COPY ${INIT_DIR_PATH}/preEntrypoint.sh ${DOCKER_DIR_PATH}/
COPY ${SOURCE_JAR} ${DOCKER_DIR_PATH}/msNotificationApp.jar
COPY ${CORE_DIR_PATH}/src/main/resources/static ${DOCKER_DIR_PATH}/src/main/resources/static
COPY ${CORE_DIR_PATH}/src/main/resources/templates ${DOCKER_DIR_PATH}/src/main/resources/templates

WORKDIR ${DOCKER_DIR_PATH}/

ENTRYPOINT ["./preEntrypoint.sh", "java", "-jar", "./msNotificationApp.jar"]
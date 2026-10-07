FROM maven:3.9.11-eclipse-temurin-17 AS compilacion
WORKDIR /proyecto
COPY pom.xml ./
COPY src ./src
RUN mvn -B -ntp -DskipTests package dependency:copy-dependencies -DincludeScope=runtime

FROM eclipse-temurin:17-jre-jammy
WORKDIR /app
RUN useradd --system --uid 10001 --create-home personas
COPY --from=compilacion /proyecto/target/SistemaPersonas-1.0-SNAPSHOT.jar ./app.jar
COPY --from=compilacion /proyecto/target/dependency ./lib
USER personas
ENTRYPOINT ["java", "-Dfile.encoding=UTF-8", "-cp", "app.jar:lib/*", "mx.edu.tesoem.sistemapersonas.prueba.PruebaPersona"]

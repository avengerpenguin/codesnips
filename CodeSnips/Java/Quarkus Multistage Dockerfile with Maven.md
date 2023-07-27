```yaml
---
tags: quarkus, java, maven, docker, dockerfile
---

```
```dockerfile
FROM quay.io/quarkus/centos-quarkus-maven:19.2.1 AS build  
COPY ./pom.xml ./pom.xml  
COPY ./src ./src  
RUN mvn -Pnative package -DskipTests  
  
FROM registry.access.redhat.com/ubi8/ubi-minimal  
WORKDIR /work/  
COPY --from=build /project/target/*-runner /work/application  
RUN chmod 775 /work  
EXPOSE 8080  
CMD ["./application", "-Dquarkus.http.host=0.0.0.0"]
```

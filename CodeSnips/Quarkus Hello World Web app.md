## Prerequisites

Create project skeleton using Maven:

```bash
quarkus create app org.example:quarkus-hello-world \
    --extension='resteasy-reactive'
```

See [Creating Your First Application - Quarkus](https://quarkus.io/guides/getting-started) for more info.

## Code

```java
package org.example;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

@Path("/hello")
public class HelloResource {

    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String hello() {
        return "Hello, Quarkus!";
    }
}
```

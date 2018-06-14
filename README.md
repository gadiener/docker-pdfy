# PDF Generator Service
> Dockerized PDF Generator with compression and pages merge features.

## How to use

### Docker run

```bash
$ docker run -p 80:8080 -v ./pdf:/storage --name pdfy -d caffeina/pdfy:1
```

### Docker compose

Example docker-compose.yml for pdfy generation and sync on AWS S3:

```yaml
version: '3'

services:
    pdfy:
        image: caffeina/pdfy:1
        restart: always
        volumes:
            - pdf-data:/storage

    awssync:
        image: caffeina/awssync:1
        restart: always
        volumes:
            - pdf-data:/storage
        environment:
            AWS_BUCKET_SYNC_DIR: "pdf"
            AWS_BUCKET: "mybucket"
            AWS_ACCESS_KEY_ID: "myawskey"
            AWS_SECRET_ACCESS_KEY: "************************"

volumes:
    pdf-data:
```

Then start the containers.

```bash
$ docker-compose up
```

**WARNING: By design pdfy isn't meant to be exposed on the internet.**


## API

### Get pdf list

```bash
$ curl http://localhost/
```

### Generate new pdf

```bash
$ curl -X POST -d "urls=https://google.it&urls=https://google.com&name=google&orientation=portrait&paper=10cmX15.5cm" http://localhost/
```

#### Parameters

- **urls:** Urls to trasform in pdf pages *(required)*
- **name:** Name of pdf without extension *(required)*
- **orientation:** Can be portrait or landscape *(optional, default=`portrait`)*
- **paper:** Can be one of the following A3, A4, A5, Legal, Letter, Tabloid or page size in mm, cm, in or px. For Example 10cmX15.5cm *(optional, default=`A4`)*

### Delete all pdfs

```bash
$ curl -X DELETE http://localhost/
```

### Delete a pdf

```bash
$ curl -X DELETE http://localhost/{pdf-name}
```

### Get pdf

```bash
$ curl http://localhost/{pdf-name}
```

## Todo

- Improve documentation;
- Upgrade to python 3;
- Use Chrome Headless instead of PhantomJS;
- Add request throttling and authentication;
- Add async mode and request queue.


## Contributing

How to get involved:

1. [Star](https://github.com/gadiener/docker-pdfy/stargazers) the project!
2. Answer questions that come through [GitHub issues](https://github.com/gadiener/docker-pdfy/issues?state=open)
3. [Report a bug](https://github.com/gadiener/docker-pdfy/issues/new) that you find

This project follows the [GitFlow branching model](http://nvie.com/posts/a-successful-git-branching-model). The ```master``` branch always reflects a production-ready state while the latest development is taking place in the ```develop``` branch.

Each time you want to work on a fix or a new feature, create a new branch based on the ```develop``` branch: ```git checkout -b BRANCH_NAME develop```. Only pull requests to the ```develop``` branch will be merged.

Pull requests are **highly appreciated**.

Solve a problem. Features are great, but even better is cleaning-up and fixing issues in the code that you discover.


## Versioning

This project is maintained by using the [Semantic Versioning Specification (SemVer)](http://semver.org).


## Copyright and license

Copyright 2018 [Caffeina](http://caffeina.com) srl under the [MIT license](LICENSE.md).
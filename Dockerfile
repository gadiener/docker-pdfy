FROM python:2-alpine

RUN apk update && \
	apk --no-cache add tini gcc musl-dev

RUN addgroup -g 82 -S www-data \
	&& adduser -u 82 -D -S -G www-data www-data

# CPDF
COPY ./cpdf.tar.gz /app/cpdf.tar.gz
RUN tar xzvf /app/cpdf.tar.gz -C /usr/bin/

# PhantomJS
COPY ./phantomjs.tar.gz /app/phantomjs.tar.gz
RUN tar xzvf /app/phantomjs.tar.gz -C /tmp/ && \
	cp -R /tmp/etc/fonts /etc/ && \
	cp -R /tmp/lib/* /lib/ && \
	cp -R /tmp/lib64 / && \
	cp -R /tmp/usr/lib/* /usr/lib/ && \
	cp -R /tmp/usr/lib/x86_64-linux-gnu /usr/ && \
	cp -R /tmp/usr/share/* /usr/share/ && \
	cp /tmp/usr/local/bin/phantomjs /usr/bin/

RUN rm -rf /app/cpdf.tar.gz /app/phantomjs.tar.gz /tmp/*

RUN mkdir -p /storage

COPY ./requirements.txt /app/requirements.txt
COPY ./setup.py /app/setup.py
COPY ./src /app/src

RUN chown -R www-data:www-data /usr/local/ /app /storage

USER www-data

RUN cd /app && \
   pip install -r requirements.txt && \
   pip install .

EXPOSE 8080
WORKDIR /app
VOLUME /storage

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["pdfy"]

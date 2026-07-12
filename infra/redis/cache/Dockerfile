FROM redis:7-alpine

COPY redis.conf /usr/local/etc/redis/redis.conf

RUN mkdir -p /data && chown redis:redis /data

CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
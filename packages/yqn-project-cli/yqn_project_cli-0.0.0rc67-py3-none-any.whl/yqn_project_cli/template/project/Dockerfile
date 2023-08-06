FROM harbor.sa.iyunquna.com/yqn-library/yqn-data-price_forecast_env:20210304
ENV LANG C.UTF-8

ARG APP_PORT
ARG PACKAGE_PATH
ARG ENV
ARG IMAGE_TAG
ENV APP_PORT $APP_PORT
ENV PACKAGE_PATH $PACKAGE_PATH
ENV IMAGE_TAG $IMAGE_TAG
ENV ENV $ENV

WORKDIR /opt/web/ws-$APP_PORT

COPY requirements.txt \
    model_url_config_local.yml \
    model_url_config_online.yml \
    ./
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

#RUN if [ "$ENV" = "sta" ] ; then yqn-model -e online -F; else yqn-model -e local -F; fi


ARG GIT_COMMIT
ENV CODE_VERSION=$GIT_COMMIT
COPY . ./
RUN chmod +x entrypoint.sh
ENTRYPOINT  ["./entrypoint.sh"]

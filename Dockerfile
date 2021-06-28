FROM python:3.9 AS base

WORKDIR /usr/python
ENV ORACLE_HOME=/opt/oracle
ENV PATH=${ORACLE_HOME}/instantclient_19_11/:$PATH
ENV LD_LIBRARY_PATH=${ORACLE_HOME}/instantclient_19_11/:$LD_LIBRARY_PATH

COPY . ./

RUN python -m pip install pipenv && pipenv install --system

RUN ./install-instantclient.sh

FROM base AS etl

ENTRYPOINT ["python"]
CMD ["push_single_owner_to_api.py"]
FROM python:3.8

LABEL org.opencontainers.image.authors="Jon Zeolla"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.vendor="Seiso"
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.title="hai"
LABEL org.opencontainers.image.description="hai"
LABEL org.opencontainers.image.url="https://seisollc.com"
LABEL org.opencontainers.image.source="https://github.com/SeisoLLC/hai"
LABEL org.opencontainers.image.revision="${COMMIT_HASH}"

RUN apt-get -y update \
 && apt-get -y install xmlsec1 \
                       libxmlsec1-openssl \
 && git clone https://github.com/IdentityPython/pysaml2.git /opt/pysaml2 \
 && pip3 install --no-cache-dir pipenv

WORKDIR /hai

ENV PIP_NO_CACHE_DIR=1
COPY Pipfile Pipfile.lock /opt/pysaml2/example/
COPY idp.xml /opt/pysaml2/example/idp2/idp.xml
COPY entrypoint.sh /opt/hai/entrypoint.sh

ENTRYPOINT ["/opt/hai/entrypoint.sh"]

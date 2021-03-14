FROM r-base

RUN apt-get update -y
RUN apt-get install -y build-essential libcurl4-gnutls-dev libxml2-dev libssl-dev

COPY . /app
WORKDIR /app

RUN Rscript install_packages.R
RUN Rscript myscript.R

CMD ["head", "-n", "10", "CONTENT_OPP_XP_2020.csv"]
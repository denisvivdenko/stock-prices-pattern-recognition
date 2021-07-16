FROM python:3.9

WORKDIR /img-generation-script

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD ./data ./data
ADD ./scripts ./scripts
ADD ./library ./library

ENTRYPOINT [ "python", "-m", "scripts.image_generation_script"]


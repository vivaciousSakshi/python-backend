FROM tiangolo/uwsgi-nginx-flask:python3.8
WORKDIR /project
ADD . /project
RUN pip install -r requirements.txt
CMD ["python","app.py"]

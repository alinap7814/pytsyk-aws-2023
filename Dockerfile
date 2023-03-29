
FROM public.ecr.aws/lambda/python:3.9


COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY remediator remediator

COPY remediations remediations

CMD [ "remediator.__main__.handler" ]
from config.celery import app


@app.task(name="execute_newsletter_mailing")
def execute_newsletter_mailing(payload):
    pass

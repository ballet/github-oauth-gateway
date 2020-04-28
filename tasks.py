from invoke import task

@task
def test(c):
    c.run('python -m pytest')


@task
def lint(c):
    c.run('flake8 ballet_oauth_gateway tests')


@task
def serve(c):
    c.run('gunicorn wsgi:app')

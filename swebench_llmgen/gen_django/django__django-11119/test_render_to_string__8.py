import pytest
from django.template import Context
from django.template.engine import Engine
from django.contrib.auth.models import User
from django.template import TemplateDoesNotExist

@pytest.fixture
def engine():
    return Engine()

@pytest.fixture
def user_template():
    return """
    Hello, {{ user.username }}!
    """

@pytest.fixture
def user_context(user_template):
    template = engine().from_string(user_template)
    return Context({"user": User(username="TestUser")}), template

def test_render_to_string_with_single_template(engine, user_context):
    context, template = user_context
    rendered = engine.render_to_string(user_template, context)
    assert "Hello, TestUser!" in rendered

def test_render_to_string_with_list_template(engine, user_context):
    context, template = user_context
    rendered = engine.render_to_string([user_template], context)
    assert "Hello, TestUser!" in rendered

def test_render_to_string_with_empty_context(engine):
    rendered = engine.render_to_string('non_existent_template.html', {})
    assert rendered == ''

def test_render_to_string_with_context_instance(engine, user_context):
    context, template = user_context
    rendered = engine.render_to_string(user_template, context)
    assert "Hello, TestUser!" in rendered

def test_render_to_string_raises_exception_for_non_existent_template(engine):
    with pytest.raises(TemplateDoesNotExist):
        engine.render_to_string('non_existent_template.html')
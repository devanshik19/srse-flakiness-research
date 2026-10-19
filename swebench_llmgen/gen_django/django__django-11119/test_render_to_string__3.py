import pytest
from django.contrib.auth.models import User
from django.template import Engine, Context
from django.template.exceptions import TemplateDoesNotExist


@pytest.fixture
def template_engine():
    return Engine(dirs=['/path/to/templates'])


def test_render_to_string_with_single_template(template_engine):
    # Assuming there's a template called 'test_template.html'
    user = User.objects.create(username='testuser')
    context = {'user': user}
    rendered = template_engine.render_to_string('test_template.html', context)
    assert 'Expected Content' in rendered  # Replace with the expected content


def test_render_to_string_with_template_list(template_engine):
    user = User.objects.create(username='testuser')
    context = {'user': user}
    rendered = template_engine.render_to_string(['test_template_1.html', 'test_template_2.html'], context)
    assert 'Expected Content' in rendered  # Replace with the expected content


def test_render_to_string_with_context_instance(template_engine):
    user = User.objects.create(username='testuser')
    context_instance = Context({'user': user})
    rendered = template_engine.render_to_string('test_template.html', context_instance)
    assert 'Expected Content' in rendered  # Replace with the expected content


def test_render_to_string_template_does_not_exist(template_engine):
    with pytest.raises(TemplateDoesNotExist):
        template_engine.render_to_string('non_existent_template.html')


def test_render_to_string_with_none_context(template_engine):
    user = User.objects.create(username='testuser')
    rendered = template_engine.render_to_string('test_template.html', None)
    assert 'Expected Content' in rendered  # Replace with the expected content
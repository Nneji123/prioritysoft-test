import pytest
import os
from core.utils import read_code_sample, get_code_samples

@pytest.fixture
def sample_file(tmpdir):
    def create_sample_file(app_name, view_name, language, content):
        path = tmpdir.mkdir("docs").mkdir("code_samples").mkdir(app_name).mkdir(view_name).join(f"{language}.txt")
        path.write(content)
        return path
    return create_sample_file

def test_read_code_sample(sample_file):
    app_name = "my_app"
    view_name = "my_view"
    language = "python"
    sample_file(app_name, view_name, language, "print('Hello, world!')")
    
    content = read_code_sample(app_name, view_name, language)
    assert content == "print('Hello, world!')"

def test_read_code_sample_file_not_found():
    content = read_code_sample("non_existent_app", "non_existent_view", "python")
    assert content == "Code sample for python not found."

def test_get_code_samples(sample_file):
    app_name = "my_app"
    view_name = "my_view"
    languages = ["typescript", "javascript", "python", "dart", "curl"]
    for lang in languages:
        sample_file(app_name, view_name, lang, f"{lang} sample content")
    
    samples = get_code_samples(app_name, view_name)
    assert len(samples) == len(languages)
    for sample in samples:
        assert sample["source"] == f"{sample['lang']} sample content"
import pytest
import os
import shutil
from src.utils.file_exporter import FileExporter

@pytest.fixture
def temp_output_dir():
    test_dir = "test_outputs"
    yield test_dir
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

@pytest.mark.asyncio
async def test_save_markdown_creates_file(temp_output_dir):
    exporter = FileExporter(base_dir=temp_output_dir)
    title = "Test Article"
    content = "# This is a test content"
    
    file_path = await exporter.save_markdown(title, content)
    
    assert os.path.exists(file_path)
    assert file_path.endswith(".md")
    
    with open(file_path, "r", encoding="utf-8") as f:
        saved_content = f.read()
    assert saved_content == content

@pytest.mark.asyncio
async def test_save_markdown_sanitizes_filename(temp_output_dir):
    exporter = FileExporter(base_dir=temp_output_dir)
    title = "My Complex Article Title !!! 123"
    content = "Content"
    
    file_path = await exporter.save_markdown(title, content)
    filename = os.path.basename(file_path)
    
    # Check if special characters were replaced by underscores
    assert "!" not in filename
    assert "complex_article_title" in filename

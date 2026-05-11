import os
import aiofiles
from datetime import datetime

class FileExporter:
    """
    Utility to export AI-generated content to files (Markdown, JSON).
    Follows 'Async First' mandate using aiofiles.
    """
    def __init__(self, base_dir: str = "outputs"):
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    async def save_content(self, title: str, content: str, sub_dir: str, extension: str = "md") -> str:
        """
        Saves content to a file in the specified sub_dir.
        Returns the path to the saved file.
        """
        target_dir = os.path.join(self.base_dir, sub_dir)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Sanitize filename: lowercase, replace spaces with underscores
        safe_title = "".join([c if c.isalnum() else "_" for c in title.lower()]).strip("_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{safe_title}.{extension}"
        file_path = os.path.join(target_dir, filename)

        async with aiofiles.open(file_path, mode='w', encoding='utf-8') as f:
            await f.write(content)

        return file_path

    async def save_markdown(self, title: str, content: str, sub_dir: str = "articles") -> str:
        """Legacy wrapper for save_content."""
        return await self.save_content(title, content, sub_dir, "md")

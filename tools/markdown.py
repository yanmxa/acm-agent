import re


# install index all the content, we can choose only embedding the title and description
def extract_title_and_description(markdown_content):
    # Extract title (H1 heading)
    title_match = re.search(r"^# (.+)", markdown_content, re.MULTILINE)
    title = title_match.group(1) if title_match else "No title found"

    # Extract description (the content after the "## Description" heading)
    description_match = re.search(
        r"## Description\s*\n([\s\S]*?)(\n##|\Z)", markdown_content, re.MULTILINE
    )
    description = (
        description_match.group(1).strip()
        if description_match
        else "No description found"
    )

    return title, description

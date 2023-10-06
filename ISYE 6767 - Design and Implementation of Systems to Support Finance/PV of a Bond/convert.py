import markdown

# Convert the markdown content to HTML
html_content = markdown.markdown(open("report.md","r+"))

# Save the HTML content to a file
html_file_path = "./homework_2_report.html"
with open(html_file_path, "w") as file:
    file.write(html_content)


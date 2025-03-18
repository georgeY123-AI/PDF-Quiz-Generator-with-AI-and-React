import os

# Define the directory structure
structure = {
    "quiz-generator": {
        "src": {
            "components": {
                "PDFUploader.js": "",
                "QuizDisplay.js": ""
            },
            "App.js": "",
            "App.css": "",
            "index.js": ""
        },
        "package.json": ""
    }
}

# Function to create directories and files
def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # If content is a dictionary, it's a directory
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            # If content is not a dictionary, it's a file
            with open(path, 'w') as file:
                if content:
                    file.write(content)

# Create the structure
create_structure(".", structure)

print("Directory structure and files created successfully.")
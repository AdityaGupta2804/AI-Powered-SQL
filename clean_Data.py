import zipfile
# Path to the downloaded ZIP file
zip_path = 'archive.zip'

# Extract the contents to a folder
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall('extracted_data')  # Creates a folder called 'extracted_data'
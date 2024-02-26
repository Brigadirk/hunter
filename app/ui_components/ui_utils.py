import os

def save_uploaded_file(uploaded_file, tmpdirname, tmpfilename):
    if uploaded_file:
        file_path = os.path.join(tmpdirname, tmpfilename)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    else:
        return ""

def save_uploaded_file_list(files, tmpdirname):
    files_paths = []
    if files:
        for file in files:
            if file:
                # Write file to the temporary directory
                file_path = os.path.join(tmpdirname, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getvalue())
                files_paths.append(file_path)
    return files_paths

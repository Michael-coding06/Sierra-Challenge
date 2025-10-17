def DOS_prevention (upload_file, max_size):
    return upload_file.size <= max_size * 1024 * 1024

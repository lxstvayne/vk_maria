from ..types.input_file import InputFile


def prepare_multipart(file: InputFile):
    return file.filename, file.read()


def prepare_files(*files: InputFile):
    return [(f'file{i}', (prepare_multipart(file))) for i, file in enumerate(files, start=1)]

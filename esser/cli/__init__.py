import os


class BaseProject(object):

    base_files = (
        '__init__.py',
        'app.py',
        'requirements.txt',
        'cloudformation'
    )

    def __init__(self, project_dir):
        self.project_dir = project_dir

    def create(self):
        for filename in self.base_files:
            if '.' in filename:
                file = open(
                    os.path.join(self.project_dir, filename),
                    'wb'
                )
                file.write('')
            
        return self.project_dir


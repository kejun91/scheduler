import os
from app.main.web.decorator import webpage
from app.utils.path import get_project_root_dir


@webpage("/")
def start_app(path):
    web_dir = os.path.join(get_project_root_dir(),'web')
    file_path = os.path.join(web_dir,path.strip('/'))

    if not path.strip('/').startswith(('images','static','favicon.ico','index.html')):
        file_path = os.path.join(web_dir,'index.html')

    return file_path
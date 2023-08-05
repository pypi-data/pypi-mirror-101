def get_cv_version() -> str:
    try:
        import cv2
        string = '* Open cv version {}'.format(cv2.getVersionString())
    except (ImportError, ModuleNotFoundError, NameError) as err:
        string = '* {}'.format(err)
    return string


def main():
    return

# File lock class for synchronizing write access to /tmp
class FileLock:
    import threading
def __enter__(self):
        self._lock = threading.Lock()
        self._lock.acquire()
        self._fd = open(
            "/tmp/lockfile.LOCK", "w+"
        )
        fcntl.lockf(
            self._fd, fcntl.LOCK_EX
        )
def __exit__(
    self, type, value, traceback
):
    self._fd.close()
    self._lock.release()

@udf(
    name="predict_nba_salary",
    is_permanent=True,
    replace=True,
    stage_location="@udf",
    imports=[("my_dnn_model.zip")],
)
def predict_salary(years: int) -> float:
    import fcntl
    import os
    import sys
    import zipfile
    
# Get the location of the import directory. Snowflake sets the import
    # directory location so code can retrieve the location via sys._xoptions.
    IMPORT_DIRECTORY_NAME = (
        "snowflake_import_directory"
    )
    import_dir = sys._xoptions[
        IMPORT_DIRECTORY_NAME
    ]
# Get the path to the ZIP file and set the location to extract to.
    zip_file_path = (
        import_dir + "my_dnn_model.zip"
    )
extracted = "/tmp"
    # Extract the contents of the ZIP. This is done under the file lock
    # to ensure that only one worker process unzips the contents.
    with FileLock():
        if not os.path.isdir(
            extracted
            + "/my_dnn_model/saved_model.pb"
        ):
            with zipfile.ZipFile(
                zip_file_path, "r"
            ) as myzip:
                myzip.extractall(
                    extracted
                )
my_model = (
        tf.keras.models.load_model(
            extracted + "/my_dnn_model"
        )
    )
x = tf.linspace(years, years, 1)
    y = my_model.predict_on_batch(x)
    return 1000000 * y.tolist()[0][0]
import logging
import re
import fnmatch
from typing import List, Tuple
import os
import os.path
import sys
from subprocess import Popen, PIPE
import shutil
import datetime

SOFFICE_PATH = shutil.which("soffice")
JAVA_PATH = shutil.which("java")
RESOURCES_PATH = os.path.dirname(os.path.abspath(__file__)) + "/resources/"
SAXON_PATH = os.getenv("SAXON_PATH") or (RESOURCES_PATH + "saxon9.jar")

if not SOFFICE_PATH:
    sys.exit("Could not find soffice. Is it in your PATH ?")
if not JAVA_PATH:
    sys.exit("Could not find java. Is it in your PATH ?")
if not SAXON_PATH:
    sys.exit(
        "Could not find the Saxon jar. Please set SAXON_PATH environment variable."
    )
if not os.path.isfile(SAXON_PATH):
    sys.exit(
        "Could not find the Saxon jar. Please check your SAXON_PATH environment variable."
    )


def _silent_remove(path: str):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def _stamp():
    return datetime.datetime.now()


def _find_files(what: str, where: str = ".") -> List[str]:
    rule = re.compile(fnmatch.translate(what), re.IGNORECASE)
    return [
        "{}{}{}".format(where, os.path.sep, name)
        for name in os.listdir(where)
        if rule.match(name)
    ]


def _process_doc(
    doc_file, working_dir: str, logger: logging.Logger
) -> Tuple[bool, str]:
    doc_file_no_extension = os.path.splitext(doc_file)[0]

    #
    # STEP 1, convert to XML
    #
    p = Popen(
        [
            SOFFICE_PATH,
            "--invisible",
            "--convert-to",
            "xml:OpenDocument Text Flat XML",
            "--outdir",
            working_dir,
            doc_file,
        ],
        stdout=PIPE,
        stderr=PIPE,
    )
    out, err = p.communicate()
    if p.returncode != 0:
        return (
            False,
            err.decode("utf-8") if err else "sub-process provided no error output",
        )
    else:
        logger.info(
            {
                "message": "Wrote {}".format(
                    os.path.basename(doc_file_no_extension + ".xml")
                ),
                "time": _stamp(),
            }
        )
    p.terminate()

    #
    # STEP 2, cleanup
    #
    p = Popen(
        [
            JAVA_PATH,
            "-jar",
            SAXON_PATH,
            doc_file_no_extension + ".xml",
            RESOURCES_PATH + "cleanup.xsl",
        ],
        stdout=PIPE,
        stderr=PIPE,
    )
    out, err = p.communicate()
    if p.returncode != 0:
        return (
            False,
            err.decode("utf-8") if err else "sub-process provided no error output",
        )
    else:
        with open(doc_file_no_extension + "_01_clean.xml", "wb") as f:
            f.write(out)
            logger.info(
                {
                    "message": "Wrote {}".format(
                        os.path.basename(doc_file_no_extension + "_01_clean.xml")
                    ),
                    "time": _stamp(),
                }
            )

    #
    # STEP 3, hierarchy
    #
    p = Popen(
        [
            JAVA_PATH,
            "-jar",
            SAXON_PATH,
            doc_file_no_extension + "_01_clean.xml",
            RESOURCES_PATH + "hierarchize.xsl",
        ],
        stdout=PIPE,
        stderr=PIPE,
    )
    out, err = p.communicate()
    if p.returncode != 0:
        return (
            False,
            err.decode("utf-8") if err else "sub-process provided no error output",
        )
    else:
        with open(doc_file_no_extension + "_02_hierarchize.xml", "wb") as f:
            f.write(out)
            logger.info(
                {
                    "message": "Wrote {}".format(
                        os.path.basename(doc_file_no_extension + "_02_hierarchize.xml")
                    ),
                    "time": _stamp(),
                }
            )

    _silent_remove(doc_file)
    _silent_remove(doc_file_no_extension + ".xml")
    _silent_remove(doc_file_no_extension + "_01_clean.xml")

    return True, "All OK"


def doc2tei(working_dir: str, logger: logging.Logger, options: dict = None):
    success_counter = 0
    failure_counter = 0
    doc_files = _find_files("*.docx", working_dir) + _find_files("*.odt", working_dir)
    logger.info(
        {"message": "{} file(s) to convert.".format(len(doc_files)), "time": _stamp()}
    )
    for doc_file in doc_files:
        logger.info(
            {
                "message": "converting {}".format(os.path.basename(doc_file)),
                "time": _stamp(),
            }
        )
        success, output = _process_doc(doc_file, working_dir, logger)
        if not success:
            logger.error(
                {
                    "message": "could not convert {}".format(
                        os.path.basename(doc_file)
                    ),
                    "output": output,
                    "time": _stamp(),
                }
            )
            failure_counter = failure_counter + 1
        else:
            success_counter = success_counter + 1
            logger.info(
                {
                    "message": "{}: success".format(os.path.basename(doc_file)),
                    "time": _stamp(),
                }
            )
    logger.info(
        {"message": "Job done", "time": _stamp(), "File(s) converted": success_counter}
    )


doc2tei.description = {
    "label": "Docx vers TEI",
    "help": "Convertir les fichiers *.docx et *.odt en fichiers *.xml (vocabulaire TEI)",
    "options": [],
}

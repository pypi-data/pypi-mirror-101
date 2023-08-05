# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.

import sys
import tqdm

from ...utility import *
from ...analysis import *
from .logger import *


class Workspace(Logger):

    logger_name = "workspace"

    @classmethod
    def create_path_line_sentences(cls, xml_directory, pls_directory, language, tokenizer, *, reset = False):
        existing_files = glob.glob(os.path.join(pls_directory, "*.txt"))

        if len(existing_files) > 0:
            if not reset:
                cls.log(f"Path line sentences already exist at {pls_directory}. Skipping.")
                return
            else:
                cls.log(f"Path line sentences exist at {pls_directory}. Removing.")
                for path in existing_files:
                    os.remove(path)
                cls.log("Existing files were removed.")

        cls.log("Creating path line sentences...")

        page_iterator = PageIterator(xml_directory)

        with FileWriter(pls_directory, "{:06d}.txt", 10000) as writer, tqdm.tqdm(page_iterator) as pager:
            for page in pager:
                pager.set_postfix(OrderedDict(reader = f"{page_iterator.i_path}/{page_iterator.n_path}", writer = f"{writer.file_count}"))
                entry = Parser.page_to_class(page, language = language, entry_only = True)

                if entry is None:
                    continue

                plain_text = Parser.to_plain_text(entry["mediawiki"], language = language)
                plain_text = plain_text.replace("\n", " ").strip()

                line = " ".join(tokenizer.split(plain_text))

                writer.write(line + "\n")

        cls.log("Done!")

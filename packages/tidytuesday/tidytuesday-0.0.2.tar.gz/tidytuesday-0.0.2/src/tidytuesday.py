from datetime import datetime
import pandas as pd
from base64 import b64decode
from io import BytesIO
from github import Github
import functools
import os


REPO = "rfordatascience/tidytuesday"
PARSERS = {
    "csv": pd.read_csv,
    "xlsx": pd.read_excel,
    "tsv": functools.partial(pd.read_csv, delimiter="\t"),
}


def get_pat():
    if os.environ["GITHUB_PAT"]:
        return os.environ["GITHUB_PAT"]
    if os.environ["GITHUB_TOKEN"]:
        return os.environ["GITHUB_TOKEN"]

    return ""


class TidyTuesday:
    def __init__(self, date, auth=get_pat()):
        self.date = datetime.strptime(date, "%Y-%m-%d").date()

        if self.date.weekday() != 1:
            raise ValueError(f'{self.date.strftime("%Y-%m-%d")} is not a Tuesday')

        self.date = self.date.strftime("%Y-%m-%d")
        self.gh = Github(auth)
        self.repo = self.gh.get_repo(REPO)
        self.load_context()
        self.download_files()

    def get_blob(self, sha):
        return b64decode(self.repo.get_git_blob(sha).content)

    def load_context(self):
        tree = self.repo.get_git_tree("master:static")

        # get shas of files in static folder
        static_sha = {}
        for path in tree.tree:
            static_sha[path.path] = path.sha

        ttdt = pd.read_csv(BytesIO(self.get_blob(static_sha["tt_data_type.csv"])))
        file_info = ttdt.loc[
            ttdt["Date"] == self.date, ["data_files", "data_type", "delim"]
        ]

        if file_info["data_files"].isna().all():
            raise ValueError("No TidyTuesday for this Tuesday")

        # compile info for data files
        self._file_info = {}
        for _, row in file_info.iterrows():
            self._file_info[row["data_files"]] = (row["data_type"], row["delim"])

        # get shas of files
        tree = self.repo.get_git_tree(f"master:data/{self.date[:4]}/{self.date}/").tree
        self.sha = {x.path: x.sha for x in tree}
        if "readme.md" in self.sha:
            self.readme = self.get_blob(self.sha["readme.md"]).decode("utf-8")
        else:
            print("\033[1m--- No readme detected ---\033[0m")

    def download_files(self):
        total = len(self._file_info)

        if total > 1:
            print(f"\033[1m--- There are {total} files available ---\033[0m")
        else:
            print("\033[1m--- There is 1 file available ---\033[0m")

        print("\033[1m--- Starting download ---\033[0m\n")

        for i, (file, (dtype, delim)) in enumerate(self._file_info.items()):
            print(f"\tDownloading file {i+1} of {total}: {file}")

            content = self.get_blob(self.sha[file])
            parser = PARSERS[dtype]
            if str(delim) != "nan":
                parser = functools.partial(parser, delimiter=delim)

            setattr(
                self, file.split(".")[0].replace("-", "_"), parser(BytesIO(content))
            )

        print("\n\033[1m--- Download complete ---\033[0m")

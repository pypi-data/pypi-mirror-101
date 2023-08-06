![GitLab pipeline](https://img.shields.io/gitlab/pipeline/shotakaha/snapsheets?style=for-the-badge)
![PyPI - Licence](https://img.shields.io/pypi/l/snapsheets?style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/snapsheets?style=for-the-badge)
![PyPI - Status](https://img.shields.io/pypi/status/snapsheets?style=for-the-badge)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/snapsheets?style=for-the-badge)


# Snapsheets

Wget snapshots of Google Spreadsheets

This package enables to wget Google Spreadsheets without login.
(Spreadsheets should be shared with public link)


---

# Usage

```python
>>> import snapsheets as ss
>>> sample_url1 = "https://docs.google.com/spreadsheets/d/1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM/edit#gid=0"
>>> sheet = ss.Sheet(url=sample_url1, desc="Get Sample Sheet")
>>> sheet.snapshot()
📣 Get Sample Sheet
🤖 Downloaded snapd/snapsheet.xlsx
🚀 Renamed to snapd/20210412T104727_snapsheet.xlsx
```

---
## Command Line Tool with configuration files (from v0.5.0)

- Make ``./config/`` directory and place your TOML/YAML configuration files.
  - If ``./config/`` does not exist, it will search from ``. (current directory)``.
- Downloaded files are saved to ``./snapd/`` directory
  - If ``./snapd/`` does not exit, it will be saved in ``. (current directory)``.
  - (Options to switch directory might be added later)

```bash
$ snapsheets
📣 Example for Snapshot module (in TOML)
🤖 Downloaded snapd/snapsheet.xlsx
🚀 Renamed to snapd/2021_toml_sample1.xlsx
📣 20210304_storage_comparison
🤖 Downloaded snapd/snapsheet.xlsx
🚀 Renamed to snapd/20210412_toml_sample2.xlsx
```

---

## Command Line Tool with Single file (from v0.5.0)

- Use ``--url`` option to download single spreadsheet.
- Downloaded file is automatically named as ``snapsheet.xlsx``
- (More options might be added later)

```bash
$ snapsheets --url "https://docs.google.com/spreadsheets/d/1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM/edit#gid=0"
📣 snapsheet
🤖 Downloaded snapd/snapsheet.xlsx
🚀 Renamed to snapd/20210412T104926_snapsheet.xlsx
```

---

# v0.2.3 or older

- Added DeprecationWarnings
- It still works

```python
>>> print("💥💥💥 deprecated since version 0.2.3 💥💥💥")
>>> fname = "config/config.yml"
>>> ss.config.add_config(fname)
snapsheets/sandbox/snapper.py:28: DeprecationWarning: Call to deprecated function (or staticmethod) add_config. (Will be removed.) -- Deprecated since version 0.2.3.
  ss.config.add_config(fname)
>>> fname = "config/gsheet.yml"
>>> ss.config.add_config(fname)
snapsheets/sandbox/snapper.py:30: DeprecationWarning: Call to deprecated function (or staticmethod) add_config. (Will be removed.) -- Deprecated since version 0.2.3.
  ss.config.add_config(fname)
>>> fname = ss.gsheet.get("test1", by="wget")
snapsheets/sandbox/snapper.py:31: DeprecationWarning: Call to deprecated function (or staticmethod) get. (Will be removed) -- Deprecated since version 0.3.0.
  fname = ss.gsheet.get("test1", by="wget")
2021-04-07 19:44:18 - INFO - gsheet.py - snapsheets.gsheet - download - ダウンロードするよ : test1
2021-04-07 19:44:19 - INFO - gsheet.py - snapsheets.gsheet - download - ダウンロードしたよ : snapd/test_sheet.xlsx
2021-04-07 19:44:19 - INFO - gsheet.py - snapsheets.gsheet - backup - 移動するよ : test_sheet.xlsx
2021-04-07 19:44:19 - INFO - gsheet.py - snapsheets.gsheet - backup - 移動したよ : 2021_test_sheet.xlsx
```

---


# Documents

- https://shotakaha.gitlab.io/snapsheets/

---

# PyPI package

- https://pypi.org/project/snapsheets/

![PyPI - Downloads](https://img.shields.io/pypi/dd/snapsheets?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dw/snapsheets?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dm/snapsheets?style=for-the-badge)

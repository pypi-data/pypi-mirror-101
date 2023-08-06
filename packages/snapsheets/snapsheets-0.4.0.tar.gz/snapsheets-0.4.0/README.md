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
>>> ss.add_config('test_config.yml')
>>> ss.get('test1', by='wget')
```

---

## Configuration

- Make your config files in ``./config/``


```yaml
volumes:
  snapd: 'snapd/'
  logd: 'varlogs/'

options:
  wget:
    '--quiet'

datefmt:
  '%Y%m%dT%H%M%S'

sheets:
  test1:
    key: '1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM'
    gid: 'None'
    format: 'xlsx'
    sheet_name:
      - 'シート1'
      - 'シート2'
    stem: 'test_sheet'
    datefmt: '%Y'
```

## ``volumes``

- directories to save data

## ``options``

- set options for ``wget``

## ``datefmt``

- set prefix to saved spreadsheet

## ``sheet``

- google spreadsheet info


---

# Documents

- https://shotakaha.gitlab.io/snapsheets/

---

# Stats

![PyPI - Downloads](https://img.shields.io/pypi/dd/snapsheets?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dw/snapsheets?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dm/snapsheets?style=for-the-badge)

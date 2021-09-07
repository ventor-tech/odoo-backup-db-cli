# odoo-backup-db-cli

[![Build Status](https://github.com/ventor-tech/odoo-backup-db-cli/workflows/test/badge.svg?branch=main&event=push)](https://github.com/ventor-tech/odoo-backup-db-cli/actions?query=workflow%3Atest)
[![Python Version](https://img.shields.io/pypi/pyversions/odoo-backup-db-cli.svg)](https://pypi.org/project/odoo-backup-db-cli/)
[![Documentation Status](https://readthedocs.org/projects/odoo-backup-db-cli/badge/?version=latest)](https://odoo-backup-db-cli.readthedocs.io/en/latest/?badge=latest)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

Tool to create full backup of odoo database and filestore

[Features](##features)
[Installation](##installation)
[Configuration](##configuration)
[Example of creating cron](##examples-of-creating-cron)
 - [simple cron](###simple-cron)
 - [with anaconda](###with-anaconda)

[License](##license)
[Credits](#credits)

## Features
- Support local backup, ftp/sftp protocols and AWS S3
- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)

## Installation

```bash
pip install odoo-backup-db-cli
```

## Configuration

Here is a config example:
 ```
[common]
db_host = localhost
db_port = 5432
db_username = ***
db_password = ***
db_name = ***
with_db = True
with_filestore = True
clean_backup_after = 7
filestore_location = /local/path/to/source/filestore/
[s3]
bucket = viveodoobackup
access_key = AAAAAAAAAAAAAAA
secret_key = aaaaaaaaaaaaaaaaaaaaaaaaaaaa
clean_backup_after = 1
[local1]
backup_location = /Users/veronika/dev/test_bk/
[local2]
backup_location = /Users/veronika/dev/test_bk2/
[ftp]
backup_location = /utires/testbackup
host = 1.111.11.111
port = 21
username = ftpuser
password = ***********
[sftp1]
backup_location = /path/to
host = 1.135.73.147
port = 22
username = sftpuser
password = *********
 ```

With the config above you can run different kinds of backuping:

`odoo-backup-db-cli create-backup local1 -t local -p ~/.config/odoo-backup-db-cli.conf`

`odoo-backup-db-cli create-backup s3 -p ~/.config/odoo-backup-db-cli.conf`

`odoo-backup-db-cli create-backup ftp -p ~/.config/odoo-backup-db-cli.conf`

`odoo-backup-db-cli create-backup sftp1 -t sftp -p ~/.config/odoo-backup-db-cli.conf`

where thw first argument is a config section, `-t` is a type of backuping, `-p` is a path to the config file


## Examples of creating cron

### Simple cron

Let's say you want to create cron to backup every hour.
Then you need:

1. Type `crontab -e` and add the command:

    `0 * * * * odoo-backup-db-cli create-backup s3 -p ~/.config/odoo-backup-db-cli.conf`

### With anaconda

1. Copy snippet appended by Anaconda in `~/.bashrc` (at the end of the file) to a separate file `~/.bashrc_conda`

    As of Anaconda 2020.02 installation, the snippet reads as follows:

    ```bash
    # >>> conda initialize >>>
    # !! Contents within this block are managed by 'conda init' !!
    __conda_setup="$('/home/USERNAME/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
    if [ $? -eq 0 ]; then
        eval "$__conda_setup"
    else
        if [ -f "/home/USERNAME/anaconda3/etc/profile.d/conda.sh" ]; then
            . "/home/USERNAME/anaconda3/etc/profile.d/conda.sh"
        else
            export PATH="/home/USERNAME/anaconda3/bin:$PATH"
        fi
    fi
    unset __conda_setup
    # <<< conda initialize <<<
    ```

    Make sure that:

    - The path `/home/USERNAME/anaconda3/` is correct.
    - The user running the cronjob has read permissions for `~/.bashrc_conda` (and no other user can write to this file).

2. In `crontab -e` add lines to run cronjobs on `bash` and to source `~/.bashrc_conda`

    Run `crontab -e` and insert the following before the cronjob:

    ```bash
    SHELL=/bin/bash
    BASH_ENV=~/.bashrc_conda
    ```

3. In `crontab -e` include at beginning of the cronjob `conda activate my_env;` as in example

    Example of entry for a script that would execute at noon 12:30 each day on the Python interpreter within the conda environment:

    ```bash
    30 12 * * * conda activate my_env; odoo-backup-db-cli create-backup production_local_with_filestore; conda deactivate
    ```

And that's it.

You may want to check from time to time that the snippet in `~/.bashrc_conda` is up to date in case conda updates its snippet in `~/.bashrc`.

## License

[agpl3](https://github.com/ventor-tech/odoo-backup-db-cli/blob/master/LICENSE)

## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [88c80f5d17a6f4bc41dbc5473db4f5ffd2b3068f](https://github.com/wemake-services/wemake-python-package/tree/88c80f5d17a6f4bc41dbc5473db4f5ffd2b3068f). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/88c80f5d17a6f4bc41dbc5473db4f5ffd2b3068f...master) since then.

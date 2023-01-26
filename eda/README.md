# Event-Driven Ansible example

This directory contains a source plugin (`new_records.py`) for Event-Drive Ansible (EDA) along with a rulebook and playbook to execute. The source plugin accepts arguments for username, password, ServiceNow instance and table (the table you want to watch for new records being created).

- To test the script independently, first set environment variables for `SN_HOST`, `SN_USERNAME`, `SN_PASSWORD` and `SN_TABLE` and run:
~~~
python new_records.py
~~~

- To test the script from `ansible-rulebook` (the CLI component of EDA), set environment variables for `SN_HOST`, `SN_USERNAME`, `SN_PASSWORD` and `SN_TABLE` and run:
~~~
ansible-rulebook --rulebook new_records_rulebook.yml -i inventory.yml -S . --env-vars SN_HOST,SN_USERNAME,SN_PASSWORD
~~~

In above command, `-S` tells `ansible-rulebook` where to look for source plugins. Typically, these source plugins would be contained within an ansible collection, but this flag works well for testing.

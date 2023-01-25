# Event-Driven Ansible example

This directory contains a source plugin (`new_records.py`) for Event-Drive Ansible (EDA) along with a rulebook and playbook to execute. The source plugin accepts arguments for username, password, ServiceNow instance and table (the table you want to watch for new records being created).

- To test the script indepently, first specify environment variables for `SN_HOST`, `SN_USERNAME`, `SN_PASSWORD` and `SN_TABLE` and run:
~~~
python new_records.py
~~~

- To test the script from `ansible-rulebook` (the CLI component of EDA), set parameters in the rulebook for instance, username, password, and table and run:
~~~
ansible-rulebook_rulebook --rulebook new_records.yml -i inventory -S . --verbose
~~~

In above command, `-S` tells `ansible-rulebook` where to look for source plugins. Typically, these source plugins would be contained within an ansible collection, but this flag works well for testing.

- If you'd like to obscure username, password, and instance url, you can export environment variables and pass them in like so: 
~~~
ansible-rulebook --rulebook new_records_rulebook.yml -i inventory.yml -S . --env-vars SN_HOST,SN_USERNAME,SN_PASSWORD
~~~

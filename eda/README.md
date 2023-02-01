# Event-Driven Ansible example

This directory contains an example source plugin (`new_records.py`) for Event-Drive Ansible (EDA) along with a rulebook and playbook to execute. The source plugin accepts arguments for username, password, ServiceNow instance and table (the table you want to watch for new records being created).

- To test the script independently, first set environment variables for `SN_HOST`, `SN_USERNAME`, `SN_PASSWORD` and `SN_TABLE` and run:
~~~
python new_records.py
~~~

- To test the script from `ansible-rulebook` (the CLI component of EDA), set environment variables for `SN_HOST`, `SN_USERNAME`, `SN_PASSWORD` and `SN_TABLE` and run:
~~~
ansible-rulebook --rulebook new_records_rulebook.yml -i inventory.yml -S . --env-vars SN_HOST,SN_USERNAME,SN_PASSWORD
~~~

In above command, `-S` tells `ansible-rulebook` where to look for source plugins. Typically, these source plugins would be contained within an ansible collection, but this flag works well for testing.

The `--env-vars` flag passes the specified environment variables into the execution of this rulebook. These environment variables match the names of the variable pulled in as a part of the arguents passed into the source plugin as defined in the source configuration in the rulebook:

~~~
  sources:
    - new_records:
        instance: "{{ SN_HOST }}"
        username: "{{ SN_USERNAME }}"
        password: "{{ SN_PASSWORD }}" 
        table: incident
        interval: 1
~~~~

After executing the rulebook with the above command, create a new incident as the same user. Success looks like:
```
vscode ➜ /workspaces/cloin-snow/eda (main) $ ansible-rulebook --rulebook new_records_rulebook.yml -i inventory.yml -S . --env-vars SN_HOST,SN_USERNAME,SN_PASSWORD

PLAY [Get information from ServiceNow record] **********************************

TASK [Print record information] ************************************************
ok: [localhost] => {
    "msg": "Record: INC0012273, Description: Something truly incredible has happened!"
}

PLAY RECAP *********************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

------
This is used in a video on '6 guidelines for creating Event-Driven Ansible event source plugins' watch below
[![Watch the video](https://i.ytimg.com/vi/4f7ARUnVZmY/hqdefault.jpg)](https://www.youtube.com/watch?v=4f7ARUnVZmY)

# Event-Driven Ansible example

This directory contains an example source plugin (`new_records.py`) for Event-Drive Ansible (EDA) along with a rulebook and playbook to execute. The source plugin accepts arguments for username, password, ServiceNow instance and table (the table you want to watch for new records being created).

**Before you go out and test** my example plugin, please know that this plugin is coming from a sub-par python person, is meant to be an example and not at all endorsed or suggested for production use. ServiceNow instances also have rate limit rules for REST resources that you may hit by polling too often. Considering that the event push paradigm is preferred for Event-Driven Ansible source plugins, a better implementation of this source plugin might be to create a ServiceNow webservice to push event details to an event aggregator! In this scenario, our integrated application (ServiceNow) would PUSH event details to something like JetStream or Kafka (for which there is [already an event source plugin](https://github.com/ansible/event-driven-ansible/blob/main/plugins/event_source/kafka.py)!).

## Testing

### pre-requisites
- ansible-rulebook>=0.10.1 [[install instructions]](https://github.com/ansible/event-driven-ansible#getting-started)
- ansible-core>=2.14.1
- ansible collection(s):
    - ansible.eda>=1.3.3
----

- To test the script independently, first set environment variables for `SN_HOST`, `SN_USERNAME`, `SN_PASSWORD` and `SN_TABLE` and run:
~~~
python new_records.py
~~~

- To test the script from `ansible-rulebook` (the CLI component of EDA), set environment variables for `SN_HOST`, `SN_USERNAME`, `SN_PASSWORD` and `SN_TABLE` and run:
~~~
ansible-rulebook --rulebook new_records_rulebook.yml \
        -i inventory.yml \
        -S . \
        --env-vars SN_HOST,SN_USERNAME,SN_PASSWORD \
        --print-events
~~~

In above command, `-S` tells `ansible-rulebook` where to look for source plugins. Typically, these source plugins would be contained within an ansible collection, but this flag works well for testing.

`--print-events` is useful to show the entire event that triggered the action. With this enabled, you'll see all event data printed before the playbook output. 

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

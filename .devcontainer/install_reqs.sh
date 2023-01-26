# install python dependencies
pip install -r $1/requirements.txt

# install ansible collections
ansible-galaxy collection install -r $1/requirements.yml

# install ansible-rulebook (https://github.com/ansible/event-driven-ansible#getting-started)
ansible-playbook -i localhost, -c local ansible.eda.install_rulebook_cli

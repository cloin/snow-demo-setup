SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
pip install -r $SCRIPTPATH/../requirements.txt
ansible-galaxy collection install -r $SCRIPTPATH/../requirements.yml
ansible-playbook -i localhost, -c local ansible.eda.install_rulebook_cli

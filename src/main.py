import os
import json
import subprocess

class GovernanceOrchestrator:
    def __init__(self, config_path):
        self.config_path = config_path
        self.load_config()

    def load_config(self):
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)

    def execute_governance_action(self, action_name, params):
        action = self.config['actions'].get(action_name)
        if not action:
            raise ValueError(f'Action {action_name} not found in config')

        command = action['command'].format(**params)
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise RuntimeError(f'Error executing action {action_name}: {result.stderr.decode().strip()}')

        return result.stdout.decode().strip()

if __name__ == '__main__':
    orchestrator = GovernanceOrchestrator('config.json')
    print(orchestrator.execute_governance_action('create_proposal', {'title': 'Increase funding for community initiatives', 'description': 'Allocate an additional $50,000 to support local community projects.', 'voting_duration': '2 weeks'}))

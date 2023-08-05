from rivery_cli.globals import global_keys, global_settings
import yaml
from rivery_cli import RiverySession


def content_loader(content):
    """ObjectHook to convert the content into more "reliable" content """
    new_content = {}
    primary_type = content.get('block_primary_type')
    new_content['block_primary_type'] = primary_type
    new_content['block_type'] = content.get('block_type')

    if primary_type == 'river':
        new_content['block_primary_type'] = primary_type
        new_content['river_id'] = content.get('river_id')
    else:
        new_content['connection_id'] = content.pop('gConnection', content.get('connection_id'))
        new_content.update(content)
    return new_content


def step_importer(steps: list):
    """ Convert the steps to the right keys in the yaml file """
    # Make the steps list
    all_steps = []
    for step in steps:
        current_step = {}
        current_step["type"] = "step" if step.get('content', []) else "container"
        current_step["isEnabled"] = step.pop("isEnabled", True)
        current_step["step_name"] = step.pop("step_name", "Logic Step")
        if current_step.get('type') == "step":
            # Update the step definition as it exists in the content
            current_step.update(content_loader(step.pop("content", {})))
            # In order to "purge" any "Type" key comes from the river
            current_step['type'] = 'step'
        else:
            # Update the CONTAINER definition
            current_step["isParallel"] = step.pop('isParallel', False)
            current_step["container_running"] = step.pop("container_running", "run_once")
            current_step["loop_over_value"] = step.pop("loop_over_value", "")
            current_step["loop_over_variable_name"] = step.pop("loop_over_variable_name", [])
            current_step["steps"] = step_importer(
                steps=step.pop('nodes', [])
            )

        all_steps.append(current_step)

    return all_steps


def import_(**def_):
    """Import a river into a yaml definition """
    # Set the basics dictionary stucture
    final_response = {
        global_keys.BASE: {
            global_keys.VERSION: global_settings.__version__,
            global_keys.ENTITY_TYPE: "river",
            global_keys.CROSS_ID: str(def_.get(global_keys.CROSS_ID)),
            global_keys.DEFINITION: {}
        }
    }

    definition_ = {
        global_keys.PROPERTIES: {},
        global_keys.SCHEDULING: {}
    }

    # Get the river definitions from the def_
    river_definition = def_.get(global_keys.RIVER_DEF, {})

    # Populate IDS, and globals from the river
    definition_.update({
        "name": river_definition.get(global_keys.RIVER_NAME),
        "description": river_definition.get(global_keys.RIVER_DESCRIPTION) or 'Imported by Rivery CLI',
        global_keys.ENTITY_TYPE: river_definition.get('river_type_id')
    })

    # Run on the tasks definitions, and set it out
    tasks_def = def_.get(global_keys.TASKS_DEF, [])
    for task in tasks_def:
        task_config = task.get(global_keys.TASK_CONFIG, {})
        # Run on each task, and set the right keys to the structure
        definition_[global_keys.PROPERTIES]["steps"] = step_importer(
            steps=task_config.get("logic_steps", []))

        # Update the variables for the logic
        definition_[global_keys.PROPERTIES]["variables"] = task_config.get('variables', {})

        if task.get(global_keys.SCHEDULING, {}).get('isEnabled'):
            definition_[global_keys.SCHEDULING] = {"cronExp": task.get(global_keys.SCHEDULING, {}).get("cronExp"),
                                           "isEnabled": task.get(global_keys.SCHEDULING, {}).get('isEnabled'),
                                           "startDate": task.get(global_keys.SCHEDULING, {}).get('startDate'),
                                           "endDate": task.get(global_keys.SCHEDULING, {}).get('endDate')}

    final_response[global_keys.BASE][global_keys.DEFINITION] = definition_

    return final_response


def run():
    session = RiverySession(
        host='https://dev.app.rivery.io',
        token="eyJhbGciOiJIUzI1NiIsImV4cCI6MTkyOTQ0NDY0NiwiaWF0IjoxNjE0MDg0NjQ2fQ.eyJhY2MiOiI1NjY0M2U2NzcwZWMwN2U2MjRkNDMzNTEiLCJzY29wZXMiOnsiNTY4MTdiMWU5NjRjZGQ2ODQxZDA5NTZkIjpbInJpdmVyOmV4ZWN1dGUiLCJyaXZlcjpsaXN0IiwibWU6bGlzdCIsImNvbm5lY3Rpb246bGlzdCIsImNvbm5lY3Rpb246ZWRpdCIsImNvbm5lY3Rpb246ZGVsZXRlIiwiY29ubmVjdGlvbjp0ZXN0Iiwicml2ZXI6ZWRpdCIsInJpdmVyOmRlbGV0ZSJdfSwidG9rZW5fbmFtZSI6IkNMSSIsImlzcyI6IjU4YjgyMGEwYzc2MjcxMWQ4YzJmNjBjNyIsImp0aSI6Ijk5YmY3ZjIyMzExMzRiNTQ5MTdiZWY2MTcxOGQ0NmIzIiwiZW52IjoiNTY4MTdiMWU5NjRjZGQ2ODQxZDA5NTZkIiwic3ViIjoiUml2ZXJ5IEFQSSJ9.Ei_CWriITd_Nq0GKgxmCD3A-o6inFM-i22hc6DT1Ieo"

    )
    river = session.get_river(river_id='60005bb389f000001ef047aa')
    resp = import_(**river)
    return resp


if __name__ == '__main__':
    resp = run()
    with open('import_test.yaml', 'w') as yml:
        yaml.safe_dump(resp, yml,
                       line_break=True, width=2, allow_unicode=True)

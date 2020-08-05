#!/usr/bin/env python

import json
import os
import re
import sys

if 'CHEF_HOME' in os.environ:
    CHEF_HOME = os.environ['CHEF_HOME']
else:
    CHEF_HOME = os.path.join(os.environ['HOME'], 'wix', 'chef-repo')
RUN_REGEX = re.compile(r'^(role|recipe)\[([^:]*)(::)?(.*)]')
RECIPE_REGEX = re.compile(r'^\s*include_recipe\s*[\'"]([^:]*)(::)?([^\'"]*)[\'"]')


def get_run_list_from_recipe(recipe: tuple):
    (cookbook, recipe_name) = recipe
    recipe_file_name = os.path.join(CHEF_HOME, 'cookbooks', cookbook, 'recipes', f"{recipe_name}.rb")
    results = {'recipe': []}
    if not os.path.exists(recipe_file_name):
        recipe_file_name = os.path.join(CHEF_HOME, 'berks-cookbooks', cookbook, 'recipes', f"{recipe_name}.rb")
    with open(recipe_file_name, 'r') as recipe_file:
        for line in recipe_file.readlines():
            if 'include_recipe' in line:
                matched = RECIPE_REGEX.match(line)
                if not matched:
                    continue
                if matched[2] is None:
                    resource = (matched[1], 'default')
                else:
                    resource = (matched[1], matched[3])
                if resource not in results['recipe']:
                    results['recipe'].append(resource)
    return results


def get_run_list_from_role(role_name: str):
    role_file = os.path.join(CHEF_HOME, 'roles', f"{role_name}.json")
    resources = {'role': [], 'recipe': []}
    with open(role_file, 'r') as json_file:
        data = json.load(json_file)
    if 'run_list' not in data:
        return resources
    for item in iter(data['run_list']):
        matched = RUN_REGEX.match(item)
        if not matched:
            continue
        resource_type = matched[1]
        if resource_type == 'role':
            resource = matched[2]
            for (k, v) in get_run_list_from_role(resource).items():
                for i in v:
                    if i in resources[k]:
                        continue
                    resources[k].append(i)
        else:
            if matched[3] is None:
                recipe_name = 'default'
            else:
                recipe_name = matched[4]
            resource = (matched[2], recipe_name)
            for (k, v) in get_run_list_from_recipe(resource).items():
                for i in v:
                    if i in resources[k]:
                        continue
                    resources[k].append(i)
        if resource in resources[resource_type]:
            continue
        resources[resource_type].append(resource)
    return resources


def format_results(input_data):
    results = {'roles': [], 'recipes': []}
    for k, v in input_data.items():
        if k == 'role':
            results['roles'] = v
        else:
            results['recipes'] = [f"{m}::{n}" for m, n in v]
    return results


if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(json.dumps(format_results(get_run_list_from_role(sys.argv[1])), sort_keys=True, indent=2))
    else:
        print(json.dumps(format_results(get_run_list_from_role('packer-template')), sort_keys=True, indent=2))

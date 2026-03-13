import difflib 


def check_config(old_config, new_config):

    if old_config != new_config:

        diff = difflib.unified_diff(
            old_config.splitlines(),
            new_config.splitlines(),
            lineterm="")

        for i in diff:
            print(i)

    else:

        print("No Change Detected")
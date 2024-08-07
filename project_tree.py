import os

def print_directory_tree(path, indent=0):
    for item in os.listdir(path):
        print('  ' * indent + item)
        if os.path.isdir(os.path.join(path, item)):
            print_directory_tree(os.path.join(path, item), indent + 1)

print_directory_tree('.')
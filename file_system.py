class Partition:
    def __init__(self, name):
        self.name = name
        self.root = Directory("/", None)
        self.current_directory = self.root

class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.contents = {}

    def add(self, item):
        self.contents[item.name] = item

    def get(self, name):
        return self.contents.get(name)

    def list_contents(self):
        return self.contents.keys()

    def delete(self, name):
        if name in self.contents:
            del self.contents[name]
            return True
        return False

    def get_path(self):
        path = []
        current = self
        while current is not None:
            path.append(current.name)
            current = current.parent
        return "/".join(reversed(path)).replace("//", "/")

class File:
    def __init__(self, name):
        self.name = name

class FileSystem:
    def __init__(self):
        self.partitions = {}
        self.current_partition = None

    def mkpart(self, name):
        if name in self.partitions:
            print(f"Partition {name} already exists.")
        else:
            self.partitions[name] = Partition(name)
            self.current_partition = self.partitions[name]
            print(f"Partition {name} created and selected.")

    def rmpart(self, name):
        if name in self.partitions:
            del self.partitions[name]
            if self.current_partition and self.current_partition.name == name:
                self.current_partition = None
            print(f"Partition {name} deleted.")
        else:
            print(f"Partition {name} does not exist.")

    def select_partition(self, name):
        if name in self.partitions:
            self.current_partition = self.partitions[name]
            print(f"Partition {name} selected.")
        else:
            print(f"Partition {name} does not exist.")

    def mkdir(self, dirname):
        if self.current_partition:
            new_dir = Directory(dirname, self.current_partition.current_directory)
            self.current_partition.current_directory.add(new_dir)
            print(f"Directory {dirname} created.")
        else:
            print("No partition selected.")

    def mkfile(self, filename):
        if self.current_partition:
            new_file = File(filename)
            self.current_partition.current_directory.add(new_file)
            print(f"File {filename} created.")
        else:
            print("No partition selected.")

    def rm(self, filename):
        if self.current_partition:
            success = self.current_partition.current_directory.delete(filename)
            if success:
                print(f"File {filename} deleted.")
            else:
                print(f"File {filename} does not exist.")
        else:
            print("No partition selected.")

    def rmdir(self, dirname):
        if self.current_partition:
            directory = self.current_partition.current_directory.get(dirname)
            if isinstance(directory, Directory) and not directory.contents:
                success = self.current_partition.current_directory.delete(dirname)
                if success:
                    print(f"Directory {dirname} deleted.")
                else:
                    print(f"Directory {dirname} does not exist.")
            elif isinstance(directory, Directory):
                print(f"Directory {dirname} is not empty.")
            else:
                print(f"{dirname} is not a directory.")
        else:
            print("No partition selected.")

    def ls(self):
        if self.current_partition:
            contents = self.current_partition.current_directory.list_contents()
            print(" ".join(contents))
        else:
            print("No partition selected.")

    def cd(self, dirname):
        if self.current_partition:
            if dirname == "..":
                if self.current_partition.current_directory.parent is not None:
                    self.current_partition.current_directory = self.current_partition.current_directory.parent
                    print("Changed to parent directory.")
                else:
                    print("Already at the root directory.")
            else:
                new_dir = self.current_partition.current_directory.get(dirname)
                if isinstance(new_dir, Directory):
                    self.current_partition.current_directory = new_dir
                    print(f"Changed directory to {dirname}.")
                else:
                    print(f"{dirname} is not a directory.")
        else:
            print("No partition selected.")

    def pwd(self):
        if self.current_partition:
            path = self.current_partition.current_directory.get_path()
            print(path)
        else:
            print("No partition selected.")

    def get_prompt(self):
        if self.current_partition:
            path = self.current_partition.current_directory.get_path()
            return f"{path}$ "
        else:
            return "$ "

    def process_command(self, command):
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd == "mkpart":
            self.mkpart(args[0])
        elif cmd == "rmpart":
            self.rmpart(args[0])
        elif cmd == "select":
            self.select_partition(args[0])
        elif cmd == "mkdir":
            self.mkdir(args[0])
        elif cmd == "mkfile":
            self.mkfile(args[0])
        elif cmd == "rm":
            self.rm(args[0])
        elif cmd == "rmdir":
            self.rmdir(args[0])
        elif cmd == "ls":
            self.ls()
        elif cmd == "cd":
            self.cd(args[0])
        elif cmd == "pwd":
            self.pwd()
        elif cmd == "exit":
            print("Exiting file system simulation.")
            return False
        else:
            print(f"Unknown command: {cmd}")
        return True

def main():
    fs = FileSystem()
    while True:
        command = input(fs.get_prompt())
        if not fs.process_command(command):
            break

if __name__ == "__main__":
    main()

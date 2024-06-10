class Partition:
    def __init__(self, name):
        # Konstruktor untuk kelas Partition. Menginisialisasi nama partisi dan menetapkan root direktori sebagai direktori saat ini.
        self.name = name  # Mengatur nama partisi.
        self.root = Directory("/", None)  # Membuat objek Directory baru sebagai root direktori dengan nama '/' dan tanpa parent.
        self.current_directory = self.root  # Mengatur direktori saat ini ke root.

class Directory:
    def __init__(self, name, parent):
        # Konstruktor untuk kelas Directory. Menginisialisasi nama direktori, parent direktori, dan konten direktori.
        self.name = name  # Mengatur nama direktori.
        self.parent = parent  # Mengatur parent direktori.
        self.contents = {}  # Menginisialisasi konten direktori sebagai dictionary kosong.

    def add(self, item):
        # Menambahkan item (berkas atau direktori) ke dalam direktori.
        self.contents[item.name] = item  # Menambahkan item ke dictionary contents dengan nama item sebagai kunci.

    def get(self, name):
        # Mengambil item dari direktori berdasarkan nama.
        return self.contents.get(name)  # Mengembalikan item berdasarkan nama jika ada, jika tidak mengembalikan None.

    def list_contents(self):
        # Mengembalikan daftar nama semua item dalam direktori.
        return self.contents.keys()  # Mengembalikan kunci dari dictionary contents.

    def delete(self, name):
        # Menghapus item dari direktori berdasarkan nama.
        if name in self.contents:  # Memeriksa apakah item dengan nama yang diberikan ada di dalam direktori.
            del self.contents[name]  # Menghapus item dari dictionary contents.
            return True  # Mengembalikan True jika penghapusan berhasil.
        return False  # Mengembalikan False jika item tidak ditemukan.

    def get_path(self):
        # Mengembalikan jalur lengkap dari direktori ke root.
        path = []  # Membuat list kosong untuk menyimpan jalur.
        current = self  # Menginisialisasi variabel current dengan objek saat ini.
        while current is not None:  # Melakukan loop sampai mencapai root.
            path.append(current.name)  # Menambahkan nama direktori saat ini ke dalam jalur.
            current = current.parent  # Pindah ke parent direktori saat ini.
        return "/".join(reversed(path)).replace("//", "/")  # Menggabungkan jalur secara terbalik dan mengembalikan sebagai string.

class File:
    def __init__(self, name):
        # Konstruktor untuk kelas File. Menginisialisasi nama berkas.
        self.name = name  # Mengatur nama berkas.

class FileSystem:
    def __init__(self):
        # Konstruktor untuk kelas FileSystem. Menginisialisasi partisi dan partisi saat ini.
        self.partitions = {}  # Menginisialisasi partisi sebagai dictionary kosong.
        self.current_partition = None  # Menginisialisasi partisi saat ini menjadi None.

    def mkpart(self, name):
        # Membuat partisi baru dengan nama yang diberikan.
        if name in self.partitions:  # Memeriksa apakah partisi dengan nama yang diberikan sudah ada.
            print(f"Partition {name} already exists.")  # Menampilkan pesan jika partisi sudah ada.
        else:
            self.partitions[name] = Partition(name)  # Membuat partisi baru dan menambahkannya ke dalam dictionary partitions.
            self.current_partition = self.partitions[name]  # Mengatur partisi saat ini ke partisi yang baru dibuat.
            print(f"Partition {name} created and selected.")  # Menampilkan pesan bahwa partisi baru telah dibuat dan dipilih.

    def rmpart(self, name):
        # Menghapus partisi dengan nama yang diberikan.
        if name in self.partitions:  # Memeriksa apakah partisi dengan nama yang diberikan ada.
            del self.partitions[name]  # Menghapus partisi dari dictionary partitions.
            if self.current_partition and self.current_partition.name == name:  # Memeriksa apakah partisi yang dihapus adalah partisi saat ini.
                self.current_partition = None  # Mengatur partisi saat ini menjadi None jika partisi yang dihapus adalah partisi saat ini.
            print(f"Partition {name} deleted.")  # Menampilkan pesan bahwa partisi telah dihapus.
        else:
            print(f"Partition {name} does not exist.")  # Menampilkan pesan jika partisi tidak ditemukan.

    def select_partition(self, name):
        # Memilih partisi dengan nama yang diberikan.
        if name in self.partitions:  # Memeriksa apakah partisi dengan nama yang diberikan ada.
            self.current_partition = self.partitions[name]  # Mengatur partisi saat ini ke partisi yang dipilih.
            print(f"Partition {name} selected.")  # Menampilkan pesan bahwa partisi telah dipilih.
        else:
            print(f"Partition {name} does not exist.")  # Menampilkan pesan jika partisi tidak ditemukan.

    def mkdir(self, dirname):
        # Membuat direktori baru dengan nama yang diberikan.
        if self.current_partition:  # Memeriksa apakah ada partisi yang dipilih.
            new_dir = Directory(dirname, self.current_partition.current_directory)  # Membuat objek Directory baru dengan nama yang diberikan.
            self.current_partition.current_directory.add(new_dir)  # Menambahkan direktori baru ke direktori saat ini.
            print(f"Directory {dirname} created.")  # Menampilkan pesan bahwa direktori telah dibuat.
        else:
            print("No partition selected.")  # Menampilkan pesan jika tidak ada partisi yang dipilih.

    def mkfile(self, filename):
        # Membuat berkas baru dengan nama yang diberikan.
        if self.current_partition:  # Memeriksa apakah ada partisi yang dipilih.
            new_file = File(filename)  # Membuat objek File baru dengan nama yang diberikan.
            self.current_partition.current_directory.add(new_file)  # Menambahkan berkas baru ke direktori saat ini.
            print(f"File {filename} created.")  # Menampilkan pesan bahwa berkas telah dibuat.
        else:
            print("No partition selected.")  # Menampilkan pesan jika tidak ada partisi yang dipilih.

    def rm(self, filename):
        # Menghapus berkas dengan nama yang diberikan.
        if self.current_partition:  # Memeriksa apakah ada partisi yang dipilih.
            success = self.current_partition.current_directory.delete(filename)  # Menghapus berkas dari direktori saat ini.
            if success:
                print(f"File {filename} deleted.")  # Menampilkan pesan jika berkas berhasil dihapus.
            else:
                print(f"File {filename} does not exist.")  # Menampilkan pesan jika berkas tidak ditemukan.
        else:
            print("No partition selected.")  # Menampilkan pesan jika tidak ada partisi yang dipilih.

    def rmdir(self, dirname):
        # Menghapus direktori dengan nama yang diberikan.
        if self.current_partition:  # Memeriksa apakah ada partisi yang dipilih.
            directory = self.current_partition.current_directory.get(dirname)  # Mengambil direktori dari direktori saat ini.
            if isinstance(directory, Directory) and not directory.contents:  # Memeriksa apakah objek adalah direktori dan kosong.
                success = self.current_partition.current_directory.delete(dirname)  # Menghapus direktori dari direktori saat ini.
                if success:
                    print(f"Directory {dirname} deleted.")  # Menampilkan pesan jika direktori berhasil dihapus.
                else:
                    print(f"Directory {dirname} does not exist.")  # Menampilkan pesan jika direktori tidak ditemukan.
            elif isinstance(directory, Directory):
                print(f"Directory {dirname} is not empty.")  # Menampilkan pesan jika direktori tidak kosong.
            else:
                print(f"{dirname} is not a directory.")  # Menampilkan pesan jika objek bukan direktori.
        else:
            print("No partition selected.")  # Menampilkan pesan jika tidak ada partisi yang dipilih.

    def ls(self):
        # Menampilkan daftar isi direktori saat ini.
        if self.current_partition:  # Memeriksa apakah ada partisi yang dipilih.
            contents = self.current_partition.current_directory.list_contents()  # Mengambil daftar isi dari direktori saat ini.
            print(" ".join(contents))  # Menampilkan daftar isi sebagai string yang dipisahkan oleh spasi.
        else:
            print("No partition selected.")  # Menampilkan pesan jika tidak ada partisi yang dipilih.

    def cd(self, dirname):
        # Mengubah direktori saat ini ke direktori yang diberikan.
        if self.current_partition:  # Memeriksa apakah ada partisi yang dipilih.
            if dirname == "..":  # Memeriksa jika perintah adalah untuk kembali ke parent direktori.
                if self.current_partition.current_directory.parent is not None:  # Memeriksa apakah direktori saat ini memiliki parent.
                    self.current_partition.current_directory = self.current_partition.current_directory.parent  # Mengubah direktori saat ini ke parent.
                    print("Changed to parent directory.")  # Menampilkan pesan bahwa telah berubah ke parent direktori.
                else:
                    print("Already at the root directory.")  # Menampilkan pesan jika sudah berada di root direktori.
            else:
                new_dir = self.current_partition.current_directory.get(dirname)  # Mengambil direktori baru dari direktori saat ini.
                if isinstance(new_dir, Directory):  # Memeriksa apakah objek adalah direktori.
                    self.current_partition.current_directory = new_dir  # Mengubah direktori saat ini ke direktori baru.
                    print(f"Changed directory to {dirname}.")  # Menampilkan pesan bahwa direktori telah berubah.
                else:
                    print(f"{dirname} is not a directory.")  # Menampilkan pesan jika objek bukan direktori.
        else:
            print("No partition selected.")  # Menampilkan pesan jika tidak ada partisi yang dipilih.

    def pwd(self):
        # Menampilkan jalur direktori saat ini.
        if self.current_partition:  # Memeriksa apakah ada partisi yang dipilih.
            path = self.current_partition.current_directory.get_path()  # Mengambil jalur dari direktori saat ini.
            print(path)  # Menampilkan jalur direktori saat ini.
        else:
            print("No partition selected.")  # Menampilkan pesan jika tidak ada partisi yang dipilih.

    def get_prompt(self):
        # Mengembalikan prompt untuk input pengguna berdasarkan direktori saat ini.
        if self.current_partition:  # Memeriksa apakah ada partisi yang dipilih.
            path = self.current_partition.current_directory.get_path()  # Mengambil jalur dari direktori saat ini.
            return f"{path}$ "  # Mengembalikan prompt dengan jalur direktori saat ini.
        else:
            return "$ "  # Mengembalikan prompt default jika tidak ada partisi yang dipilih.

    def process_command(self, command):
        # Memproses perintah yang diberikan oleh pengguna.
        parts = command.split()  # Memisahkan perintah menjadi bagian-bagian.
        cmd = parts[0]  # Mengambil perintah utama.
        args = parts[1:]  # Mengambil argumen perintah.

        if cmd == "mkpart":
            self.mkpart(args[0])  # Membuat partisi baru.
        elif cmd == "rmpart":
            self.rmpart(args[0])  # Menghapus partisi.
        elif cmd == "select":
            self.select_partition(args[0])  # Memilih partisi.
        elif cmd == "mkdir":
            self.mkdir(args[0])  # Membuat direktori baru.
        elif cmd == "mkfile":
            self.mkfile(args[0])  # Membuat berkas baru.
        elif cmd == "rm":
            self.rm(args[0])  # Menghapus berkas.
        elif cmd == "rmdir":
            self.rmdir(args[0])  # Menghapus direktori.
        elif cmd == "ls":
            self.ls()  # Menampilkan isi direktori.
        elif cmd == "cd":
            self.cd(args[0])  # Mengubah direktori.
        elif cmd == "pwd":
            self.pwd()  # Menampilkan jalur direktori saat ini.
        elif cmd == "exit":
            print("Exiting file system simulation.")  # Menampilkan pesan keluar.
            return False  # Menghentikan loop utama.
        else:
            print(f"Unknown command: {cmd}")  # Menampilkan pesan jika perintah tidak dikenal.
        return True  # Mengembalikan True untuk melanjutkan loop utama.

def main():
    # Fungsi utama program.
    fs = FileSystem()  # Membuat objek FileSystem baru.
    while True:  # Loop utama program.
        command = input(fs.get_prompt())  # Menerima input perintah dari pengguna.
        if not fs.process_command(command):  # Memproses perintah yang diberikan pengguna.
            break  # Menghentikan loop jika pengguna memasukkan perintah "exit".

if __name__ == "__main__":
    main()  # Memanggil fungsi utama jika skrip ini dijalankan secara langsung.

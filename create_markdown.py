import os


def generate_markdown():
    os_walk = os.walk(os.path.abspath("./images"))
    for root, dirs, files in os_walk:
        if dirs:
            with open('README.md', 'w+') as f:
                f.write("## This is a repo for backup Risa Yoshiki\n")
                f.write("### Photo Book List\n")
                for root_dir in dirs:
                    print("{}/{}".format(root, root_dir))
                    ndir = root_dir.replace('[', '').replace(']', '').replace('&amp;', '')
                    f.write(f"- [{ndir}]({'./images/' + ndir + '.md'})\n")
                    with open(os.path.join('./images/' + ndir + '.md'), 'w+') as ff:
                        dir_walk = os.walk(os.path.join(root, root_dir))
                        for droot, ddirs, dfiles in dir_walk:
                            for img_file in dfiles:
                                print(os.path.join(root, droot, img_file))
                                ff.write(f"![{img_file}]({'./' + root_dir + os.sep + img_file})\n")
                            print("--------------------------------")


def rename_image_folder():
    os_walk = os.walk(os.path.abspath("./images"))
    for root, dirs, files in os_walk:
        if dirs:
            for root_dir in dirs:
                new_dir = root_dir.replace('[', '').replace(']', '').replace('&amp;', '')
                os.rename(os.path.join(root, root_dir), os.path.join(root, new_dir))
                print(f"folder: {os.path.join(root, root_dir)} rename to {os.path.join(root, new_dir)}")


def main():
    generate_markdown()
    rename_image_folder()


if __name__ == '__main__':
    main()

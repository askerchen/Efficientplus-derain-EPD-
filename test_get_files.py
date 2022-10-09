import os

# rain100H/L / SPA
def get_files(path):
    ret = []
    path_rainy = path + "/rain"
    path_gt = path + "/norain"
    for root, dirs, files in os.walk(path_rainy):
        files.sort()

        for name in files:
            if name.split('.')[1] != 'png':
                continue
            print(name)
            file_rainy = path_rainy + "/" + name  # name = "rain-xxx.png"
            file_gt = path_gt + "/" + "no" + name
            print("file_rainy : {}".format(file_rainy))
            print("file_gt : {}".format(file_gt))
            ret.append([file_rainy, file_gt])
    # print("ret = {}".format(ret))
    return ret

print(get_files("./datasets/rain100H/test"))
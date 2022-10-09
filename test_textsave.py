def text_save(content, filename, mode = 'a'):
    # save a list to a txt
    # Try to save a list variable in txt file.
    file = open(filename, mode)
    for i in range(len(content)):
        file.write(str(content[i]))
    file.close()

for i in range(1, 10):
    text_save("{}\n".format(i), "./test_results/v4sp/test_textsave.txt") # 不能直接创建，因为前一级的目录文件也不存在;

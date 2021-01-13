from urllib import request

url = "https://mirror.azure.cn/docker-ce/linux/centos/7/x86_64/stable/repodata/"


def get_html(url, filepath):
    html = request.urlopen(url).read()
    fout = open(filepath, "wb")
    fout.write(html)
    fout.close()


'''
从包含“filelists.xml.gz”的HTML行解析完整文件名和更新日期，它们将被传入键值对
前提是必须包含子串“filelists.xml.gz”，否则解析失败
目前的实现尚不优雅，格式变了就玩完了
'''


def parse_filelists_xml_gz(line):
    filename = line[9:90]
    offset = line.find("</a>")
    timeStr = line[offset+5:offset+22]
    return filename, timeStr


def get_all_filelists_xml_gz(filepath):
    target_lines = {}
    fin = open(filepath)
    for line in fin.readlines():
        line = line.strip("\n")
        if "filelists.xml.gz" in line:
            filename, timeStr = parse_filelists_xml_gz(line)
            target_lines[filename] = timeStr
    print(f"{filename}\t{timeStr}")
    return target_lines


get_html(url, "test.html")
get_all_filelists_xml_gz("test.html")

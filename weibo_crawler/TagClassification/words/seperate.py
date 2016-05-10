#!/usr/bin/python
# -*-coding:utf-8-*-


def filter_tag(tagmap, tag):
    """ @param: tagmap 一个字典, 键是tag, 值是类别.
    @param: tag需要分类的标签词.
    @return: 词属于的类别.
    """

    if tag in tagmap:
        return tagmap[tag]
    else:
        return "-1"


def main():
    f = "../data/classes.txt"

    fd = open(f, "rb")

    tagmap = {}
    for line in fd.xreadlines():
        tag, c = line.split(" ")
        tagmap[tag] = c.strip()

    print "Has %s tags." % len(tagmap.keys())
    fd.close()

    tags = "../data/tg.txt"
    ft = open(tags, "rb")
    seperate = {}
    lineno = 0
    for tag in ft.xreadlines():
        lineno += 1
        tag = tag.strip()
        print "Read %s lines." % lineno
        cl = filter_tag(tagmap, tag)
        print "%s belong to class %s." % (tag, cl)
        seperate[cl].append(tag) if seperate.has_key(cl) else seperate.update({cl: [tag]})

    ft.close()

    for cl, tags in seperate.iteritems():
        print cl, tags
        with open("class" + str(cl), "wb") as fd:
            for tag in tags:
                fd.write(tag + "\n")


if __name__ == "__main__":
    main()




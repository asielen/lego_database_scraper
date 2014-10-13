# This isn't part of the project, but rather a side project to count lines of code.
#
# Database
# objects:
# name TEXT
# path TEXT
#     type TEXT (file)
#     parent ID
#     line_count INT
#     comment_count INT
#     code_count INT
#
#
# imports
#   object id
#   method id
#
import sqlite3 as lite
import os
import sys

analytics_db = os.path.abspath('project_eval.sqlite')

exts = ['.py']  #, '.ini', '.c', '.h']
count_empty_line = True
here = os.path.abspath(os.path.dirname(sys.argv[0]))

#
#
#
#
# if __name__ == '__main__':
#     line_count = 0
#     file_count = 0
#     files = []
#     for base, dirs, files in os.walk(here):
#         for file in files:
#             # Check the sub directories
#             if file.find('.') < 0:
#                 continue
#             ext = (file[file.rindex('.'):]).lower()
#             try:
#                 if exts.index(ext) >= 0:
#                     file_count += 1
#                     path = (base + '/'+ file)
#                     if file == '__init__.py':
#                         print("Found Module {}".format(base.split('/')[-1]))
#                     cfile = read_file(file, path)
#
#                     print(".%s : %d" % (path[len(here):], cfile))
#                     line_count += cfile
#             except:
#                 pass
#     print('File count : %d' % file_count)
#     print('Line count : %d' % line_count)

def main():
    line_count = 0
    code_count = 0
    comment_count = 0
    white_count = 0
    file_count = 0
    current_count = ()
    for base, dirs, files in os.walk(here):
        for file in files:
            # Check the sub directories
            if file.find('.') < 0:
                continue
            ext = (file[file.rindex('.'):]).lower()
            try:
                if exts.index(ext) >= 0:
                    file_count += 1
                    path = (base + '/' + file)
                    current_count = get_file_details(file, path)
                    line_count += current_count[0]
                    code_count += current_count[1]
                    comment_count += current_count[2]
                    white_count += current_count[3]
                    print(".%s : %d" % (path[len(here):], comment_count[0]))
            except:
                pass
    print('File count : %d' % file_count)
    print('Line count : %d' % line_count)
    print('Code count : %d' % code_count)
    print('Comment count : %d' % comment_count)
    print('White count : %d' % white_count)

    print('Line Count Check {}'.format(code_count + comment_count + white_count))
    print('{}% Code | {}% Comments | {}% White Space'.format(round((code_count / line_count) * 100),
                                                             round((comment_count / line_count) * 100),
                                                             round((white_count / line_count) * 100)))


def parse_file(path, file_name):
    c_line = ""
    line_count = 0
    code_count = 0
    comment_count = 0
    white_count = 0
    for line in open(path).readlines():
        c_line = line.strip()
        line_count += 1
        if len(c_line) > 0:
            if c_line[0] == "#":
                comment_count += 1
            else:
                code_count += 1
                parse_line(c_line, path, file_name)
        else:
            white_count += 1
    return line_count, code_count, comment_count, white_count


def parse_line(line, path, file):
    imports = []
    methods = []
    classes = []
    used = []
    # print("Line Length {}".format(len(line)))
    # print(line)
    if line[0:6] == "import":
        print("IMPORT")
        print(line[6:].split(' as '))
    if line[0:4] == "from":
        print("FROM")
        print(line[4:].split(' import '))


    # This finds all methods/functions starting with a white space and ending with a (
    # Not needed but keeping because it regex are not fun to write
    # print([re.findall(r'[a-zA-Z0-9_\.]+', r) for r in re.findall(r'[^a-zA-Z0-9_\.][a-zA-Z0-9_\.]+\(', line)])

    return


def get_file_details(file_name, path):
    """
    Take an object and returns the details about that object
    @param object:
    @return:
    """
    if file_name == 'analytics.py': return
    create_db_ob(name=file_name, path=path)
    check_module(file_name)
    return parse_file(path, file_name)


def check_module(name=""):
    if name == '__init__.py':
        return True
    return False


def create_db_ob(name="", path=None):
    """
    Create a new entry in the db
    @param name:
    @param path:
    @param type:
    @param parent:
    @param line_count:
    @param code_count:
    @param comment_count:
    @param white_count:
    @return:
    """


def create_import(import_obj, parent_obj):
    """

    @return:
    """
    import_id = lookup_id(import_obj[0], import_obj[1])
    parent_id = lookup_id(parent_obj[0], parent_obj[1])


def lookup_id(name, path):
    """

    @param name:
    @param path:
    @return:
    """


def create_db():
    con = lite.connect(analytics_db)
    with con:
        # Empty the database if it was run before
        con.execute("PRAGMA writable_schema = 1;")
        con.execute("DELETE FROM sqlite_master WHERE type = 'table';")
        con.execute("PRAGMA writable_schema = 0;")
        con.execute("VACUUM;")
        con.execute("PRAGMA INTEGRITY_CHECK;")

        con.execute("CREATE TABLE IF NOT EXISTS objects(id INTEGER PRIMARY KEY,"
                    "name TEXT, "
                    "path TEXT, "
                    "type TEXT, "
                    "parent_id INTEGER, "
                    "line_count INTEGER, "
                    "code_count INTEGER, "
                    "comment_count INTEGER, "
                    "white_count INTEGER);")

        con.execute("CREATE TABLE IF NOT EXISTS imports(id INTEGER PRIMARY KEY,"
                    "object_id INTEGER, "
                    "imported_id INTEGER);")

        con.execute("CREATE TABLE IF NOT EXISTS modules(id INTEGER PRIMARY KEY,"
                    "module_id INTEGER, "
                    "file_id INTEGER);")


if __name__ == '__main__':
    create_db()
    main()

    # Created by Liang Sun <i@liangsun.org> in 2012
    # This code is for Python 2.x
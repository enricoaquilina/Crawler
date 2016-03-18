import os

#each website you crawl is a separate project
def create_project_directory(directory):
    if not os.path.exists(directory):
        print('Creating project ' + directory)
        os.makedirs(directory)

#create queue and crawled files if they dont exist
def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')

#create a new file
def write_file(file_name, contents):
    #this is in write mode
    f = open(file_name, 'w')
    f.write(contents)
    #free up memory, avoid data leaks
    f.close()

#add datta on to an existing file
def append_to_file(file_name, contents):
    with open(file_name, 'a') as file:
        file.write(contents + '\n')

#delete the contents of a file
def delete_file_contents(file_name):
    with open(file_name, 'w'):
        #this is the same as doin nothing
        pass

#we re gonna use sets since they allow uniqueness which is KEY to my precious!

#read a file and convert eac line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

#convert a set into a file
def set_to_file(linkSet, file):
    delete_file_contents(file)
    for line in sorted(linkSet):
        append_to_file(file, line)
    return file


import sys, os
import pickle

DEBUG_MODE = True

def print_usage():
    print >> sys.stderr, "Usage: %s <path1> <path2> [...]" % (sys.argv[0])

def debug(msg):
    """
    output the debug message under debug mode
    """
    global DEBUG_MODE
    if DEBUG_MODE:
        print >> sys.stderr, msg


def mergeCache(data_list):
    """
    merges all the given cached data in data_list into 1 merged data and return
    """
    ret = {'blogs': {}, 'posts': {}} # the ultimate merged data
    debug_counter = 0
    for data in data_list:
        ret['blogs'].update(data['blogs'])
        ret['posts'].update(data['posts'])
        debug("already merged %d" % (debug_counter+1))
        debug_counter += 1
    return ret

if __name__ == "__main__":
    
    # check argument count (at least 2 input paths and exactly 1 output path)
    if len(sys.argv) < 4:
        print >> sys.stderr, "wrong arguments!"
        print_usage()
        sys.exit(-1)

    # check arguments
    paths = sys.argv[1:-1] # discard the 1st and the last argument
    for p in paths:
        if not os.path.isfile(p):
            print >> sys.stderr, "%s is not a file" % (p)
            print_usage()
            sys.exit(-1)

    outputPath = sys.argv[-1]
    if os.path.exists(outputPath):
        print >> sys.stderr, "the given output path: %s already exists" % (outputPath)
        print_usage()
        sys.exit(-1)

    # load the data
    debug("start loading the pickle data...")
    data_list = []
    for p in paths:
        try:
            debug("loading data from %s" % (p))
            data_list.append( pickle.load(open(p, "r")) )
        except:
            print >> sys.stderr, "error occurred when loading pickle data at: %s" % (p)
            sys.exit(-1)

    # merge them
    debug("start merging all the loaded data...")
    merged_data = mergeCache(data_list)
    
    # output the merged data
    debug("start dumping merged data as pickled...")
    pickle.dump(merged_data, open(outputPath, "w"))

    debug("finish.")




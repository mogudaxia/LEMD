from lemd_prototype.extensions import mongo


def feed_content():
    """List all content of the Mongo Database"""
#    res = ''
#    for q in mongo.db.fs.files.find():
#        res += str(q)
    return ''.join([str(q) for q in mongo.db.fs.files.find()])


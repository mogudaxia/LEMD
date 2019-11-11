from lemd_prototype.extensions import mongo


def feed_content():
    """List all content of the Mongo Database"""

    return mongo.fs.files.find()

from lemd_prototype.extensions import mongo
import gridfs


def feed_content():
    """List all content of the Mongo Database"""
#    res = ''
#    for q in mongo.db.fs.files.find():
#        res += str(q)
    return ''.join([str(q['_id']) for q in mongo.db.fs.files.find()])


class DpField:
    _system = ''
    _dist_to_ref = 0
    _ids = ''
    _version = ''
    _file_idx = ''

    def __init__(self, mat_sys :str, vers: str):
        self._system = mat_sys
        self._version = vers
        db_ids = self._system + '_' + self._version
        try:
            self._ids = mongo.db.fs.files.find_one({"name": db_ids})
        except len(self._ids) == 0:
            raise ValueError("Given system not found in database")

    def get_dist(self):
        return self._ids["dist"]

    def get_fileid(self):
        return self._ids["_id"]

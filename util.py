import uuid


def short_uid():
    return str(uuid.uuid4().hex[:8])

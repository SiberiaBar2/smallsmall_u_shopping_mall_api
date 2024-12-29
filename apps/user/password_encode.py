import hashlib

def get_md5(param):
    # 必须处理 若为空 哈希会使用之前的值
    if not param:
        return ''
    md5 = hashlib.md5()
    md5.update(param.encode('utf-8'))

    return md5.hexdigest()
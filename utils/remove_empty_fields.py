def remove_empty_fields(obj):
    """
    遍历字典，删除其中值为空的字段。
    :param obj: 输入字典
    :return: 去除空字段后的字典
    """
    # 遍历字典的副本，因为在字典遍历时直接删除会引发异常
    for key in list(obj.keys()):
        # 判断值是否为空
        if not obj[key]:
            del obj[key]

    return obj


# 示例用法
data = {
    'name': 'John',
    'age': None,
    'email': '',
    'address': {},
    'phone': '1234567890',
    'is_active': True
}

# 移除空字段
cleaned_data = remove_empty_fields(data)

print('cleaned_data',cleaned_data)
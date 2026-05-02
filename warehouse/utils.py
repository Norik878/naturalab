def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Администратор').exists()

def is_worker(user):
    return user.groups.filter(name='Сотрудник').exists() or is_admin(user)
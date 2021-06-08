from django.db import models


class XmlUpdate(models.Model):
    need_update = models.BooleanField('Требуется обновление файла XML')

    def __str__(self):
        need_update_str = "Нет"
        if self.need_update:
            need_update_str = "Да"
        return 'Требуется обновление XML файла: ' + need_update_str

    class Meta:
        verbose_name = 'Обновление схем'
        verbose_name_plural = '1. Обновление схем'


class Messenger(models.Model):
    name = models.CharField('Имя мессенджера', max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мессенджер'
        verbose_name_plural = 'Мессенджеры'


class Config(models.Model):
    messenger = models.ForeignKey('Messenger', on_delete=models.CASCADE)
    token = models.CharField('Токен', max_length=100)
    is_on = models.BooleanField('Бот включен')

    def __str__(self):
        is_on_str = "Выключен"
        if self.is_on:
            is_on_str = "Включен"
        return "(" + is_on_str + ") " + self.messenger.name + ": " + self.token

    class Meta:
        verbose_name = 'Конфигурация'
        verbose_name_plural = '2. Конфигурации'


class User(models.Model):
    messenger = models.ForeignKey('Messenger', on_delete=models.CASCADE)
    user_id = models.CharField('ID пользователя', max_length=100)
    element = models.ForeignKey('Element', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '(' + self.messenger.name + ') ' + self.user_id + ": " + self.element.text

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = '3. Пользователи'


class Scheme(models.Model):
    name = models.CharField('Имя схемы', max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Схема'
        verbose_name_plural = '4. Схемы'


class Element(models.Model):
    scheme = models.ForeignKey('Scheme', on_delete=models.CASCADE)
    name = models.CharField('Имя элемента', max_length=100, unique=True)
    text = models.TextField('Текст элемента')

    def __str__(self):
        return self.scheme.name + ': ' + ' (' + self.name + ') ' + self.text

    class Meta:
        verbose_name = 'Элемент'
        verbose_name_plural = '5. Элементы'


class ElementAddition(models.Model):
    element = models.ForeignKey('Element', on_delete=models.CASCADE, related_name='addition_from')
    addition = models.ForeignKey('Element', on_delete=models.CASCADE, related_name='addition_to')
    text = models.CharField('Текст дополнения', max_length=100)

    def __str__(self):
        return self.element.name + ' (' + self.element.scheme.name + ') ' + ' <--- ' + self.addition.name + ' (' + self.addition.scheme.name + ') , ' + self.text

    class Meta:
        verbose_name = 'Дополнение'
        verbose_name_plural = '6. Дополнения'


class ElementTransition(models.Model):
    element = models.ForeignKey('Element', on_delete=models.CASCADE, related_name='transition_from')
    transition = models.ForeignKey('Element', on_delete=models.CASCADE, related_name='transition_to')
    text = models.CharField('Текст перехода', max_length=100)

    def __str__(self):
        return self.element.name + ' (' + self.element.scheme.name + ') ' + ' ---> ' + self.transition.name + ' (' + self.transition.scheme.name + ') , ' + self.text

    class Meta:
        verbose_name = 'Переход'
        verbose_name_plural = '7. Переходы'

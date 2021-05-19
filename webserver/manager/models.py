from django.db import models


class Messenger(models.Model):
    name = models.CharField('Имя мессенджера', max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мессенджер'
        verbose_name_plural = '1_Мессенджеры'


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
        verbose_name_plural = '2_Конфигурации'


class User(models.Model):
    messenger = models.ForeignKey('Messenger', on_delete=models.CASCADE)
    user_id = models.CharField('ID пользователя', max_length=100)
    element = models.ForeignKey('Element', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user_id + " : " + self.element.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = '3_Пользователи'


class Scheme(models.Model):
    name = models.CharField('Имя ветки', max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Схема'
        verbose_name_plural = '4_Схемы'


class Element(models.Model):
    scheme = models.ForeignKey('Scheme', on_delete=models.CASCADE)
    name = models.CharField('Имя элемента', max_length=100, unique=True)
    text = models.TextField('Текст элемента')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Элемент'
        verbose_name_plural = '5_Элементы'


class ElementAddition(models.Model):
    element = models.ForeignKey('Element', on_delete=models.CASCADE, related_name='addition_from')
    addition = models.ForeignKey('Element', on_delete=models.CASCADE, related_name='addition_to')
    text = models.CharField('Текст дополнения', max_length=100)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Дополнение'
        verbose_name_plural = '6_Дополнения'


class ElementTransition(models.Model):
    element = models.ForeignKey('Element', on_delete=models.CASCADE, related_name='transition_from')
    transition = models.ForeignKey('Element', on_delete=models.CASCADE, related_name='transition_to')
    text = models.CharField('Текст перехода', max_length=100)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Переход'
        verbose_name_plural = '7_Переходы'

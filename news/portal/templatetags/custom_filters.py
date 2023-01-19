from django import template

register = template.Library()

allword = {""}


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
    """
   value: значение, к которому нужно применить фильтр
   """
    badwords = ["modern", "try","society"]
    splitwords = value.split()

    for i in range(len(splitwords)):
        if splitwords[i] in badwords:
            firstletter = splitwords[i][0]
            newvalue=firstletter +"*"*(len(splitwords[i])-1)
            splitwords[i] = newvalue
    result = " ".join(splitwords)
    return f'{result} '

    # Возвращаемое функцией значение подставится в шаблон.

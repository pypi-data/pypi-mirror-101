from typing import Union


def cpf_int_validation(cpf: int) -> bool:
    """
    Validation CPF integer.

    Args:
        cpf (int): CPF.

    Returns:
        bool: If CPF real True else False.
    """
    clean_cpf = str(cpf).zfill(11)
    digito = {}
    digito[0] = 0
    digito[1] = 0
    a = 10
    total = 0
    for c in range(0, 2):
        for i in range(0, (9+c)):
            total = total+int(clean_cpf[i])*a
            a -= 1
        digito[f'total_{c}'] = total
        total_value = total % 11
        digito[c] = (int(11-(total_value))
                     if total_value > 0 else total_value)
        if digito[c] >= 10:
            digito[c] = int(str(digito[c])[-1])
        a = 11
        total = 0
    if ((int(clean_cpf[9]) == int(digito[0])) and (int(clean_cpf[10]) == int(digito[1]))):
        return True
    else:
        return False


def cpf_str_validation(cpf: str) -> bool:
    """
    Validation CPF string

    Args:
        cpf (str): CPF.

    Returns:
        bool: If CPF real True else False.
    """
    clean_cpf = cpf.replace('.', '').replace('-', '')

    try:
        return cpf_int_validation(cpf=int(clean_cpf))
    except ValueError:
        print('ERROR: CPF entered is not a number, please review.')
        return False


def cpf_format(cpf: Union[int, str, float]) -> str:
    """
    Format CPF.

    Args:
        cpf (Union[int, str, float]): CPF

    Returns:
        str: Formated CPF "***.***.***-**"
    """
    try:
        if type(cpf) == float:
            cpf = int(cpf)
        cpf_cleaned = int(''.join(filter(str.isdigit, str(cpf))))
        cpf_cleaned = str(cpf_cleaned).zfill(11)
        return (f'{cpf_cleaned[:3]}.{cpf_cleaned[3:6]}.{cpf_cleaned[6:9]}-{cpf_cleaned[9:]}')
    except ValueError:
        return ''

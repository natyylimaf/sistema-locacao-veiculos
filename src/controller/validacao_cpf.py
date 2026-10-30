import re


def normalizar_cpf(cpf: str) -> str:
    """Remove pontos, hífens, espaços e qualquer caractere que não seja dígito."""
    return re.sub(r"\D", "", cpf)


def validar_cpf(cpf: str) -> bool:
    """Verifica o formato e os dígitos verificadores do CPF brasileiro."""
    cpf = normalizar_cpf(cpf)

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    numeros = [int(digito) for digito in cpf]

    soma = sum(numeros[i] * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    primeiro_digito = 0 if resto == 10 else resto

    if numeros[9] != primeiro_digito:
        return False

    soma = sum(numeros[i] * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    segundo_digito = 0 if resto == 10 else resto

    return numeros[10] == segundo_digito

def ler_cpf(mensagem: str = "CPF: ") -> str:
    """Lê o CPF digitado (válido ou não) e devolve só os dígitos."""
    return normalizar_cpf(input(mensagem).strip())

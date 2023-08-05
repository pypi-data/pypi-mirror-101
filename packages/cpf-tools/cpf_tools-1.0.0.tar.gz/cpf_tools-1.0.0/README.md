# cpf_tools

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=flat-square)](https://www.python.org/)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/BrunoASNascimento/cpf_tools.svg?logo=lgtm&logoWidth=18&style=flat-square)](https://lgtm.com/projects/g/BrunoASNascimento/cpf_tools/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/BrunoASNascimento/cpf_tools.svg?logo=lgtm&logoWidth=18&style=flat-square)](https://lgtm.com/projects/g/BrunoASNascimento/cpf_tools/context:python)

Biblioteca com ferramentas para auxiliar na checagem, formatação etc. de CPFs.

## Instalação:

` $ pip install cpf-tools`

## Funções:

- _cpf-tools.**cpf_int_validation**(cpf: int) -> bool_:

Essas função recebe um valor inteiro e verifica se o digito verificador do CPF é verdadeiro (True) ou falso (False).

- _cpf-tools.**cpf_str_validation**(cpf: str) -> bool_:

Essas função recebe um valor string e verifica se o digito verificador do CPF é verdadeiro (True) ou falso (False).

- _cpf-tools.**cpf_format**(cpf: Union[int, str, float]) -> str_:

Essa função recebe um valor integer, string ou float de um CPF e retorna uma string formatada.
(Exemplo: "00000000000" -> "000.000.000-00")

## Usando com Pandas:

Para utilizar com a biblioteca Pandas, utilize o seguinte comando:

`df['your-cpf-field'].apply(cpf-tools.cpf_int_validation)` ou

`df['your-cpf-field'].apply(cpf-tools.cpf_str_validation)` ou

`df['your-cpf-field'].apply(cpf-tools.cpf_format)`

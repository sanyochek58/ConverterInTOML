import argparse
import re
from typing import Dict, Any


def parse_input_file(input_file: str) -> str:
    with open(input_file, 'r') as file:
        return file.read()

def remove_multiline_comments(content: str) -> str:
    return re.sub(r'#\|.*?\|#', '', content, flags=re.DOTALL)

def parse_value(value: str, variables: Dict[str, Any]) -> Any:
    value = value.strip().rstrip(';')
    if re.fullmatch(r'\d+', value):
        return int(value)
    elif value.startswith('@') and value.endswith('"'):
        return value[2:-1]
    elif value.startswith('?(') and value.endswith(')'):
        expr = value[2:-1].strip()
        return evaluate_expression(expr, variables)
    elif value in variables:
        return variables[value]
    else:
        raise SyntaxError(f"Неверное значение: {value}")


def evaluate_expression(expr: str, variables: Dict[str, Any]) -> Any:
    tokens = expr.split()
    stack = []

    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        elif token in variables:
            stack.append(variables[token])
        elif token == '+':
            b = stack.pop()
            a = stack.pop()
            if isinstance(a, dict) and isinstance(b, dict):
                a.update(b)
                stack.append(a)
            elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
                stack.append(a + b)
            else:
                raise SyntaxError(f"Операнды операции '+' должны быть либо числами, либо словарями: {a}, {b}")
        elif token == '-':
            b = stack.pop()
            a = stack.pop()
            if isinstance(a, dict) and isinstance(b, dict):
                # Удаляем ключи b из a
                for key in b:
                    a.pop(key, None)
                stack.append(a)
            elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
                stack.append(a - b)
            else:
                raise SyntaxError(f"Операнды операции '-' должны быть либо числами, либо словарями: {a}, {b}")
        elif token == '*':
            b = stack.pop()
            a = stack.pop()
            stack.append(a * b)
        elif token == '/':
            b = stack.pop()
            a = stack.pop()
            if b == 0:
                raise SyntaxError("Ошибка: деление на ноль")
            stack.append(a // b)
        else:
            raise SyntaxError(f"Неизвестный токен: {token}")

    if len(stack) != 1:
        raise SyntaxError(f"Ошибка в выражении: {expr}")

    return stack[0]



def parse_dict(content: str, variables: Dict[str, Any]) -> Dict[str, Any]:
    pattern = r'(\w+)\s*:\s*([^;]+);'
    items = re.findall(pattern, content)

    if not items:
        raise SyntaxError(f"Ошибка в формате словаря: {content}")
    parsed_dict = {}
    for key, value in items:
        parsed_dict[key.strip()] = parse_value(value.strip(), variables)

    return parsed_dict

def convert_to_toml(content: str, variables: Dict[str, Any]) -> str:
    lines = content.strip().splitlines()
    toml_lines = []
    current_dict = None
    dict_name = None

    for line in lines:
        line = line.rstrip()
        print(f"Обработка строки: {line}")

        if not line:
            toml_lines.append("")
            continue

        if line.startswith('#'):
            continue

        if current_dict is not None:
            if line.endswith('};'):
                current_dict += ' ' + line[:-1]
                parsed_dict = parse_dict(current_dict, variables)
                toml_lines.append(f"[{dict_name}]")
                for key, value in parsed_dict.items():
                    toml_lines.append(f"{key} = {format_toml_value(value)}")
                toml_lines.append("")
                variables[dict_name] = parsed_dict
                current_dict = None
                dict_name = None
            else:
                current_dict += ' ' + line
            continue

        if ':=' in line:
            name, value = map(str.strip, line.split(':='))
            if value.startswith('{') and not value.endswith('};'):
                current_dict = value[1:].strip()
                dict_name = name
            else:
                variables[name] = parse_value(value, variables)
                toml_lines.append(f"{name} = {format_toml_value(variables[name])}")
                toml_lines.append("")

        elif line.startswith('?('):
            expr = line[2:-1].strip()
            if '+' in expr:
                operands = expr.split('+')
                result = {}
                for operand in operands:
                    operand = operand.strip()
                    if operand in variables:
                        if isinstance(variables[operand], dict):
                            result.update(variables[operand])  # Объединяем словари
                        else:
                            raise SyntaxError(f"Операнды операции сложения должны быть словарями: {operand}")
                    else:
                        raise SyntaxError(f"Неизвестная переменная: {operand}")
                result_name = "system_colors"
                toml_lines.append(f"[{result_name}]")
                for key, value in result.items():
                    toml_lines.append(f"{key} = {format_toml_value(value)}")
                toml_lines.append("")
                variables[result_name] = result
            else:
                result = evaluate_expression(expr, variables)
                toml_lines.append(f"# Результат вычисления {expr}: {result}")
            toml_lines.append("")

        else:
            raise SyntaxError(f"Неверная строка: {line}")

    return '\n'.join(toml_lines)



def format_toml_value(value: Any) -> str:
    if isinstance(value, str):
        return f'"{value}"'
    return str(value)


def main():
    parser = argparse.ArgumentParser(description='Конвертация конфигурации из учебного языка в TOML.')
    parser.add_argument('input', help='Путь к входному файлу')
    parser.add_argument('output', help='Путь к выходному файлу')

    args = parser.parse_args()

    try:
        content = parse_input_file(args.input)

        content = remove_multiline_comments(content)

        variables = {}

        toml_content = convert_to_toml(content, variables)

        with open(args.output, 'w') as file:
            file.write(toml_content)

        print(f'Конвертация завершена! Выходной файл: {args.output}')
    except SyntaxError as e:
        print(f"Ошибка синтаксиса: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == '__main__':
    main()

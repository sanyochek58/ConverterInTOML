import unittest
from main import remove_multiline_comments, parse_value, evaluate_expression, parse_dict, convert_to_toml


class TestConfigConverterSimple(unittest.TestCase):
    def test_remove_multiline_comments(self):
        content = """
        #| Этот комментарий
        занимает несколько строк |#
        x := 42;
        """
        expected = "x := 42;"
        self.assertEqual(remove_multiline_comments(content).strip(), expected.strip())

    def test_parse_value(self):
        variables = {"x": 42}
        self.assertEqual(parse_value("42;", variables), 42)  # Число
        self.assertEqual(parse_value("?(x x +);", variables), 84)  # Выражение

    def test_evaluate_expression(self):
        variables = {"x": 5, "y": 3}
        self.assertEqual(evaluate_expression("x y +", variables), 8)
        self.assertEqual(evaluate_expression("x y *", variables), 15)
        self.assertEqual(evaluate_expression("x y -", variables), 2)
        self.assertEqual(evaluate_expression("x y /", variables), 1)

    def test_parse_dict(self):
        variables = {"db_name": "test"}
        content = """
        host : @"localhost";
        port : 5432;
        name : db_name;
        """
        expected = {
            "host": "localhost",
            "port": 5432,
            "name": "test",
        }
        self.assertEqual(parse_dict(content.strip(), variables), expected)


if __name__ == "__main__":
    unittest.main()

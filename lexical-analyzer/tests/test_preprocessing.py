# import unittest
# class TestPreprocessing(unittest.TestCase):
#     def test_texto_simples(self):
#         text = "O gato subiu no telhado para caçar o rato."
#         result = remove_stopwords(text)
#         expect = ['gato', 'subiu', 'telhado', 'caçar', 'rato']
#         self.assertEqual(result, expect)

#     def test_empty_text(self):
#         text = ""
#         result = remove_stopwords(text)
#         expect = []
#         self.assertEqual(result, expect)

#     def test_text_only_stopwords(self):
#         text = "o a de para com em"
#         result = remove_stopwords(text)
#         expect = []
#         self.assertEqual(result, expect)

#     def test_text_com_special_chars(self):
#         text = "Programação é incrível! #Python <3"
#         result = remove_stopwords(text)
#         expect = ['programação', 'incrível', 'python', '3']
#         self.assertEqual(result, expect)

# if __name__ == "__main__":
#     unittest.main()

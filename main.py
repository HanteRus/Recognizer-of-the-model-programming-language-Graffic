from tkinter import *
from tkinter import scrolledtext, messagebox
from lexer import LexicalAnalyzer
from parserr import SyntaxAnalyzer
from semantic import SemanticAnalyzer, generate_symbol_table_and_operations

class CompilerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Анализатор кода")
        master.geometry("800x600")
        self.tab_control = ttk.Notebook(master)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text='Редактор кода')
        self.tab_control.add(self.tab2, text='Результаты анализа')
        self.tab_control.pack(expand=1, fill='both')
        self.create_editor_tab()
        self.create_results_tab()

    def create_editor_tab(self):
        example_label = Label(self.tab1, text="Пример кода:", anchor='w')
        example_label.pack(fill='x', padx=5, pady=(5, 0))
        self.code_editor = scrolledtext.ScrolledText(self.tab1, wrap=WORD, width=80, height=20)
        self.code_editor.pack(padx=5, pady=5, fill='both', expand=True)
        default_code = '''{программа 1}
program
var x, y : integer; 
begin
  x := 5;  { Присваиваем x значение 5 }
  y := 10; { Присваиваем y значение 10 }

  if x < y then [
    write (x);
    write (y);
  ]
  else [
    write (y);
    write (x);
  ]
end.'''
        self.code_editor.insert(INSERT, default_code)
        analyze_btn = Button(self.tab1, text="Анализировать код", command=self.analyze_code)
        analyze_btn.pack(pady=5)

    def create_results_tab(self):
        lex_frame = LabelFrame(self.tab2, text="Лексический анализ")
        lex_frame.pack(fill='both', expand=True, padx=5, pady=5)
        self.lexical_output = scrolledtext.ScrolledText(lex_frame, wrap=WORD, width=80, height=8)
        self.lexical_output.pack(fill='both', expand=True, padx=5, pady=5)
        syntax_frame = LabelFrame(self.tab2, text="Синтаксический анализ")
        syntax_frame.pack(fill='both', expand=True, padx=5, pady=5)
        self.syntax_output = scrolledtext.ScrolledText(syntax_frame, wrap=WORD, width=80, height=4)
        self.syntax_output.pack(fill='both', expand=True, padx=5, pady=5)
        semantic_frame = LabelFrame(self.tab2, text="Семантический анализ")
        semantic_frame.pack(fill='both', expand=True, padx=5, pady=5)
        self.semantic_output = scrolledtext.ScrolledText(semantic_frame, wrap=WORD, width=80, height=4)
        self.semantic_output.pack(fill='both', expand=True, padx=5, pady=5)

    def analyze_code(self):
        self.lexical_output.delete(1.0, END)
        self.syntax_output.delete(1.0, END)
        self.semantic_output.delete(1.0, END)
        code = self.code_editor.get(1.0, END)
        if not code.strip():
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите код для анализа")
            return
        try:
            self.lexical_output.insert(INSERT, "* Лексический анализ *\n")
            lexer = LexicalAnalyzer(code)
            tokens = lexer.tokenize()
            for token in tokens:
                self.lexical_output.insert(INSERT, f"Токен: {token[0]}, элемент: {token[1]}\n")
            self.lexical_output.insert(INSERT, "* Лексический анализ завершен *\n")
            self.syntax_output.insert(INSERT, "* Синтаксический анализ *\n")
            try:
                parser = SyntaxAnalyzer(tokens)
                parsed_program = parser.parse()
                self.syntax_output.insert(INSERT, f"Синтаксический анализ завершен. Статус: {parsed_program}\n")
                self.semantic_output.insert(INSERT, "* Семантический анализ *\n")
                symbol_table, operations = generate_symbol_table_and_operations(tokens)
                analyzer = SemanticAnalyzer(symbol_table)
                analyzer.analyze(operations)
                errors = analyzer.get_errors()
                if errors:
                    self.semantic_output.insert(INSERT, "Обнаружены ошибки семантического анализа:\n")
                    for error in errors:
                        self.semantic_output.insert(INSERT, f"{error}\n")
                else:
                    self.semantic_output.insert(INSERT, "Семантический анализ успешно завершен. Ошибок нет.\n")
            except Exception as e:
                self.syntax_output.insert(INSERT, f"Ошибка синтаксического анализа: {e}\n")
                self.semantic_output.insert(INSERT, "Семантический анализ не выполнен из-за ошибок синтаксиса\n")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при анализе кода: {e}")

if __name__ == "__main__":
    try:
        from tkinter import ttk
    except ImportError:
        import tkinter.ttk as ttk
    root = Tk()
    app = CompilerGUI(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import tkinter.font as tkFont
import pyperclip


class PubChem:
    def __init__(self, page):
        self.page = page
        self.hazard = []
        self.output = []
        self.chemical = ""
        self.molar = ""
        self.CAS = ""
        self.formula = ""

    def find(self):
        self.findCAS()
        self.findChemical()
        self.findFormula()
        self.findHazard()
        self.findMolar()

    def findHazard(self):
        try:
            start = self.page.index("GHS Hazard Statements\t")
            end = self.page.index("Precautionary Statement Codes\t")
            self.hazard.append("Hazard Category:\n")
            for i in range(1, end - start):
                if i % 2 == 0:
                    continue
                self.hazard.append(self.page[start + i] + "\n")
        except ValueError:
            self.hazard.append("Hazard information not found\n")

    def findChemical(self):
        try:
            point = self.page.index("compound Summary")
            self.chemical = self.page[point + 1]
        except ValueError:
            self.chemical = "Chemical name not found"

    def findMolar(self):
        try:
            point = self.page.index("Molecular Weight\t")
            self.molar = "Molecular Weight: " + self.page[point + 1]
        except ValueError:
            self.molar = "Molecular Weight not found"

    def findCAS(self):
        try:
            point = self.page.index("2.3.1 CAS")
            self.CAS = "CAS Number: " + self.page[point + 2]
        except ValueError:
            self.CAS = "CAS Number not found"

    def findFormula(self):
        try:
            point = self.page.index("Molecular Formula\t")
            self.formula = "Chemical Formula: " + self.page[point + 1]
        except ValueError:
            self.formula = "Chemical Formula not found"

    def getChemical(self):
        return self.chemical

    def getMolar(self):
        return self.molar

    def getCAS(self):
        return self.CAS

    def getHazard(self):
        return "".join(self.hazard)

    def getFormula(self):
        return self.formula

    def __str__(self):
        result = []
        result.append(self.getChemical())
        result.append(self.getCAS())
        result.append(self.getFormula())
        result.append(self.getMolar())
        result.append(self.getHazard())
        return "\n".join(result)


class MainFrame:
    def __init__(self):
        self.delete_button = None
        self.start_button = None
        self.text_area = None
        self.root = tk.Tk()
        self.root.title("一键生成Properties and MSDS")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # 显示初始提示信息
        self.root.after(100, lambda: messagebox.showinfo(
            "使用说明",
            "找到要生成的试剂对应的PubChem页面，ctrl+a全选复制，粘贴到输入框中，点确定输出结果，目前只能输出分子量、化学式、CAS和hazard，CAS可能会有问题，其他的应该还好"))
        self.setup_ui()



    def setup_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # 创建文本区域
        self.text_area = scrolledtext.ScrolledText(main_frame, width=80, height=25, wrap=tk.WORD)
        self.text_area.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.text_area.config(state=tk.NORMAL)


        # 创建按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # 确定按钮
        self.start_button = ttk.Button(button_frame, text="确定", command=self.on_start_click)
        self.start_button.pack(side=tk.LEFT, padx=(0, 20))

        # 清空按钮
        self.delete_button = ttk.Button(button_frame, text="清空", command=self.on_delete_click)
        self.delete_button.pack(side=tk.LEFT)

        # 配置主框架的行列权重
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

    def on_start_click(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("警告", "请输入内容")
            return

        page = text.split('\n')
        chem = PubChem(page)

        try:
            chem.find()
        except Exception as e:
            messagebox.showerror("错误", "出现报错，请按照要求输入\n错误信息: " + str(e))
            messagebox.showinfo("使用说明",
                                "找到要生成的试剂对应的PubChem页面，ctrl+a全选复制，粘贴到输入框中，点确定输出结果\n")
            return

        result = str(chem)
        messagebox.showinfo("结果已复制到剪贴板", result)

        # 复制到剪贴板
        pyperclip.copy(result)

    def on_delete_click(self):
        self.text_area.delete("1.0", tk.END)

    def run(self):
        self.root.mainloop()


def main():
    # 检查是否安装了pyperclip，如果没有则尝试安装
    try:
        import pyperclip
    except ImportError:
        print("pyperclip库未安装，尝试安装...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
        import pyperclip

    app = MainFrame()
    app.run()


if __name__ == "__main__":
    main()
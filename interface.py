import tkinter as tk
from tkinter import ttk, messagebox
from database import Database


class AddProductView(tk.Toplevel):
    price_entry: tk.Entry
    title_entry: tk.Entry
    quantity_entry: tk.Entry

    database = Database()

    def __init__(self, master_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master_window = master_window
        self.init_ui()

    def init_ui(self):
        title_label = tk.Label(self, text='Добавление товара')
        title_label.place(anchor='center')
        title_label.grid(row=0, column=0)

        tk.Label(self, text='Цена: ').grid(row=1, column=0)
        self.price_entry = tk.Entry(self)
        self.price_entry.grid(row=1, column=1)

        tk.Label(self, text='Название: ').grid(row=2, column=0)
        self.title_entry = tk.Entry(self)
        self.title_entry.grid(row=2, column=1)

        tk.Label(self, text='Кол-во: ').grid(row=3, column=0)
        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.grid(row=3, column=1)

        tk.Button(self, text='Добавить', command=self.add_value).grid(row=4)

    def destroy(self) -> None:
        self.update_tree()
        super().destroy()

    def update_tree(self):
        tree = self.master_window.tree

        if not tree:
            return print('No tree selected!')

        for item in tree.get_children():
            tree.delete(item)

        database_records = self.database.get_products()
        for index, record in enumerate(database_records):
            tree.insert("", index, values=tuple(record.values()))

    def add_value(self):
        title, price, quantity = self.title_entry.get(), self.price_entry.get(), self.quantity_entry.get()
        self.database.add_product(title=title, price=price, quantity=quantity)
        messagebox.showinfo('Успех', 'Данные в БД добавлены!')
        self.destroy()


class MainView:
    tree: ttk.Treeview

    tree_columns = dict(
        id='ID',
        title='Название',
        price='Цена',
        qunatity='Кол-во'
    )

    database = Database()

    def __init__(self, root: tk.Tk = None):
        self.root = tk.Tk() if not root else root
        self.root.title("программа")
        self.root.geometry('900x350')
        self.root.configure(bg='green')
        self.init_ui()

    def build_tree(self):
        columns = tuple(self.tree_columns.keys())
        tree = ttk.Treeview(self.root,
                            columns=columns,
                            show='headings')

        for key, heading in self.tree_columns.items():
            tree.heading(key, text=heading)

        self.update_tree(tree)
        return tree

    def update_tree(self, tree: ttk.Treeview = None):
        if not tree:
            tree = self.tree

        print("Updating tree: ", tree.__dict__)

        for item in tree.get_children():
            tree.delete(item)

        database_records = self.database.get_products()
        for index, record in enumerate(database_records):
            tree.insert("", index, values=tuple(record.values()))

    def to_add_view(self):
        AddProductView(master_window=self)
        self.update_tree(self.tree)

    @property
    def tree_focus(self):
        product_focus = self.tree.focus()
        item = self.tree.item(product_focus)

        if not product_focus or not item or not item.get('values'):
            return None

        row_id = item['values'][0]
        return row_id

    def delete_by_focus(self):
        focus_id = self.tree_focus
        if focus_id:
            self.database.delete_product(id=focus_id)

        self.update_tree(self.tree)

    def init_ui(self):
        self.tree = self.build_tree()
        self.tree.grid(row=0, column=0)
        self.tree.place(x=10, y=10)

        tk.Button(self.root, text='Добавить', command=self.to_add_view).place(x=10, y=250)
        tk.Button(self.root, text='Удалить', command=self.delete_by_focus).place(x=120, y=250)

        tk.Label(self.root,
                 text='Короче все воркает прям с кайфом лютым. Цитата года: "Мы пьем в дни на букву "с", среда, суббота и СЕГОДНЯ"'
                 ).place(x=10, y=300)
    def mainloop(self):
        return self.root.mainloop()


if __name__ == '__main__':
    main = MainView()
    main.mainloop()

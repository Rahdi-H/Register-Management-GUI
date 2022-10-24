from email.mime import image
import tkinter
import tkinter.messagebox
from turtle import width
import customtkinter
import sqlite3
import datetime
import pandas as pd
import openpyxl
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"



a = datetime.datetime.now()
datee, y = str(a.today()).split(' ')

class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("COMM UNIT SIGNAL CENTER")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        self.iconbitmap('baf.png')

        self.image = Image.open('baf.png')
        self.imgg = self.image.resize((200,200),)
        self.img = ImageTk.PhotoImage(self.imgg)
        self.lbl = customtkinter.CTkLabel(image = self.img, width=50, height=50)
        self.lbl.place(rely=0.2, relx=0.5, anchor=tkinter.CENTER)

        self.frame = customtkinter.CTkFrame(master=self, width=600, height=400, corner_radius=10)
        self.frame.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        IN_LOS_BUTTON = customtkinter.CTkButton(master=self.frame, width=120, height=50, corner_radius=5, text='IN LOS', command=self.in_los)
        IN_LOS_BUTTON.grid(row=0, column=0, padx=20, pady=20)

        IN_ISD_BUTTON = customtkinter.CTkButton(master=self.frame, width=120, height=50, corner_radius=5, text='IN ISD', command=self.in_isd)
        IN_ISD_BUTTON.grid(row=0, column=1, padx=20, pady=20)

        IN_NON_CRYPTO_BUTTON = customtkinter.CTkButton(master=self.frame, width=120, height=50, corner_radius=5, text="IN NON CRYPTO", command=self.in_non_crypto)
        IN_NON_CRYPTO_BUTTON.grid(row=0, column=2, padx=20, pady=20)

        OUT_LOS_BUTTON = customtkinter.CTkButton(master=self.frame, width=120, height=50, corner_radius=5, text='OUT LOS', command=self.out_los)
        OUT_LOS_BUTTON.grid(row=1, column=0, padx=20, pady=20)

        OUT_ISD_BUTTON = customtkinter.CTkButton(master=self.frame, width=120, height=50, corner_radius=5, text='OUT ISD', command=self.out_isd)
        OUT_ISD_BUTTON.grid(row=1, column=1, padx=20, pady=20)

        OUT_NON_CRYPTO_BUTTON = customtkinter.CTkButton(master=self.frame, width=120, height=50, corner_radius=5, text='OUT NON CRYPTO', command=self.out_non_crypto)
        OUT_NON_CRYPTO_BUTTON.grid(row=1, column=2, padx=20, pady=20)

    def in_los(self):
        def button_add():
            conn = sqlite3.connect('comm_unit.db')
            c = conn.cursor()
            c.execute("INSERT INTO IN_LOS VALUES(?, ?, ?, ?, ?);", (datee, message_number.get(), from_option.get(), for_entry.get(), sign_entry.get()))
            conn.commit()
            conn.close()

        def button_print():
            conn = sqlite3.connect('comm_unit.db')
            c = conn.cursor()
            #c.execute("SELECT ROWID From IN_LOS WHERE Date = (?) LIMIT 1;", print_from.get())
            #print(c.fetchone())
            data = "SELECT rowid, * FROM IN_LOS" #WHERE ROWID BETWEEN {id_from.fetchone()} AND {id_to.fetchone()}"
            df = pd.read_sql(data, conn)
            df.to_excel(f"{file_name.get()}.xlsx")
            conn.close()
        def show_recent():
            conn = sqlite3.connect('comm_unit.db')
            c = conn.cursor()
            c.execute("SELECT rowid FROM IN_LOS ORDER BY ROWID DESC")
            i = c.fetchone()
            recent_data_id.set_text(i)
            recent_data_ref.set_text(message_number.get())
            recent_data_date.set_text(datee)
            recent_data_from.set_text(from_option.get())
            recent_data_for.set_text(for_entry.get())
            recent_data_sign.set_text(sign_entry.get())
            conn.close()
        def button_modify():
            iii = modify_entry.get()
            def button_update():
                conn = sqlite3.connect('comm_unit.db')
                c = conn.cursor()
                c.execute("""UPDATE IN_LOS SET 
                MessageNumber = :ref, 
                From_ = :fromm, 
                For_ = :forr, 
                Sign = :sign 
                WHERE rowid = :idd""", 
                {'ref' : message_numberr.get(), 'fromm' : from_optionr.get(), 'forr' : for_entryr.get(), 'sign' : sign_entryr.get(), 'idd' : modify_entry.get()})
                conn.commit()
                conn.close()
            def show_updated():
                conn = sqlite3.connect('comm_unit.db')
                c = conn.cursor()
                c.execute("SELECT rowid, * FROM IN_LOS WHERE rowid = :ii", {'ii': iii})
                o = c.fetchone()
                recent_data_idr.set_text(o[0])
                recent_data_refr.set_text(o[2])
                recent_data_dater.set_text(o[1])
                recent_data_fromr.set_text(o[3])
                recent_data_forr.set_text(o[4])
                recent_data_signr.set_text(o[5])
                conn.close()
            windo = customtkinter.CTkToplevel(window)
            windo.geometry('750x400')
            windo.title("Modify IN LOS")
            recent_data_frame = customtkinter.CTkFrame(master=windo, width=755, height=50, corner_radius=5)
            recent_data_frame.place(relx=0.5, rely=0.1, anchor = tkinter.CENTER)
            recent_data_id_label = customtkinter.CTkLabel(master=recent_data_frame, width=50, height=25, corner_radius=5, text='Serial')
            recent_data_id_label.grid(row=0, column=0)
            recent_data_idr = customtkinter.CTkLabel(master=recent_data_frame, width=50, height=25, corner_radius=5)
            recent_data_idr.grid(row=1, column=0)
            recent_data_ref_label = customtkinter.CTkLabel(master=recent_data_frame, width=80, height=25, corner_radius=5, text='Ref')
            recent_data_ref_label.grid(row=0, column=1)
            recent_data_refr = customtkinter.CTkLabel(master=recent_data_frame, width=80, height=25, corner_radius=5)
            recent_data_refr.grid(row=1, column=1)
            recent_data_date_label = customtkinter.CTkLabel(master=recent_data_frame, width=50, height=25, corner_radius=5, text='Date')
            recent_data_date_label.grid(row=0, column=2)
            recent_data_dater = customtkinter.CTkLabel(master=recent_data_frame, width=50, height=25, corner_radius=5)
            recent_data_dater.grid(row=1, column=2)
            recent_data_from_label = customtkinter.CTkLabel(master=recent_data_frame, width=50, height=25, corner_radius=5, text='From')
            recent_data_from_label.grid(row=0, column=3)
            recent_data_fromr = customtkinter.CTkLabel(master=recent_data_frame, width=50, height=25, corner_radius=5)
            recent_data_fromr.grid(row=1, column=3)
            recent_data_For_label = customtkinter.CTkLabel(master=recent_data_frame, width=80, height=25, corner_radius=5, text="For")
            recent_data_For_label.grid(row=0, column=4)
            recent_data_forr = customtkinter.CTkLabel(master=recent_data_frame, width=80, height=25, corner_radius=5)
            recent_data_forr.grid(row=1, column=4)
            recent_data_sign_label = customtkinter.CTkLabel(master=recent_data_frame, width=50, height=25, corner_radius=5, text='Sign')
            recent_data_sign_label.grid(row=0, column=5)
            recent_data_signr = customtkinter.CTkLabel(master=recent_data_frame, width=50, height=25, corner_radius=5)
            recent_data_signr.grid(row=1, column=5)
            frame = customtkinter.CTkFrame(master=windo, width=self.WIDTH, height=150, corner_radius=5)
            frame.place(relx = 0.5, rely= 0.25, anchor = tkinter.CENTER)
            message_number_label = customtkinter.CTkLabel(master=frame, text="Ref")
            message_number_label.grid(row=0, column=0)
            message_numberr = customtkinter.CTkEntry(master=frame, placeholder_text="Reference Number", width=170, height=50, border_width=2, corner_radius=5)
            message_numberr.grid(row=1, column=0)
            from_label = customtkinter.CTkLabel(master=frame, text="From")
            from_label.grid(row=0, column=1)
            from_optionr = customtkinter.CTkOptionMenu(master=frame, values=["ZHR", "MTR", 'BBD', "PKP", "CXB", "CRU", "MRU", "BRU", 'SNR', "BSRU", "71 SQN", "74 SQN"], height=50)
            from_optionr.set("ZHR")
            from_optionr.grid(row=1, column=1)
            for_entry_label = customtkinter.CTkLabel(master=frame, text='For')
            for_entry_label.grid(row=0, column=2)
            for_entryr = customtkinter.CTkComboBox(master=frame, values=['ADOC', "BSR", 'CSTI', "103 ATTU", 'Dte Air Ops', 'Dte AD', 'Dte AI', 'Dte Air Trg', 'Dte Armt', 'Dte C&E', 'Dte CW&IT', 'Dte MS'], width=150, height=50, border_width=2, corner_radius=5)
            for_entryr.grid(row=1, column=2)
            for_entryr.set('ADOC')
            sign_entry_label = customtkinter.CTkLabel(master=frame, text='Sign')
            sign_entry_label.grid(row=0, column=3)
            sign_entryr = customtkinter.CTkComboBox(master=frame, values=['NSR', 'HNF', 'ARN', 'RHD', 'IBR', 'ARF', 'SYF', 'ERL', 'JKR', 'FSL'], width=150, height=50, border_width=2, corner_radius=5)
            sign_entryr.grid(row=1, column=3)
            sign_entryr.set('NSR')
            update_button = customtkinter.CTkButton(master=windo, text='UPDATE', height=50, width=150, command=lambda:[button_update(), show_updated()])
            update_button.place(relx=0.5, rely = 0.5, anchor=tkinter.CENTER)

        window = customtkinter.CTkToplevel(self)
        window.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        window.title('IN LOS')
        recent_data_frame = customtkinter.CTkFrame(master=window, width=755, height=50, corner_radius=5)
        recent_data_frame.place(relx=0.5, rely=0.1, anchor = tkinter.CENTER)
        recent_data_id_label = customtkinter.CTkLabel(master=recent_data_frame, width=50, height=25, corner_radius=5, text='Serial')
        recent_data_id_label.grid(row=0, column=0)
        recent_data_id = customtkinter.CTkLabel(master=recent_data_frame, width=50, height=25, corner_radius=5)
        recent_data_id.grid(row=1, column=0)
        recent_data_ref_label = customtkinter.CTkLabel(master=recent_data_frame, width=80, height=25, corner_radius=5, text='Ref')
        recent_data_ref_label.grid(row=0, column=1)
        recent_data_ref = customtkinter.CTkLabel(master=recent_data_frame, width=80, height=25, corner_radius=5)
        recent_data_ref.grid(row=1, column=1)
        recent_data_date_label = customtkinter.CTkLabel(master=recent_data_frame, width=50, height=25, corner_radius=5, text='Date')
        recent_data_date_label.grid(row=0, column=2)
        recent_data_date = customtkinter.CTkLabel(master=recent_data_frame, width=50, height=25, corner_radius=5)
        recent_data_date.grid(row=1, column=2)
        recent_data_from_label = customtkinter.CTkLabel(master=recent_data_frame, width=50, height=25, corner_radius=5, text='From')
        recent_data_from_label.grid(row=0, column=3)
        recent_data_from = customtkinter.CTkLabel(master=recent_data_frame, width=50, height=25, corner_radius=5)
        recent_data_from.grid(row=1, column=3)
        recent_data_For_label = customtkinter.CTkLabel(master=recent_data_frame, width=80, height=25, corner_radius=5, text="For")
        recent_data_For_label.grid(row=0, column=4)
        recent_data_for = customtkinter.CTkLabel(master=recent_data_frame, width=80, height=25, corner_radius=5)
        recent_data_for.grid(row=1, column=4)
        recent_data_sign_label = customtkinter.CTkLabel(master=recent_data_frame, width=50, height=25, corner_radius=5, text='Sign')
        recent_data_sign_label.grid(row=0, column=5)
        recent_data_sign = customtkinter.CTkLabel(master=recent_data_frame, width=50, height=25, corner_radius=5)
        recent_data_sign.grid(row=1, column=5)
        frame = customtkinter.CTkFrame(master=window, width=self.WIDTH, height=150, corner_radius=5)
        frame.place(relx = 0.5, rely= 0.25, anchor = tkinter.CENTER)
        message_number_label = customtkinter.CTkLabel(master=frame, text="Ref")
        message_number_label.grid(row=0, column=0)
        message_number = customtkinter.CTkEntry(master=frame, placeholder_text="Reference Number", width=170, height=50, border_width=2, corner_radius=5)
        message_number.grid(row=1, column=0)
        from_label = customtkinter.CTkLabel(master=frame, text="From")
        from_label.grid(row=0, column=1)
        from_option = customtkinter.CTkOptionMenu(master=frame, values=["ZHR", "MTR", 'BBD', "PKP", "CXB", "CRU", "MRU", "BRU", 'SNR', "BSRU", "71 SQN", "74 SQN"], height=50)
        from_option.set("ZHR")
        from_option.grid(row=1, column=1)
        for_entry_label = customtkinter.CTkLabel(master=frame, text='For')
        for_entry_label.grid(row=0, column=2)
        for_entry = customtkinter.CTkComboBox(master=frame, values=['ADOC', "BSR", 'CSTI', "103 ATTU", 'Dte Air Ops', 'Dte AD', 'Dte AI', 'Dte Air Trg', 'Dte Armt', 'Dte C&E', 'Dte CW&IT', 'Dte MS'], width=150, height=50, border_width=2, corner_radius=5)
        for_entry.grid(row=1, column=2)
        for_entry.set('ADOC')
        sign_entry_label = customtkinter.CTkLabel(master=frame, text='Sign')
        sign_entry_label.grid(row=0, column=3)
        sign_entry = customtkinter.CTkComboBox(master=frame, values=['NSR', 'HNF', 'ARN', 'RHD', 'IBR', 'ARF', 'SYF', 'ERL', 'JKR', 'FSL'], width=150, height=50, border_width=2, corner_radius=5)
        sign_entry.grid(row=1, column=3)
        sign_entry.set('NSR')
        buttons_view = customtkinter.CTkFrame(master=window, width=250, height=150, corner_radius=5)
        buttons_view.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)
        add_button = customtkinter.CTkButton(master=frame, width=150, height=50, corner_radius=5, text='ADD', command=lambda:[button_add(), show_recent()])
        add_button.grid(row=1, column=4)
        modify_entry = customtkinter.CTkEntry(master=buttons_view, width=150, height=25, corner_radius=5, placeholder_text="Serial No")
        modify_entry.grid(row=0, column=1)
        modify_button = customtkinter.CTkButton(master=buttons_view, width=150, height=50, corner_radius=5, text='MODIFY', command=button_modify)
        modify_button.grid(row=3, column=1)
        #print_from = customtkinter.CTkEntry(master=buttons_view, width=150, height=25, corner_radius=5, placeholder_text='From', border_width=2)
        #print_from.grid(row=0, column=2)
        #print_to = customtkinter.CTkEntry(master=buttons_view, width=150, height=25, corner_radius=5, placeholder_text='To', border_width=2)
        #print_to.grid(row=1, column=2)
        file_name = customtkinter.CTkEntry(master=buttons_view, width=150, height=25, corner_radius=5, placeholder_text='File Name', border_width=2)
        file_name.grid(row=0, column=2)
        print_button = customtkinter.CTkButton(master=buttons_view, width=150, height=50, corner_radius=5, text='PRINT', command=button_print)
        print_button.grid(row=3, column=2)

    def in_isd(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        window.title('IN ISD')

    def out_los(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        window.title('OUT LOS')

    def out_isd(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        window.title('OUT ISD')

    def in_non_crypto(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        window.title('IN NON CRYPTO')

    def out_non_crypto(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        window.title('OUT NON CRYPTO')

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
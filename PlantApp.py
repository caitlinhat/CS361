import tkinter as tk
# from datetime import timedelta
#
# from tkcalendar import DateEntry
from tkinter import messagebox
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="!October2023_!!",
    database="myplants",
)

cursor = mydb.cursor()


class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("500x500")
        self.configure(bg="lightgray")
        self._frame = None
        self.switch_frame(HomePage)

    def switch_frame(self, frame_class, *args):
        new_frame = frame_class(self, *args)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


# Home page
class HomePage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        title_label = tk.Label(self, text="Home")
        title_label.pack(side="top")

        # Top frame
        home_frame = tk.Frame(self, highlightthickness=2)

        # frame_label = tk.Label(home_frame, text="Due today:")
        # frame_label.pack()

        # Navigation buttons
        my_plants_button = tk.Button(self,
                                     text="My Plants",
                                     command=lambda: parent.switch_frame(MyPlantsPage))

        locations_button = tk.Button(self,
                                     text="Locations",
                                     command=lambda: parent.switch_frame(LocationsPage))

        # scheduler_button = tk.Button(self,
        #                              text="Scheduler",
        #                              command=lambda: parent.switch_frame(SchedulerPage))

        search_plants_button = tk.Button(self,
                                         text="Search Plants",
                                         command=lambda: parent.switch_frame(SearchPage))

        home_frame.pack(side="top", fill="both", expand=True)
        # frame_label.pack()
        my_plants_button.pack(side="left", padx=10)
        locations_button.pack(side="left", padx=10)
        # scheduler_button.pack()
        search_plants_button.pack(side="left", padx=10)


class LocationsPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        add_location_sql = "INSERT INTO my_locations (name, light) VALUES (%s, %s);"

        remove_location_sql = "DELETE FROM my_locations WHERE name=%s AND loc_id <>0;"

        def open_add_popup():
            top = tk.Toplevel(self)
            name_var = tk.StringVar()
            light_var = tk.StringVar()

            def add_loc():
                loc_name = name_var.get()
                loc_light = light_var.get()

                cursor.execute(add_location_sql, (loc_name, loc_light))
                mydb.commit()

                if cursor.rowcount > 0:
                    messagebox.showinfo("Success!", "Location added")

                else:
                    messagebox.showerror("Error", "Failed to add location")

            name_field = tk.Entry(top, textvariable=name_var)
            light_field = tk.Entry(top, textvariable=light_var)
            submit_button = tk.Button(top,
                                      text="Submit",
                                      command=add_loc)

            name_field.pack()
            light_field.pack()
            submit_button.pack()

        def open_remove_popup():
            top = tk.Toplevel(self)
            name_var = tk.StringVar()

            def remove_loc():
                loc_name = name_var.get()

                cursor.execute(remove_location_sql, (loc_name,))
                mydb.commit()

                if cursor.rowcount > 0:
                    messagebox.showinfo("Success!", "Location removed")

                else:
                    messagebox.showerror("Error", "Failed to remove location")

            name_field = tk.Entry(top, textvariable=name_var)
            submit_button = tk.Button(top,
                                      text="Submit",
                                      command=remove_loc)

            name_field.pack()
            submit_button.pack()

        home_button = tk.Button(self,
                                text="Home",
                                command=lambda: parent.switch_frame(HomePage))

        add_loc_button = tk.Button(self,
                                   text="Add location",
                                   command=lambda: open_add_popup())

        remove_loc_button = tk.Button(self,
                                      text="Remove location",
                                      command=lambda: open_remove_popup())

        title_label = tk.Label(self, text="My Locations")
        title_label.pack(side="top")
        home_button.pack()

        def display_locations():
            cursor.execute("SELECT name, light from my_locations")
            for name, light in cursor:
                label = tk.Label(text=f"{name}: {light}")
                label.pack()

        display_locations()
        add_loc_button.pack()
        remove_loc_button.pack()


class MyPlantsPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        def open_add_popup():
            top = tk.Toplevel(self)
            name_var = tk.StringVar()
            nickname_var = tk.StringVar()
            water_var = tk.StringVar()
            light_var = tk.StringVar()
            food_var = tk.StringVar()
            store_var = tk.StringVar()
            price_var = tk.StringVar()
            purchase_var = tk.StringVar()

            def add_plant():
                plant_name = name_var.get()
                nickname = nickname_var.get()
                water = water_var.get()
                light = light_var.get()
                food = food_var.get()
                store = store_var.get()
                price = price_var.get()
                purchase_date = purchase_var.get()

                cursor.execute(add_plant_sql, (plant_name, nickname, water, light, food, store, price, purchase_date))
                mydb.commit()

                if cursor.rowcount > 0:
                    messagebox.showinfo("Success!", "Plant added")

                else:
                    messagebox.showerror("Error", "Failed to add plant")

            name_field = tk.Entry(top, textvariable=name_var)
            nickname_field = tk.Entry(top, textvariable=nickname_var)
            water_field = tk.Entry(top, textvariable=water_var)
            light_field = tk.Entry(top, textvariable=light_var)
            food_field = tk.Entry(top, textvariable=food_var)
            store_field = tk.Entry(top, textvariable=store_var)
            price_field = tk.Entry(top, textvariable=price_var)
            purchase_field = tk.Entry(top, textvariable=purchase_var)

            submit_button = tk.Button(top,
                                      text="Submit",
                                      command=add_plant)

            name_field.pack()
            nickname_field.pack()
            water_field.pack()
            light_field.pack()
            food_field.pack()
            store_field.pack()
            price_field.pack()
            purchase_field.pack()
            submit_button.pack()

        def open_remove_popup():
            top = tk.Toplevel(self)

            name_var = tk.StringVar()

            def remove_plant():
                plant_name = name_var.get()

                cursor.execute(remove_plant_sql, (plant_name,))
                mydb.commit()

                if cursor.rowcount > 0:
                    messagebox.showinfo("Success!", "Plant removed")

                else:
                    messagebox.showerror("Error", "Failed to remove plant")

            name_field = tk.Entry(top, textvariable=name_var)
            submit_button = tk.Button(top,
                                      text="Submit",
                                      command=remove_plant)

            name_field.pack()
            submit_button.pack()

        def display_plant_list():
            cursor.execute("SELECT plant_id, nickname from my_plants")
            for plant_id, name in cursor:
                button = tk.Button(text=name, command=lambda id=plant_id: open_plant_page(plant_id))
                button.pack()

        def open_plant_page(plant_data):
            parent.switch_frame(PlantPage, plant_data)

        add_plant_sql = ("INSERT INTO my_plants (name, nickname, water, light, food, store, price, purchase_date) "
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);")

        remove_plant_sql = "DELETE FROM my_plants WHERE name=%s AND plant_id <> 0;"

        display_plant_list()

        home_button = tk.Button(self,
                                text="Home",
                                command=lambda: parent.switch_frame(HomePage))

        add_button = tk.Button(self,
                               text="Add plant",
                               command=lambda: open_add_popup())

        remove_button = tk.Button(self,
                                  text="Remove plant",
                                  command=lambda: open_remove_popup())

        home_button.pack()
        add_button.pack()
        remove_button.pack()


class PlantPage(tk.Frame):
    def __init__(self, parent, plant_data):
        tk.Frame.__init__(self, parent)

        title_label = tk.Label(self, text="Plant")

        grab_plant_info_sql = "SELECT name, nickname, water, light, food, store, price, purchase_date from my_plants"

        cursor.execute(grab_plant_info_sql)
        data_list = cursor.fetchall()

        for index, item in enumerate(data_list):
            name_index = item[1]
            scientific_index = item[0]
            water_index = item[2]
            light_index = item[3]
            food_index = item[4]

        plant_label = tk.Label(self, text=f"{name_index}")
        scientific_label = tk.Label(self, text=f"{scientific_index}")
        location_label = tk.Label(self, text="Location:")
        care_title = tk.Label(self, text="Care Needs")
        water_label = tk.Label(self, text=f"Water: {water_index}")
        light_label = tk.Label(self, text=f"Light: {light_index}")
        food_label = tk.Label(self, text=f"Food: {food_index}")

        home_button = tk.Button(self,
                                text="Home",
                                command=lambda: parent.switch_frame(HomePage))

        home_button.pack(side="top")
        title_label.pack(side="top")
        plant_label.pack()
        scientific_label.pack()
        location_label.pack()
        care_title.pack()
        water_label.pack()
        light_label.pack()
        food_label.pack()


# class SchedulerPage(tk.Frame):
#     def __init__(self, parent):
#         tk.Frame.__init__(self, parent)
#         selected_plants = []
#
#         title_label = tk.Label(self, text="Care Schedule")
#
#         home_button = tk.Button(self,
#                                 text="Home",
#                                 command=lambda: parent.switch_frame(HomePage))
#
#         grab_plant_info_sql = "SELECT name, nickname, water, light, food, store, price, purchase_date from my_plants"
#
#         def convert_schedule_to_days(description):
#             days = 0
#             if "week" in description:
#                 days = 7
#             elif "month" in description:
#                 days = 30
#             else:
#                 schedule_map = {
#                     "daily": 1,
#                     "weekly":7,
#                     "month": 30,
#                     "monthly": 30,
#                 }
#
#             words = description.lower().strip().split()
#
#             for word in words:
#                 if word in schedule_map:
#                     days += schedule_map[word]
#                 elif word.isdigit():
#                     days += int(word)
#             return days
#
#         def get_plant_data():
#             cursor.execute(grab_plant_info_sql)
#             for plant in cursor.fetchall():
#                 name = plant[1]
#                 plant_var = tk.BooleanVar()
#                 checkbox = tk.Checkbutton(text=name, variable=plant_var)
#                 checkbox.pack()
#                 selected_plants.append((name, plant_var))
#
#         day_var = tk.IntVar()
#
#         def get_days():
#             days = day_var.get()
#
#             day_field = tk.Entry(textvariable=days)
#             day_field.pack()
#
#         self.cal = DateEntry()
#
#         # def get_start_date():
#         #     selected_date = self.cal.get_date()
#
#         def generate_schedule():
#             start_date = self.cal.get_date()
#             duration = day_var.get()
#
#             for plant, plant_checkbox in selected_plants:
#                 if plant_checkbox.get():
#                     cursor.execute("SELECT water from my_plants")
#                     result = cursor.fetchone()
#                     if result:
#                         schedule_desc = result[0]
#                         care_schedule = []
#
#                         days = convert_schedule_to_days(schedule_desc)
#
#                         for day in range(0, duration * days, days):
#                             schedule_date = start_date + timedelta(days=day)
#                             care_schedule.append(schedule_date)
#
#                         schedule_label = tk.Label(self, text="Care schedule:")
#                         schedule_label.pack()
#
#                         for date in care_schedule:
#                             schedule_item = tk.Label(self, text=date.strftime('%Y-%m-%d'))
#                             print(schedule_item)
#         #             display_schedule(plant, care_schedule)
#         #
#         # def display_schedule(plant, care_schedule):
#         #     schedule_window = tk.Toplevel(self)
#         #     schedule_window.title(f"Care schedule")
#         #     schedule_label = tk.Label(schedule_window, text = "Care schedule:")
#         #     schedule_label.pack()
#         #
#         #     for date in care_schedule:
#         #         schedule_item = tk.Label(schedule_window, text=date.strftime('%Y-%m-%d'))
#         #         schedule_item.pack()
#
#
#         # Top frame
#         home_frame = tk.Frame(self, highlightthickness=2)
#         select_label = tk.Label(self, text="Select plants to include:")
#
#         date_label = tk.Label(self, text="Choose a start date:")
#         duration_label = tk.Label(self, text="Duration:")
#
#         generate_button = tk.Button(text="Go!", command=generate_schedule)
#
#         home_button.pack(side="top")
#         title_label.pack(side="top")
#         home_frame.pack()
#         select_label.pack()
#         get_plant_data()
#         get_days()
#         self.cal.pack()
#         generate_button.pack()
#         date_label.pack()
#         duration_label.pack()


class SearchPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        title_label = tk.Label(self, text="Search")

        home_button = tk.Button(self,
                                text="Home",
                                command=lambda: parent.switch_frame(HomePage))

        search = tk.Entry()

        go_button = tk.Button(text="Go!")

        home_button.pack(side="top")
        title_label.pack(side="top")
        search.pack()
        go_button.pack()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

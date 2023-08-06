import os

try:
    from dearpygui.core import *
    from dearpygui.simple import *
except ImportError:
    exit("Dear PyGui not installed, please run pip to install it.")
from drop import *
from drop import moderation, errors, finder, __version__
from random import randint
import configparser

print(f"Running in {os.getcwd()}")
if not os.path.exists('data/'):
    print("No data/ directory! Are you sure you're running this GUI in the right directory?")

window_margins = 150
window_width = get_main_window_size()[0]
window_height = get_main_window_size()[1]  # how the fuck did I forget to set the index to 1
config_filepath = 'data/guiconfig.ini'

config = configparser.ConfigParser()
config.read(config_filepath)
if not config.has_section('position'):
    config.add_section('position')


class Rules:
    @staticmethod
    def show_rules(sender, data):
        if data:
            guild_id = int(data)
        else:
            guild_id = get_value("rule_guild")
        parent = f"Rules for {guild_id}"
        rules = []
        if parent in get_windows():
            delete_item(parent)
        try:
            # for key, value in moderation.get_rules(guild_id).sort().items():
            for key, value in {key: value for key, value in sorted(moderation.get_rules(guild_id).items(),
                                                                   key=lambda item: item[0])}.items():
                # That way, stuff is sorted by keys. If you really wanted to, you could change item[0] to item[1]
                # if you wanted to sort by value.
                rules.append(f"{key}: {value}")
        except errors.NoRulesError:
            show_item("Incorrect guild.")
        else:
            with window(parent, no_title_bar=False, autosize=False, no_resize=False, no_close=False, no_move=False):
                add_text('\n'.join(rules))
            hide_item("Incorrect guild.")

    @staticmethod
    def set_rule(sender, data):
        guild_id = get_value("rule_guild")
        rule_key = get_value('Rule Key').lower()
        rule_value = get_value("Rule Value")
        moderation.set_rule(guild_id, rule_key, rule_value)
        delete_item("Rule description window")

    @staticmethod
    def do_rule_popup(sender, data):
        guild_id = get_value("rule_guild")
        rule_key = get_value('Rule Key').lower()
        if not (guild_id or rule_key):
            if not guild_id:
                show_item("Incorrect guild.")
            if not rule_key:
                show_item("Invalid rule key.")
            return
        if "Rule description window" in get_windows():
            delete_item("Rule description window")
        with window(f"Rule description window", no_title_bar=False, autosize=True, no_resize=False,
                    no_close=False, no_move=False):
            add_text('Rule description:')
            def_val = moderation.get_rule(guild_id, rule_key)
            if not def_val:
                def_val = ""
            add_input_text('Rule Value', label="", on_enter=True, callback=Rules.set_rule,
                           default_value=def_val)


class Guilds:
    @staticmethod
    def get_warned_users(sender, data):
        # data is guild id.
        data = int(data)  # so that it's an actual ID, grr.
        window_name = f"Warns for guild {data}"
        if window_name in get_windows():
            delete_item(window_name)
        with window(window_name, no_title_bar=False, autosize=False, no_resize=False,
                    no_close=False, no_move=False):
            user_list = finder.find_warns(data)
            if not user_list:
                add_text("There are no warned users in this guild.", color=[255, 0, 0])
                return
            for user in user_list:
                if f"Warns for user {user}" in get_windows():
                    thing_name = f"Warns for user {user}"
                    delete_item(thing_name, children_only=True)
                    delete_item(thing_name)
                warn_data = moderation.get_warns(data, user)
                warns = warn_data.get('warns')
                with collapsing_header(f'all_warns##{user}', label=f"{warn_data.get('offender_name')} ({data})"):
                    for index, warn in enumerate(warns):
                        add_text(f"{warn.get('reason')}\n"
                                 f"warned by {warn.get('warner_name')} (id: {warn.get('warner')}), "
                                 f"in channel {warn.get('channel')}, warned on {warn.get('datetime')}")
                        add_button(f"{user}_del_warn##{index}", callback=Warns.delete_warn, callback_data=[
                            data, user, f'{index}'  # you gotta do some out-of-the-box thinking.
                        ], label="Delete warn")
                        add_text(f"{user}_deleted_warn##{index}", default_value="Deleted warn.", show=False)
                        add_spacing()


class Warns:
    @staticmethod
    def update_offender_name(sender, data):
        guild_id = get_value("warn_guild")
        offender_id = get_value("warn_offender_id")
        offender_name = moderation.get_warns(guild_id, offender_id)
        if offender_name and not get_value("warn_offender_name"):
            offender_name = offender_name.get("offender_name")
            set_value("warn_offender_name", offender_name)

    @staticmethod
    def add_warn():
        guild_id = get_value("warn_guild")
        author_id = get_value("warn_author_id")
        author_name = get_value("warn_author_name")
        offender_id = get_value("warn_offender_id")
        offender_name = get_value("warn_offender_name")
        channel_id = get_value("warn_channel")
        reason = get_value("warn_reason")
        if not (guild_id or author_id or author_name or offender_id or offender_name or channel_id or reason):
            # It just works.
            show_item("warn_fill_all_the_fucking_fields")
            return
        hide_item("warn_fill_all_the_fucking_fields")
        moderation.warn(guild_id, offender_id, offender_name, author_id, author_name, channel_id, reason)

    @staticmethod
    def show_warns():
        guild_id = get_value("warn_guild")
        offender_id = get_value("warn_offender_id")
        hide_item("warn_invalid_offender_id")
        hide_item("warn_invalid_guild")
        hide_item("warn_no_warns")
        proceed = True
        if not offender_id:
            show_item("warn_invalid_offender_id")
            proceed = False
        if not guild_id:
            show_item("warn_invalid_guild")
            proceed = False
        if proceed:
            warns = moderation.get_warns(guild_id, offender_id)
            if not warns:
                show_item("warn_no_warns")
                return
            parent = f"Warns for user {warns.get('offender_name')}"
            window_list = get_windows()
            if parent in window_list:
                delete_item(parent, children_only=True)
                delete_item(parent)
            if f"Warns for guild {guild_id}" in window_list:
                thing_name = f"Warns for guild {guild_id}"
                delete_item(thing_name, children_only=True)
                delete_item(thing_name)
            with window(parent, no_title_bar=False, autosize=True, no_resize=False, no_close=False, no_move=False,
                        on_close=lambda: delete_item(parent)):
                for index, warn in enumerate(warns.get("warns")):
                    add_text(f"{warn.get('reason')}\n"
                             f"warned by {warn.get('warner_name')} (id: {warn.get('warner')}), "
                             f"in channel {warn.get('channel')}, warned on {warn.get('datetime')}")
                    add_button(f"{offender_id}_del_warn##{index}", callback=Warns.delete_warn, callback_data=[
                        guild_id, offender_id, f'{index}'  # you gotta do some out-of-the-box thinking.
                    ], label="Delete warn")
                    add_text(f"{offender_id}_deleted_warn##{index}", default_value="Deleted warn.", show=False)
                    add_spacing()

    @staticmethod
    def delete_warn(sender, data):
        moderation.remove_warn(data[0], data[1], int(data[2]))
        show_item(f"{data[1]}_deleted_warn##{data[2]}")


class GuiStuff:
    @staticmethod
    def about_drop():
        if 'About window' in get_windows():
            delete_item('About window')
        with window('About window', no_title_bar=False, autosize=True, no_resize=True, no_close=False, no_move=False,
                    on_close=lambda: delete_item("About window")):
            add_text(f"Drop version {__version__}")
            with collapsing_header("Drop licenses", default_open=True):
                add_text(licenses())

    @staticmethod
    def theme_callback(sender, data):
        set_theme("Dark Grey")  # other themes just look weird without this one being set first.
        set_theme(sender)

    @staticmethod
    def save_window_pos():
        print("Saving window positions")
        if not os.path.exists('data/'):
            os.mkdir('data/')
        config.read(config_filepath)
        for opened_window in get_windows():
            if ('##' in opened_window) or (opened_window == 'main') or ('dialog' in opened_window) \
                    or ('for' in opened_window):
                pass
            else:
                window_pos = get_window_pos(opened_window)
                pos_string = f'{window_pos[0]}x{window_pos[1]}'
                config.set('position', opened_window.lower(), pos_string)
                with open(config_filepath, 'w+') as f:
                    config.write(f)

    @staticmethod
    def set_window_pos():
        config.read(config_filepath)
        for opened_window in get_windows():
            if ('##' in opened_window) or (opened_window == 'main') or ('dialog' in opened_window) \
                    or ('for' in opened_window):
                pass
            else:
                try:
                    position_str = config.get('position', opened_window)
                except configparser.NoOptionError:
                    # that window has not been saved yet.
                    x_pos = randint(window_margins, int(window_width - window_margins))
                    y_pos = randint(window_margins, int(window_height - window_margins))
                else:
                    saved_position = position_str.split('x')
                    x_pos = int(saved_position[0])
                    y_pos = int(saved_position[1])
                print(opened_window, x_pos, y_pos)
                set_window_pos(opened_window, x_pos, y_pos)


def start_gui():
    with window('main', label="If you're reading this you tinkered with the wrong thing."):
        # doesn't apply if you're seeing the source code.
        with menu_bar("Main Menu Bar"):
            with menu("Debug"):
                add_menu_item("About Dear PyGui", callback=show_about)
                add_menu_item("Show Debug", callback=show_debug)
                add_menu_item("Show Dear PyGui Documentation", callback=show_documentation)
                add_menu_item("Show Metrics", callback=show_metrics)
                add_menu_item("Show Logger", callback=show_logger)
            with menu("Themes"):
                add_menu_item("Dark", callback=GuiStuff.theme_callback)
                add_menu_item("Light", callback=GuiStuff.theme_callback)
                add_menu_item("Classic", callback=GuiStuff.theme_callback)
                add_menu_item("Dark 2", callback=GuiStuff.theme_callback)
                add_menu_item("Grey", callback=GuiStuff.theme_callback)
                add_menu_item("Dark Grey", callback=GuiStuff.theme_callback)
                add_menu_item("Cherry", callback=GuiStuff.theme_callback)
                add_menu_item("Purple", callback=GuiStuff.theme_callback)
                add_menu_item("Gold", callback=GuiStuff.theme_callback)
                add_menu_item("Red", callback=GuiStuff.theme_callback)
            with menu("About"):
                add_menu_item("About Drop", callback=GuiStuff.about_drop)

    with window('Rules', no_title_bar=False, autosize=True, no_resize=True, no_close=True, no_move=False,
                y_pos=randint(window_margins, int(window_height - window_margins)),
                x_pos=randint(window_margins, int(window_width - window_margins))):
        add_input_text('rule_guild', label="Guild ID", on_enter=True, callback=Rules.show_rules)
        add_text('Incorrect guild.', color=[255, 0, 0], parent='Rules', show=False)
        add_button('Show rules', callback=Rules.show_rules)

        add_button("Set rule", callback=Rules.do_rule_popup)
        add_same_line(spacing=10)
        add_input_text('Rule Key', on_enter=True, label="", callback=Rules.do_rule_popup)
        add_text('Invalid rule key.', color=[255, 0, 0], parent='Rules', show=False)

    with window('Warns', no_title_bar=False, autosize=True, no_resize=True, no_close=True, no_move=False):
        add_input_text('warn_guild', label="Guild ID")
        add_text("warn_invalid_guild", default_value='Invalid guild ID.', color=[255, 0, 0],
                 parent='Warns', show=False)
        add_spacing(count=2)
        with collapsing_header("Author info", default_open=True):
            add_input_text("warn_author_id", label="Author ID")
            add_input_text("warn_author_name", label="Author name")
        add_spacing(count=1)
        with collapsing_header("User info", default_open=True):
            add_input_text("warn_offender_id", label="Offender ID", on_enter=False, callback=Warns.update_offender_name)
            add_input_text("warn_offender_name", label="Offender name")
        add_text("warn_invalid_offender_id", default_value='Invalid offender ID.', color=[255, 0, 0],
                 parent='Warns', show=False)
        add_spacing(count=2)
        add_input_text('warn_channel', label="Warn channel ID")
        add_input_text('warn_reason', label="Warn reason", height=500)
        add_text("warn_fill_all_the_fucking_fields", default_value='Please fill all of the fields.', color=[255, 0, 0],
                 parent='Warns', show=False)
        # I'm tired, gimme a break.

        add_spacing()
        add_button("Show warns", callback=lambda: Warns.show_warns())
        add_same_line(spacing=5)
        add_button("Add warn", callback=lambda: Warns.add_warn())
        add_text("warn_no_warns", default_value='Offender has no warns', color=[255, 0, 0],
                 parent='Warns', show=False)

    with window('stored_guilds', label='Stored guilds', no_title_bar=False, autosize=True, no_resize=False,
                no_close=True, no_move=False):
        for guild in finder.find_guilds():
            add_text(guild)
            add_button(f"{guild}_show_warns", callback=Guilds.get_warned_users, callback_data=f'{guild}',
                       label="Show all warns")
            add_same_line(spacing=5)
            add_button(f"{guild}_show_rules", callback=Rules.show_rules, callback_data=f'{guild}',
                       label="Show all rules")
            add_spacing(count=1)
        add_text('stored_guilds_text_thingy_i_guess', default_value="I don't have any ideas on how to make this window "
                                                                    "look better.")  # self esteem 100%

    set_exit_callback(GuiStuff.save_window_pos)
    GuiStuff.set_window_pos()
    start_dearpygui(primary_window="main")


if __name__.lower() == '__main__':  # added the .lower() just for fun. ultimately useless at the end of the day.
    start_gui()

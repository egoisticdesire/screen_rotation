def set_dark_theme(radius: int):
    return f'''
        QMenu{{
            font-size: 16px;
            background-color: rgb(26, 26, 26);
            color: rgb(200, 200, 200);
            border: 2px solid rgb(86, 86, 86);
            border-radius: {radius}px;
        }}
        QMenu::item {{
            border-radius: 6px;
            padding: 4px 10px;
            margin: 4px;
            padding-left: 20px;
        }}
        QMenu::icon {{
            padding: 5px 10px;
        }}
        QMenu::item:selected {{
            background-color: rgb(46, 46, 46);
        }}
        QMenu::item:pressed {{
            background-color: rgb(36, 36, 36);
        }}
        QMenu::item:disabled {{
            color: rgb(96, 96, 96);
            background-color: rgb(36, 36, 36);
        }}
        QMenu::separator {{
            margin: 0 10px;
            height: 1px;
            background-color: rgb(46, 46, 46);
        }}
    '''


def set_light_theme(radius: int):
    return f'''
        QMenu{{
            font-size: 16px;
            background-color: rgb(253, 253, 253);
            color: rgb(14, 14, 14);
            border: 2px solid rgb(186, 186, 186);
            border-radius: {radius}px;
        }}
        QMenu::item {{
            border-radius: 6px;
            padding: 4px 10px;
            margin: 3px;
            padding-left: 20px;
        }}
        QMenu::icon {{
            padding: 5px 10px;
        }}
        QMenu::item:selected {{
            background-color: rgb(213, 213, 213);
        }}
        QMenu::item:pressed {{
            background-color: rgb(233, 233, 233);
        }}
        QMenu::item:disabled {{
            color: rgb(136, 136, 136);
            background-color: rgb(233, 233, 233);
        }}
        QMenu::separator {{
            margin: 0 10px;
            height: 1px;
            background-color: rgb(233, 233, 233);
        }}
    '''

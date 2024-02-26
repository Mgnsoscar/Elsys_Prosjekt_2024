import pickle

def dumpStyle(styleVar: str, path: str) -> None:
    with open(path, "wb") as file:
        pickle.dump(styleVar, file)


#dumpStyle(style, "Resources/Stylesheets/comboboxStyle.pkl")


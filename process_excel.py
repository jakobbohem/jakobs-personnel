from pathlib import Path

def main():
    print("here")
    test_file = Path(r"C:\Users\jakobryden\OneDrive - Microsoft\Administration\org_chart_local.xlsx")
    # test_file = Path(r"C:\Users\jakobryden\OneDrive - Microsoft\Administration\example.xlsx")
    sheet_name = "Spicewood Org Chart"
    # sheet_name = "Sheet1"

    # with open test_file

    import pandas as pd

    df = pd.read_excel(test_file, sheet_name=sheet_name)
    print(df) 

if __name__=="__main__":
    main()
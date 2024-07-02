import pandas as pd
import json
import streamlit as st

VERSION = "1.0.1"

generic_layout = {
    "markets_panel_description_name": {
        "en": "Generic Layout",
        "es": "Generic Layout"
    },
    "markets_panel_order_index": 99,
    "markets_panel_groups": ["all"],
    "should_have_panel_view": False,
    "markets": [
        {
            "market_layout_id": "default_generic_layout",
            "market_description_name": {
                "en": "Generic Layout",
                "es": "Generic Layout"
            },
            "columns_sort_by": None,
            "rows_sort_by": "SelectionId",
            "specifier_sort_by_keys": None,
            "column_sort_order": "ASC",
            "row_sort_order": "ASC",
            "market_order_index": 99,
            "selections": None,
            "merge_layout": None
        }
    ]
}


def clean_column_names(df):
    df.columns = df.columns.str.replace('"', '').str.strip()
    return df


def create_json(panel_settings, panel_name, market_settings, market_name, selections_settings, group_order):
    layout = {}
    groups_set = set()

    panel_name_dict = panel_name.set_index('panel_id').to_dict(orient='index')
    market_name_dict = market_name.set_index('market_layout_id').to_dict(orient='index')
    selections_settings_dict = selections_settings.groupby('market_layout_id').apply(
        lambda x: x.to_dict(orient='records')).to_dict()

    for _, panel_row in panel_settings.iterrows():
        panel_id = panel_row['panel_id']
        groups = [group.strip() for group in panel_row['markets_panel_groups'].split(',')]
        groups_set.update(groups)
        layout[str(panel_id)] = {
            "markets_panel_description_name": {
                "en": panel_name_dict[panel_id]['en'],
                "es": panel_name_dict[panel_id]['es']
            },
            "markets_panel_order_index": panel_row['markets_panel_order_index'],
            "markets_panel_groups": groups,
            "should_have_panel_view": panel_row['should_have_panel_view'] if panel_row[
                                                                                 'should_have_panel_view'] is not None else False,
            "markets": []
        }

        for _, market_row in market_settings[
            market_settings['market_layout_id'] == panel_row['market_layout_id']].iterrows():
            market_layout_id = market_row['market_layout_id']
            market_dict = {
                "market_layout_id": str(market_layout_id),
                "market_description_name": {
                    "en": market_name_dict[market_layout_id]['en'],
                    "es": market_name_dict[market_layout_id]['es']
                },
                "columns_sort_by": market_row['columns_sort_by'],
                "rows_sort_by": market_row['rows_sort_by'],
                "specifier_sort_by_keys": market_row['specifier_sort_by_keys'],
                "column_sort_order": market_row['column_sort_order'],
                "row_sort_order": market_row['row_sort_order'],
                "market_order_index": market_row['market_order_index'],
                "selections": []
            }

            for selection in selections_settings_dict[market_layout_id]:
                selection_dict = {
                    "selection_type_id": str(selection['selection_type_id']),
                    "column_index": selection['column_index'],
                    "row_index": selection['row_index'],
                    'row_name': selection['row_name'],
                    "selection_description_name": selection['selection_description_name']
                }
                market_dict['selections'].append(selection_dict)

            layout[str(panel_id)]["markets"].append(market_dict)
        layout["default_generic_layout"] = generic_layout

    # Read the group order from the new sheet
    group_order_list = group_order['group_order'].tolist()

    return {"layout": layout, "groups_order": group_order_list}


def clean_json(data):
    if isinstance(data, dict):
        return {k: clean_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_json(v) for v in data]
    elif pd.isna(data):
        return None
    elif isinstance(data, str) and data.startswith('"') and data.endswith('"'):
        return data[1:-1]
    else:
        return data


def decode_string(s):
    try:
        return s.encode('latin1').decode('utf-8')
    except UnicodeDecodeError:
        return s


def decode_unicode(data):
    if isinstance(data, dict):
        return {k: decode_unicode(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [decode_unicode(v) for v in data]
    elif isinstance(data, str):
        return decode_string(data)
    else:
        return data


def main(file):
    try:
        xls = pd.ExcelFile(file)
        panel_settings = pd.read_excel(xls, 'Panel settings')
        panel_name = pd.read_excel(xls, 'panel name')
        market_settings = pd.read_excel(xls, 'Market settings')
        market_name = pd.read_excel(xls, 'Market name')
        selections_settings = pd.read_excel(xls, 'Selections settings')
        group_order = pd.read_excel(xls, 'Group order')
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None, None, None, None, None

    panel_settings = clean_column_names(panel_settings)
    panel_name = clean_column_names(panel_name)
    market_settings = clean_column_names(market_settings)
    market_name = clean_column_names(market_name)
    selections_settings = clean_column_names(selections_settings)
    group_order = clean_column_names(group_order)

    # Debug: Print column names
    print("Panel Settings Columns:", panel_settings.columns)
    print("Panel Name Columns:", panel_name.columns)
    print("Market Settings Columns:", market_settings.columns)
    print("Market Name Columns:", market_name.columns)
    print("Selections Settings Columns:", selections_settings.columns)
    print("Group Order Columns:", group_order.columns)

    json_result = create_json(panel_settings, panel_name, market_settings, market_name, selections_settings,
                              group_order)
    cleaned_json_result = clean_json(json_result)
    decoded_json_result = decode_unicode(cleaned_json_result)
    decoded_json_str = json.dumps(decoded_json_result, indent=2, ensure_ascii=False)

    return decoded_json_str, panel_settings, market_settings, selections_settings, group_order


st.set_page_config(page_title="Excel to JSON Layouts Converter", page_icon="static/logo.png", layout="centered")
st.logo("static/logo.png")
st.title('Excel to JSON Layouts Converter 📊🔄')

st.write("""
Welcome to the **Excel to JSON Layouts Converter**! This tool allows you to upload an Excel file and convert its content into a JSON structure. 
Simply upload your file, and we'll handle the rest. The conversion process will display a progress spinner, so you'll know when it's done. 
""")
st.write(f"Current version of the script: :green[{VERSION}]")

uploaded_file = st.file_uploader("Choose an Excel file to upload", type="xlsx")

if uploaded_file is not None:
    if st.button('Process File 🚀'):
        with st.spinner('Processing... Please wait ⏳'):
            json_output, panel_settings, market_settings, selections_settings, group_order = main(uploaded_file)
            if json_output:
                st.success('Processing complete! ✅')

                st.subheader('Generated JSON Output:')
                with st.expander("View JSON Output", expanded=False):
                    st.json(json_output, expanded=False)

                st.download_button(label="Download JSON", data=json_output, file_name="output.json",
                                   mime="application/json")

                st.subheader('Metrics')
                st.metric(label="Number of Panels", value=panel_settings['panel_id'].nunique())
                st.metric(label="Number of Markets", value=market_settings['market_layout_id'].nunique())
                st.metric(label="Number of Selections", value=selections_settings['selection_type_id'].nunique())
            else:
                st.error('Error processing the file. Please check the console for details.')

import pandas as pd
import json
import click
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation

# JSON转Excel的函数
def json_to_excel(json_file, excel_file):
    # 读取JSON文件
    with open(json_file, 'r') as f:
        data = json.load(f)

    # 确保data是列表
    if not isinstance(data, list):
        data = [data]

    # 提取主表数据
    main_data_list = []
    for card in data:
        main_data_list.append({
            "牌名称": card["label"],
            "牌组": card["suit"],
            "图片路径": card["image"],
            "3D图片路径": card["image3d"]
        })
    df_main = pd.DataFrame(main_data_list)

    # 提取元素坐标数据
    element_coords = []
    for card in data:
        for element in card["elements"]:
            element_coords.append({
                "牌名称": card["label"],
                "元素名称": element["label"],
                "x": element.get("x"),
                "y": element.get("y"),
                "r": element.get("r")
            })
    df_element_coords = pd.DataFrame(element_coords)

    # 提取元素详情数据
    elements = []
    for card in data:
        for element in card["elements"]:
            for detail in element["details"]:
                elements.append({
                    "牌名称": card["label"],
                    "元素名称": element["label"],
                    "类型": detail["type"],
                    "内容": detail["content"]
                })
    df_elements = pd.DataFrame(elements)

    # 提取正位逆位含义数据
    meanings = []
    for card in data:
        upright = card["meanings"]["upright"]
        reversed_meaning = card["meanings"]["reversed"]
        meanings.append({
            "牌名称": card["label"],
            "类型": "upright",
            "关键词": ", ".join(upright["keywords"]),
            "总结": upright["summary"],
            "含义": upright["meaning"]
        })
        meanings.append({
            "牌名称": card["label"],
            "类型": "reversed",
            "关键词": ", ".join(reversed_meaning["keywords"]),
            "总结": reversed_meaning["summary"],
            "含义": reversed_meaning["meaning"]
        })
    df_meanings = pd.DataFrame(meanings)

    # 提取场景数据
    scenarios = []
    for card in data:
        upright = card["meanings"]["upright"]
        reversed_meaning = card["meanings"]["reversed"]
        for scenario in upright["scenarios"]:
            scenarios.append({
                "牌名称": card["label"],
                "类型": "upright",
                "场景类型": scenario["type"],
                "场景内容": scenario["content"]
            })
        for scenario in reversed_meaning["scenarios"]:
            scenarios.append({
                "牌名称": card["label"],
                "类型": "reversed",
                "场景类型": scenario["type"],
                "场景内容": scenario["content"]
            })
    df_scenarios = pd.DataFrame(scenarios)

    # 写入Excel文件
    with pd.ExcelWriter(excel_file) as writer:
        df_main.to_excel(writer, sheet_name="主表", index=False)
        df_element_coords.to_excel(writer, sheet_name="元素", index=False)
        df_elements.to_excel(writer, sheet_name="元素详情", index=False)
        df_meanings.to_excel(writer, sheet_name="正位逆位含义", index=False)
        df_scenarios.to_excel(writer, sheet_name="场景表", index=False)

    # 添加数据验证约束
    wb = load_workbook(excel_file)

    # 获取所有牌名称用于下拉列表（使用行号范围而不是直接值）
    card_names = df_main["牌名称"].tolist()

    # 获取所有唯一的牌组
    suits = df_main["牌组"].unique().tolist()
    suits_str = ','.join(suits)

    # 主表约束
    ws_main = wb["主表"]
    max_row_main = len(df_main) + 1

    # 牌组：下拉列表
    dv_suit = DataValidation(type="list", formula1=f'"{suits_str}"', allow_blank=False, showErrorMessage=True)
    dv_suit.error = '牌组必须从列表中选择'
    dv_suit.errorTitle = '无效的牌组'
    dv_suit.add(f'B2:B{max_row_main}')
    ws_main.add_data_validation(dv_suit)

    # 元素表约束
    ws_elements = wb["元素"]
    max_row_elem = len(df_element_coords) + 1

    # 牌名称：下拉列表（使用主表的牌名称范围）
    dv_elem_card = DataValidation(type="list", formula1='主表!$A$2:$A$' + str(max_row_main), allow_blank=False, showErrorMessage=True)
    dv_elem_card.error = '牌名称必须从主表选择'
    dv_elem_card.errorTitle = '无效的牌名称'
    dv_elem_card.add(f'A2:A{max_row_elem}')
    ws_elements.add_data_validation(dv_elem_card)

    # x, y, r：数字且在合理范围（0-1000）
    dv_coord = DataValidation(type="whole", operator="between", formula1='0', formula2='1000', allow_blank=True, showErrorMessage=True)
    dv_coord.error = '坐标值必须是0-1000之间的数字'
    dv_coord.errorTitle = '无效的坐标'
    dv_coord.add(f'C2:E{max_row_elem}')
    ws_elements.add_data_validation(dv_coord)

    # 元素详情表约束
    ws_details = wb["元素详情"]
    max_row_details = len(df_elements) + 1

    # 牌名称：下拉列表（使用主表的牌名称范围）
    dv_detail_card = DataValidation(type="list", formula1='主表!$A$2:$A$' + str(max_row_main), allow_blank=False, showErrorMessage=True)
    dv_detail_card.error = '牌名称必须从主表选择'
    dv_detail_card.add(f'A2:A{max_row_details}')
    ws_details.add_data_validation(dv_detail_card)

    # 类型：下拉列表（visual, symbolism, interpretation）
    dv_detail_type = DataValidation(type="list", formula1='"visual,symbolism,interpretation"', allow_blank=False, showErrorMessage=True)
    dv_detail_type.error = '类型必须是：visual、symbolism或interpretation'
    dv_detail_type.errorTitle = '无效的详情类型'
    dv_detail_type.add(f'C2:C{max_row_details}')
    ws_details.add_data_validation(dv_detail_type)

    # 正位逆位含义表约束
    ws_meanings = wb["正位逆位含义"]
    max_row_meanings = len(df_meanings) + 1

    # 牌名称：下拉列表（使用主表的牌名称范围）
    dv_mean_card = DataValidation(type="list", formula1='主表!$A$2:$A$' + str(max_row_main), allow_blank=False, showErrorMessage=True)
    dv_mean_card.error = '牌名称必须从主表选择'
    dv_mean_card.add(f'A2:A{max_row_meanings}')
    ws_meanings.add_data_validation(dv_mean_card)

    # 类型：只能是upright或reversed
    dv_mean_type = DataValidation(type="list", formula1='"upright,reversed"', allow_blank=False, showErrorMessage=True)
    dv_mean_type.error = '类型必须是：upright或reversed'
    dv_mean_type.errorTitle = '无效的含义类型'
    dv_mean_type.add(f'B2:B{max_row_meanings}')
    ws_meanings.add_data_validation(dv_mean_type)

    # 场景表约束
    ws_scenarios = wb["场景表"]
    max_row_scenarios = len(df_scenarios) + 1

    # 牌名称：下拉列表（使用主表的牌名称范围）
    dv_scen_card = DataValidation(type="list", formula1='主表!$A$2:$A$' + str(max_row_main), allow_blank=False, showErrorMessage=True)
    dv_scen_card.error = '牌名称必须从主表选择'
    dv_scen_card.add(f'A2:A{max_row_scenarios}')
    ws_scenarios.add_data_validation(dv_scen_card)

    # 类型：只能是upright或reversed
    dv_scen_type = DataValidation(type="list", formula1='"upright,reversed"', allow_blank=False, showErrorMessage=True)
    dv_scen_type.error = '类型必须是：upright或reversed'
    dv_scen_type.errorTitle = '无效的场景类型'
    dv_scen_type.add(f'B2:B{max_row_scenarios}')
    ws_scenarios.add_data_validation(dv_scen_type)

    wb.save(excel_file)

    return True

# Excel转JSON的函数
def excel_to_json(excel_file, json_file):
    # 读取Excel文件的各表
    df_main = pd.read_excel(excel_file, sheet_name="主表")
    df_element_coords = pd.read_excel(excel_file, sheet_name="元素")
    df_elements = pd.read_excel(excel_file, sheet_name="元素详情")
    df_meanings = pd.read_excel(excel_file, sheet_name="正位逆位含义")
    df_scenarios = pd.read_excel(excel_file, sheet_name="场景表")

    # 转换所有卡片
    cards = []
    main_records = df_main.to_dict(orient="records")

    for main_data in main_records:
        card_name = main_data["牌名称"]

        # 转换元素数据（包含坐标）
        elements = []
        processed_elements = set()
        card_element_coords = df_element_coords[df_element_coords["牌名称"] == card_name]
        card_elements = df_elements[df_elements["牌名称"] == card_name]

        for index, coord_row in card_element_coords.iterrows():
            element_name = coord_row["元素名称"]
            if element_name not in processed_elements:
                element = {
                    "label": element_name,
                    "x": coord_row["x"],
                    "y": coord_row["y"],
                    "r": coord_row["r"],
                    "details": []
                }
                # 查找对应元素的所有详情
                for detail_row in card_elements[card_elements["元素名称"] == element_name].iterrows():
                    element["details"].append({
                        "type": detail_row[1]["类型"],
                        "content": detail_row[1]["内容"]
                    })
                elements.append(element)
                processed_elements.add(element_name)

        # 转换正位逆位含义数据
        card_meanings = df_meanings[df_meanings["牌名称"] == card_name]
        meanings = {
            "upright": {
                "keywords": card_meanings[card_meanings["类型"] == "upright"]["关键词"].values[0].split(", ") if pd.notna(card_meanings[card_meanings["类型"] == "upright"]["关键词"].values[0]) else [],
                "summary": card_meanings[card_meanings["类型"] == "upright"]["总结"].values[0] if pd.notna(card_meanings[card_meanings["类型"] == "upright"]["总结"].values[0]) else "",
                "meaning": card_meanings[card_meanings["类型"] == "upright"]["含义"].values[0] if pd.notna(card_meanings[card_meanings["类型"] == "upright"]["含义"].values[0]) else "",
                "scenarios": []
            },
            "reversed": {
                "keywords": card_meanings[card_meanings["类型"] == "reversed"]["关键词"].values[0].split(", ") if pd.notna(card_meanings[card_meanings["类型"] == "reversed"]["关键词"].values[0]) else [],
                "summary": card_meanings[card_meanings["类型"] == "reversed"]["总结"].values[0] if pd.notna(card_meanings[card_meanings["类型"] == "reversed"]["总结"].values[0]) else "",
                "meaning": card_meanings[card_meanings["类型"] == "reversed"]["含义"].values[0] if pd.notna(card_meanings[card_meanings["类型"] == "reversed"]["含义"].values[0]) else "",
                "scenarios": []
            }
        }

        # 转换场景数据
        card_scenarios = df_scenarios[df_scenarios["牌名称"] == card_name]
        for index, row in card_scenarios.iterrows():
            if row["类型"] == "upright":
                meanings["upright"]["scenarios"].append({
                    "type": row["场景类型"],
                    "content": row["场景内容"]
                })
            else:
                meanings["reversed"]["scenarios"].append({
                    "type": row["场景类型"],
                    "content": row["场景内容"]
                })

        # 构建当前卡片的JSON数据
        json_card = {
            "label": main_data["牌名称"],
            "suit": main_data["牌组"],
            "image": main_data["图片路径"],
            "image3d": main_data["3D图片路径"],
            "elements": elements,
            "meanings": meanings
        }
        cards.append(json_card)

    # 写入JSON文件
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(cards, f, indent=4, ensure_ascii=False)

    return True


# json2excel命令
@click.command(name='json2excel')
@click.option('--input', type=click.Path(exists=True, readable=True), required=True, help='Input JSON file path')
@click.option('--output', type=click.Path(writable=True), required=True, help='Output Excel file path')
def json2excel_cmd(input, output):
    success = json_to_excel(input, output)
    if success:
        click.echo(f"Successfully converted {input} to {output}.")
    else:
        click.echo(f"Failed to convert {input} to {output}.")


# excel2json命令
@click.command(name='excel2json')
@click.option('--input', type=click.Path(exists=True, readable=True), required=True, help='Input Excel file path')
@click.option('--output', type=click.Path(writable=True), required=True, help='Output JSON file path')
def excel2json_cmd(input, output):
    success = excel_to_json(input, output)
    if success:
        click.echo(f"Successfully converted {input} to {output}.")
    else:
        click.echo(f"Failed to convert {input} to {output}.")


# 定义命令组
@click.group()
def cli():
    pass


# 添加命令到命令组
cli.add_command(json2excel_cmd)
cli.add_command(excel2json_cmd)


# 运行
if __name__ == "__main__":
    cli()

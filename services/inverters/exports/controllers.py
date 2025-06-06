from helpers.csv_export import convert_to_csv
from services.inverters.helpers.ai_csv_parse import ai_parser as csv_ai_parser
from helpers.ai_req import gemini_request
from http import HTTPStatus
from services.inverters.helpers.import_data import import_data
from services.inverters.helpers.ai_html_parse import ai_parser as html_ai_parser
from prompts.inverters.parse_txt_prompt import parse_txt_prompt

async def reports_import(file_path, supplier_name, comment):
    csv_report = convert_to_csv(file_path)
    ai_data = csv_ai_parser(csv_report, comment)
    await import_data(ai_data, supplier_name, "supplier")
    return HTTPStatus.OK


async def parse_txt(text, supplier_name, comment):
    prompt = parse_txt_prompt(text, comment)
    ai_data = await gemini_request(prompt)
    await import_data(ai_data, supplier_name, "supplier")
    return HTTPStatus.OK


async def parse_competitors(parse_func, supplier_name):
    html_data = await parse_func()
    ai_data = await html_ai_parser(html_data)
    await import_data(ai_data, supplier_name, "competitor")
    return HTTPStatus.OK

async def parse_my_inverters(parse_func, supplier_name):
    html_data = await parse_func()
    ai_data = await html_ai_parser(html_data)
    await import_data(ai_data, supplier_name, "me")
    return HTTPStatus.OK
    
    

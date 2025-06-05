from fastapi import APIRouter, HTTPException
from fastapi import UploadFile
import os
import tempfile
from helpers.csv_export import convert_to_csv
from services.batteries.exports.controllers import reports_import, parse_txt, parse_my_batteries, parse_competitors
from services.batteries.helpers.competitor import get_competitors_name

from services.batteries.parsers.akum_centr import a_c_parser
from services.batteries.parsers.makb import parse_batteries_makb
from services.batteries.parsers.avto_zvuk import parse_batteries_avto_zvuk
from services.batteries.parsers.shyp_shuna import parse_batteries_shyp_shuna
from services.batteries.parsers.akb_mag import parse_batteries_akb_mag
from services.batteries.parsers.akb_plus import parse_batteries_akb_plus
from services.batteries.parsers.dvi_klemy import parse_batteries_dvi_klemy
from services.batteries.parsers.aku_lviv import parse_batteries_aku_lviv
from services.batteries.parsers.aet_ua import parse_batteries_aet_ua






router = APIRouter(prefix="/upload", tags=["Upload/Export"])


@router.post("/convert_to_csv")
async def upload_batteries_file(
    doc_file: UploadFile | None = None,
    docs_link: str | None = None,
):
    # Визначаємо розширення файлу
    tmp_path = None
    csv_path = None
    if doc_file:
        file_name = doc_file.filename
        suffix = os.path.splitext(file_name)[1]
    
        # Створюємо тимчасовий файл
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        tmp_path = tmp.name
    
        try:
            # Записуємо вміст файлу
            content = await doc_file.read() 
            tmp.write(content)
            tmp.close()  # Закриваємо файл перед подальшою обробкою
            
            # Конвертуємо файл у CSV
            csv_path = convert_to_csv(tmp_path)
            
            # Виводимо вміст CSV файлу
            print("\n--- Вміст CSV файлу ---")
            with open(csv_path, 'r', encoding='utf-8') as f:
                csv_content = f.read()
                print(csv_content)
            print("--- Кінець вмісту CSV файлу ---\n")
            
            return {"detail": "Conversion completed", "csv_file": csv_path}
        finally:
            # Видаляємо тимчасовий файл, якщо він існує
            try:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
            except Exception as e:
                # Якщо не вдалося видалити файл, просто логуємо помилку
                print(f"Не вдалося видалити тимчасовий файл: {str(e)}")
    
    else:
        try:
            # Конвертуємо файл з посилання Google Docs
            csv_path = convert_to_csv(docs_link)
            
            # Виводимо вміст CSV файлу
            print("\n--- Вміст CSV файлу ---")
            with open(csv_path, 'r', encoding='utf-8') as f:
                csv_content = f.read()
                print(csv_content)
            print("--- Кінець вмісту CSV файлу ---\n")
            
            return {"detail": "Conversion completed", "csv_file": csv_path}
        except Exception as e:
            print(f"Помилка при конвертації з Google Docs: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload_reports")
async def upload_batteries_file(
    doc_file: UploadFile | None = None,
    supplier_name: str = "", 
    docs_link: str | None = None,
    comment: str | None = None,
):
    # Визначаємо розширення файлу
    if doc_file:
        file_name = doc_file.filename
        suffix = os.path.splitext(file_name)[1]
    
        # Створюємо тимчасовий файл
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        tmp_path = tmp.name
        csv_path = None
        
        try:
            # Записуємо вміст файлу
            content = await doc_file.read() 
            tmp.write(content)
            tmp.close()  # Закриваємо файл перед подальшою обробкою

            await reports_import(tmp.name, supplier_name, comment)
            return {"detail": "Conversion completed", "csv_file": csv_path}
        except Exception as e:
            # Логуємо помилку для діагностики
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            # Видаляємо тимчасовий файл, якщо він існує
            try:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
            except Exception as e:
                # Якщо не вдалося видалити файл, просто логуємо помилку
                print(f"Не вдалося видалити тимчасовий файл: {str(e)}")
    else:
        await reports_import(docs_link, supplier_name, comment)
        return {"detail": "Conversion completed"}


    

@router.post("/ai_upload/upload_reports_text")
async def upload_batteries_text(
    supplier_name: str,
    text: str,
    comment: str | None = None
):
    await parse_txt(text=text, supplier_name=supplier_name, comment=comment)
    return {"detail": "Import completed"}



@router.post("/parse_competitors")
async def parse_competitors_html():
    func_list =[]
    # func_list.append(parse_batteries_makb)
    func_list.append(parse_batteries_avto_zvuk)
    # func_list.append(parse_batteries_shyp_shuna)
    # func_list.append(parse_batteries_akb_mag)
    # func_list.append(parse_batteries_akb_plus)
    # func_list.append(parse_batteries_dvi_klemy)
    # func_list.append(parse_batteries_aku_lviv)
    # func_list.append(parse_batteries_aet_ua)
    for func in func_list:
        supplier_name = await get_competitors_name(func)
        print(supplier_name)
        await parse_competitors(func, supplier_name)
    return {"detail": "Import completed"}


@router.post("/parse_me")
async def parse_me():
    supplier_name = "Акумулятор центр"
    await parse_my_batteries(a_c_parser, supplier_name)
    return {"detail": "Import completed"}



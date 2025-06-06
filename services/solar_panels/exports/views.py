from fastapi import APIRouter, HTTPException
from fastapi import UploadFile
import os
import tempfile
from services.solar_panels.exports.controllers import reports_import, parse_txt, parse_competitors, parse_my_solar_panels
from services.solar_panels.helpers.competitor import get_competitors_name


from services.solar_panels.parsers import solarflow, friends_solar

router = APIRouter(prefix="/upload", tags=["Upload/Export"])



@router.post("/upload_reports")
async def upload_solar_panels_file(
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
async def upload_solar_panels_text(
    supplier_name: str,
    text: str,
    comment: str | None = None
):
    await parse_txt(text=text, supplier_name=supplier_name, comment=comment)
    return {"detail": "Import completed"}


@router.post("/parse_competitors")
async def parse_competitors_html():
    func_list =[]
    func_list.append(solarflow)
    func_list.append(friends_solar)
    for func in func_list:
        supplier_name = await get_competitors_name(func)
        print(supplier_name)
        await parse_competitors(func, supplier_name)
    return {"detail": "Import completed"}



# @router.post("/parse_me")
# async def parse_me():
#     supplier_name = "Акумулятор центр"
#     await parse_my_solar_panels(a_c_parser, supplier_name)
#     return {"detail": "Import completed"}

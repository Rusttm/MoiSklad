# !!!used SQLAlchemy 2.0.18
from sqlalchemy import create_engine, inspect
from sqlalchemy import Integer, String, JSON, DateTime, func, ARRAY, PickleType
from sqlalchemy import Double, BigInteger, Uuid, Boolean
# from sqlalchemy.dialects.postgresql import JSONB, ARRAY, insert
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import asyncio
import sqlite3
import aiosqlite

from AiogramPackage.TGAlchemy.TGConnSQL import TGConnSQL
__url = TGConnSQL().get_sql_url()
engine = create_async_engine(__url)
session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
	created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
	updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class ModALBaseProd(Base):
	def __init__(self, dictionary=None):
		if dictionary:
			for k, v in dictionary.items():
				setattr(self, k, v)

	__tablename__ = 'product_model'
	position_id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, comment='Обязательное поле для всех таблиц, автоповышение')
	accountId = mapped_column(Uuid, comment='ID учетной записи Обязательное при ответе Только для чтения')
	alcoholic = mapped_column(JSON, comment='Объект, содержащий поля алкогольной продукции. Подробнее тут')
	archived = mapped_column(Boolean, comment='Добавлен ли Товар в архив Обязательное при ответе')
	article = mapped_column(String(255), comment='Артикул')
	# attributes = mapped_column(MutableList.as_mutable(ARRAY(JSON)), comment='Коллекция доп. полей')
	# barcodes = mapped_column(MutableList.as_mutable(ARRAY(JSON)), comment='Штрихкоды Комплекта. Подробнее тут')
	attributes = mapped_column(MutableList.as_mutable(PickleType()), comment='Коллекция доп. полей')
	barcodes = mapped_column(MutableList.as_mutable(PickleType()), comment='Штрихкоды Комплекта. Подробнее тут')
	buyPrice = mapped_column(JSON, comment='Закупочная цена. Подробнее тут')
	code = mapped_column(String(255), comment='Код Товара')
	country = mapped_column(JSON, comment='Метаданные Страны Expand')
	description = mapped_column(String(4096), comment='Описание Товара')
	discountProhibited = mapped_column(Boolean, comment='Признак запрета скидок Обязательное при ответе')
	effectiveVat = mapped_column(BigInteger, comment='Реальный НДС % Только для чтения')
	effectiveVatEnabled = mapped_column(Boolean, comment='Дополнительный признак для определения разграничения реального НДС = 0 или "без НДС". (effectiveVat = 0, effectiveVatEnabled = false) -> "без НДС", (effectiveVat = 0, effectiveVatEnabled = true) -> 0%. Только для чтения')
	externalCode = mapped_column(String(255), comment='Внешний код Товара Обязательное при ответе')
	files = mapped_column(JSON, comment='Метаданные массива Файлов (Максимальное количество файлов - 100) Expand')
	group = mapped_column(JSON, comment='Метаданные отдела сотрудника Обязательное при ответе Expand')

	id = mapped_column(Uuid, unique=True, nullable=False, comment='ID Товара Обязательное при ответе Только для чтения')
	images = mapped_column(JSON,
						   comment='Массив метаданных Изображений (Максимальное количество изображений - 10) Expand')

	isSerialTrackable = mapped_column(Boolean, comment='Учет по серийным номерам. Данная отметка не сочетается с признаками weighed, alcoholic, ppeType, trackingType, onTap.')
	meta = mapped_column(JSON, comment='Метаданные Товара Обязательное при ответе')
	minPrice = mapped_column(JSON, comment='Минимальная цена. Подробнее тут')
	minimumBalance = mapped_column(BigInteger, comment='Неснижаемый остаток')
	name = mapped_column(String(255), comment='Наименование Товара Обязательное при ответе Необходимо при создании')
	owner = mapped_column(JSON, comment='Метаданные владельца (Сотрудника) Expand')
	# packs = mapped_column(MutableList.as_mutable(ARRAY(JSON)), comment='Упаковки Товара. Подробнее тут')
	packs = mapped_column(MutableList.as_mutable(PickleType()), comment='Упаковки Товара. Подробнее тут')
	partialDisposal = mapped_column(Boolean, comment='Управление состоянием частичного выбытия маркированного товара. «true» - возможность включена.')
	pathName = mapped_column(String, comment='Наименование группы, в которую входит Товар Обязательное при ответе Только для чтения')
	paymentItemType = mapped_column(String(255), comment='Признак предмета расчета. Подробнее тут')
	ppeType = mapped_column(String(255), comment='Код вида номенклатурной классификации медицинских средств индивидуальной защиты (EAN-13). Подробнее тут')
	productFolder = mapped_column(JSON, comment='Метаданные группы Товара Expand')
	# salePrices = mapped_column(MutableList.as_mutable(ARRAY(JSON)), comment='Цены продажи. Подробнее тут')
	salePrices = mapped_column(MutableList.as_mutable(PickleType()), comment='Цены продажи. Подробнее тут')

	shared = mapped_column(Boolean, comment='Общий доступ Обязательное при ответе')
	supplier = mapped_column(JSON, comment='Метаданные контрагента-поставщика Expand')
	syncId = mapped_column(Uuid, comment='ID синхронизации Только для чтения Заполнение при создании')
	taxSystem = mapped_column(String(255), comment='Код системы налогообложения. Подробнее тут')
	# things = mapped_column(MutableList.as_mutable(ARRAY(String)), comment='Серийные номера')
	things = mapped_column(MutableList.as_mutable(PickleType()), comment='Серийные номера')
	tnved = mapped_column(String(255), comment='Код ТН ВЭД')
	trackingType = mapped_column(String(255), comment='Тип маркируемой продукции. Подробнее тут')
	uom = mapped_column(JSON, comment='Единицы измерения Expand')
	updated = mapped_column(DateTime, comment='Момент последнего обновления сущности Обязательное при ответе Только для чтения')
	useParentVat = mapped_column(Boolean, comment='Используется ли ставка НДС родительской группы. Если true для единицы ассортимента будет применена ставка, установленная для родительской группы. Обязательное при ответе')
	variantsCount = mapped_column(BigInteger, comment='Количество модификаций у данного товара Обязательное при ответе Только для чтения')
	vat = mapped_column(BigInteger, comment='НДС %')
	vatEnabled = mapped_column(Boolean, comment='Включен ли НДС для товара. С помощью этого флага для товара можно выставлять НДС = 0 или НДС = "без НДС". (vat = 0, vatEnabled = false) -> vat = "без НДС", (vat = 0, vatEnabled = true) -> vat = 0%.')
	volume = mapped_column(BigInteger, comment='Объем')
	weight = mapped_column(BigInteger, comment='Вес')

async def create_db_async():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)

async def drop_db_async():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all())

async def insert_new_row():
	prod = {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/product/019c8e46-a807-11eb-0a80-00ec00080e83", "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/product/metadata", "type": "product", "mediaType": "application/json", "uuidHref": "https://online.moysklad.ru/app/#good/edit?id=019c84fe-a807-11eb-0a80-00ec00080e7d"}, "id": "019c8e46-a807-11eb-0a80-00ec00080e83", "accountId": "e4154b3e-56fa-11eb-0a80-06e200011b76", "owner": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/employee/e430cdb4-56fa-11eb-0a80-079c0026a51d", "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/employee/metadata", "type": "employee", "mediaType": "application/json", "uuidHref": "https://online.moysklad.ru/app/#employee/edit?id=e430cdb4-56fa-11eb-0a80-079c0026a51d"}}, "shared": True, "group": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/group/e415b013-56fa-11eb-0a80-06e200011b77", "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/group/metadata", "type": "group", "mediaType": "application/json"}}, "updated": "2022-03-05 01:13:56.083", "name": "AA33L-Y02A1 Цилиндр с уплотнительными кольцами MT8016LN#102", "description": "AA33L-Y02A1 Цилиндр с уплотнительными кольцами MT8016LN#102", "code": "м77000000000929", "externalCode": "pegSRlphgwfboyZfp5FHB0", "archived": False, "pathName": "Торговый каталог/Запасные части/Запасные части Meite MT8016 NL", "productFolder": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/productfolder/7dac9640-a806-11eb-0a80-01430007cea9", "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/productfolder/metadata", "type": "productfolder", "mediaType": "application/json", "uuidHref": "https://online.moysklad.ru/app/#good/edit?id=7dac9640-a806-11eb-0a80-01430007cea9"}}, "effectiveVat": 20, "effectiveVatEnabled": True, "vat": 20, "vatEnabled": True, "useParentVat": False, "uom": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/uom/19f1edc0-fc42-4001-94cb-c9ec9c62ec10", "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/uom/metadata", "type": "uom", "mediaType": "application/json"}}, "images": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/product/019c8e46-a807-11eb-0a80-00ec00080e83/images", "type": "image", "mediaType": "application/json", "size": 0, "limit": 1000, "offset": 0}}, "minPrice": {"value": 60000.0, "currency": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/currency/e4485ffd-56fa-11eb-0a80-079c0026a562", "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata", "type": "currency", "mediaType": "application/json", "uuidHref": "https://online.moysklad.ru/app/#currency/edit?id=e4485ffd-56fa-11eb-0a80-079c0026a562"}}}, "salePrices": [{"value": 240000.0, "currency": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/currency/e4485ffd-56fa-11eb-0a80-079c0026a562", "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata", "type": "currency", "mediaType": "application/json", "uuidHref": "https://online.moysklad.ru/app/#currency/edit?id=e4485ffd-56fa-11eb-0a80-079c0026a562"}}, "priceType": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/e4492cfd-56fa-11eb-0a80-079c0026a563", "type": "pricetype", "mediaType": "application/json"}, "id": "e4492cfd-56fa-11eb-0a80-079c0026a563", "name": "Цена розн", "externalCode": "cbcf493b-55bc-11d9-848a-00112f43529a"}}, {"value": 0.0, "currency": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/currency/e4485ffd-56fa-11eb-0a80-079c0026a562", "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata", "type": "currency", "mediaType": "application/json", "uuidHref": "https://online.moysklad.ru/app/#currency/edit?id=e4485ffd-56fa-11eb-0a80-079c0026a562"}}, "priceType": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/91ef8b05-570f-11eb-0a80-079c0029e363", "type": "pricetype", "mediaType": "application/json"}, "id": "91ef8b05-570f-11eb-0a80-079c0029e363", "name": "Цена опт", "externalCode": "6b4df01d-572c-4bcd-a72c-44bb568ff7ba"}}, {"value": 0.0, "currency": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/currency/e4485ffd-56fa-11eb-0a80-079c0026a562", "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata", "type": "currency", "mediaType": "application/json", "uuidHref": "https://online.moysklad.ru/app/#currency/edit?id=e4485ffd-56fa-11eb-0a80-079c0026a562"}}, "priceType": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/cdaa9907-69f6-11eb-0a80-0338002d0134", "type": "pricetype", "mediaType": "application/json"}, "id": "cdaa9907-69f6-11eb-0a80-0338002d0134", "name": "Арбен", "externalCode": "1fcaec3a-1980-4bb2-94c7-c3baa8b18c3c"}}, {"value": 0.0, "currency": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/currency/e4485ffd-56fa-11eb-0a80-079c0026a562", "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata", "type": "currency", "mediaType": "application/json", "uuidHref": "https://online.moysklad.ru/app/#currency/edit?id=e4485ffd-56fa-11eb-0a80-079c0026a562"}}, "priceType": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/0f7205d7-7b33-11eb-0a80-08f800068612", "type": "pricetype", "mediaType": "application/json"}, "id": "0f7205d7-7b33-11eb-0a80-08f800068612", "name": "ЭРА", "externalCode": "07b29f4b-8c02-49a6-ad86-4423efc4ff0b"}}, {"value": 0.0, "currency": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/currency/e4485ffd-56fa-11eb-0a80-079c0026a562", "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata", "type": "currency", "mediaType": "application/json", "uuidHref": "https://online.moysklad.ru/app/#currency/edit?id=e4485ffd-56fa-11eb-0a80-079c0026a562"}}, "priceType": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/44b0b82f-d402-11eb-0a80-0ddf000718b0", "type": "pricetype", "mediaType": "application/json"}, "id": "44b0b82f-d402-11eb-0a80-0ddf000718b0", "name": "Сапогова", "externalCode": "e8448e0f-1548-4b36-9075-281ac209f846"}}, {"value": 0.0, "currency": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/currency/e4485ffd-56fa-11eb-0a80-079c0026a562", "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata", "type": "currency", "mediaType": "application/json", "uuidHref": "https://online.moysklad.ru/app/#currency/edit?id=e4485ffd-56fa-11eb-0a80-079c0026a562"}}, "priceType": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/c3fe9017-359c-11ec-0a80-029b00069168", "type": "pricetype", "mediaType": "application/json"}, "id": "c3fe9017-359c-11ec-0a80-029b00069168", "name": "МЕГАСТРОЙ", "externalCode": "183119a1-5c92-4bdf-836e-c1ddf63872e7"}}, {"value": 0.0, "currency": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/currency/e4485ffd-56fa-11eb-0a80-079c0026a562", "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata", "type": "currency", "mediaType": "application/json", "uuidHref": "https://online.moysklad.ru/app/#currency/edit?id=e4485ffd-56fa-11eb-0a80-079c0026a562"}}, "priceType": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/context/companysettings/pricetype/888049bd-aec9-11ee-0a80-117b007a4e00", "type": "pricetype", "mediaType": "application/json"}, "id": "888049bd-aec9-11ee-0a80-117b007a4e00", "name": "Стройгранд", "externalCode": "8b37fe0a-4f4e-42f9-be86-b3eddfc0d133"}}], "buyPrice": {"value": 345.0, "currency": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/currency/eeb95bfd-570b-11eb-0a80-01de0029f5ef", "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata", "type": "currency", "mediaType": "application/json", "uuidHref": "https://online.moysklad.ru/app/#currency/edit?id=eeb95bfd-570b-11eb-0a80-01de0029f5ef"}}}, "barcodes": [{"ean13": "2000000009933"}, {"code128": "AA33L-Y02A1"}], "supplier": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/counterparty/3297017e-5783-11eb-0a80-06ec00b86625", "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/counterparty/metadata", "type": "counterparty", "mediaType": "application/json", "uuidHref": "https://online.moysklad.ru/app/#company/edit?id=3297017e-5783-11eb-0a80-06ec00b86625"}}, "attributes": [{"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/product/metadata/attributes/838b9fcc-859d-11eb-0a80-005a00356e0b", "type": "attributemetadata", "mediaType": "application/json"}, "id": "838b9fcc-859d-11eb-0a80-005a00356e0b", "name": "Производитель", "type": "string", "value": "Meite"}, {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/product/metadata/attributes/3d57e1e2-859e-11eb-0a80-010e0037e03f", "type": "attributemetadata", "mediaType": "application/json"}, "id": "3d57e1e2-859e-11eb-0a80-010e0037e03f", "name": "Модель", "type": "string", "value": "MT8016LN#102"}, {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/product/metadata/attributes/c56db16b-859e-11eb-0a80-005a00359f0d", "type": "attributemetadata", "mediaType": "application/json"}, "id": "c56db16b-859e-11eb-0a80-005a00359f0d", "name": "Код производителя", "type": "string", "value": "AA33L-Y02A1"}, {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/product/metadata/attributes/b0fe8080-859e-11eb-0a80-02b50037a4da", "type": "attributemetadata", "mediaType": "application/json"}, "id": "b0fe8080-859e-11eb-0a80-02b50037a4da", "name": "Категория товара", "type": "string", "value": "Все товары/Строительство и ремонт/Инструменты/Расходные материалы и оснастка/Для пневмоинструмента"}], "paymentItemType": "GOOD", "discountProhibited": False, "country": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/country/fd44cd2e-b398-4222-9c43-f75688bdf327", "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/country/metadata", "type": "country", "mediaType": "application/json", "uuidHref": "https://online.moysklad.ru/app/#country/edit?id=fd44cd2e-b398-4222-9c43-f75688bdf327"}}, "article": "MT8016LN#102", "weight": 0.0, "volume": 0.0, "variantsCount": 0, "isSerialTrackable": False, "trackingType": "NOT_TRACKED", "files": {"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/product/019c8e46-a807-11eb-0a80-00ec00080e83/files", "type": "files", "mediaType": "application/json", "size": 0, "limit": 1000, "offset": 0}}}
	prog_obj = ModALBaseProd(prod)
	print(prog_obj)
	async with session.begin() as s:
		await s.add(prog_obj)
def create_new_table():
	Base.metadata.create_all(engine)

def delete_table():
	Base.metadata.drop_all(engine)

if __name__ == '__main__':
	create_new_table()
	# delete_table()
	# asyncio.run(insert_new_row())

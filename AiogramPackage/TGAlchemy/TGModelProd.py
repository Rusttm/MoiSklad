# !!!used SQLAlchemy 2.0.18
from sqlalchemy import create_engine, inspect
from sqlalchemy import mapped_column, Integer, String, JSON, DateTime, func
from sqlalchemy import Double, BigInteger, Uuid, Boolean
# from sqlalchemy.dialects.postgresql import JSONB, ARRAY, insert
# from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from TGConnSQL import TGConnSQL
__url = TGConnSQL().get_sql_url()
engine = create_engine(__url)

class Base(DeclarativeBase):
	created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
	updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class ModALBaseProd(Base):
	__tablename__ = 'product_model'
	position_id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, comment='Обязательное поле для всех таблиц, автоповышение')
	accountId = mapped_column(Uuid, comment='ID учетной записи Обязательное при ответе Только для чтения')
	alcoholic = mapped_column(JSON, comment='Объект, содержащий поля алкогольной продукции. Подробнее тут')
	archived = mapped_column(Boolean, comment='Добавлен ли Товар в архив Обязательное при ответе')
	article = mapped_column(String(255), comment='Артикул')
	# attributes = mapped_column(MutableList.as_mutable(ARRAY(JSON)), comment='Коллекция доп. полей')
	# barcodes = mapped_column(MutableList.as_mutable(ARRAY(JSON)), comment='Штрихкоды Комплекта. Подробнее тут')
	attributes = mapped_column(MutableList.as_mutable(ARRAY(JSON)), comment='Коллекция доп. полей')
	barcodes = mapped_column(MutableList.as_mutable(ARRAY(JSON)), comment='Штрихкоды Комплекта. Подробнее тут')

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
	packs = mapped_column(MutableList.as_mutable(ARRAY(JSON)), comment='Упаковки Товара. Подробнее тут')
	partialDisposal = mapped_column(Boolean, comment='Управление состоянием частичного выбытия маркированного товара. «true» - возможность включена.')
	pathName = mapped_column(String, comment='Наименование группы, в которую входит Товар Обязательное при ответе Только для чтения')
	paymentItemType = mapped_column(String(255), comment='Признак предмета расчета. Подробнее тут')
	ppeType = mapped_column(String(255), comment='Код вида номенклатурной классификации медицинских средств индивидуальной защиты (EAN-13). Подробнее тут')
	productFolder = mapped_column(JSON, comment='Метаданные группы Товара Expand')
	salePrices = mapped_column(MutableList.as_mutable(ARRAY(JSON)), comment='Цены продажи. Подробнее тут')
	shared = mapped_column(Boolean, comment='Общий доступ Обязательное при ответе')
	supplier = mapped_column(JSON, comment='Метаданные контрагента-поставщика Expand')
	syncId = mapped_column(Uuid, comment='ID синхронизации Только для чтения Заполнение при создании')
	taxSystem = mapped_column(String(255), comment='Код системы налогообложения. Подробнее тут')
	things = mapped_column(MutableList.as_mutable(ARRAY(String)), comment='Серийные номера')
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

def create_new_table():
	Base.metadata.create_all(engine)

def delete_table():
	Base.metadata.drop_all(engine)

if __name__ == '__main__':
	create_new_table()
	# delete_table()

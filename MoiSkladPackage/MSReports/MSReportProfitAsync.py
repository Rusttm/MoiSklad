import datetime

from MoiSkladPackage.MSConnectors.MSMainClass import MSMainClass

import time
import asyncio
from datetime import datetime
import os


class MSReportProfitAsync(MSMainClass):
    """ gather profit report in one dict"""
    logger_name = f"{os.path.basename(__file__)}"
    _main_key = "ms_profit"
    _agent_payments_key = "agent_payments"
    _module_conf_dir = "config"
    _module_conf_file = "ms_profit_config.json"
    _result_bal_columns_key = "result_profit_columns"  # list of result columns
    _module_config = None
    _unknown_dep = "неизвестно"

    def __init__(self):
        super().__init__()
        self._module_config = self.get_json_data_sync(self._module_conf_dir, self._module_conf_file)

    async def get_dep_sales_dict_async(self, from_date: str, to_date: str) -> dict:
        """ result returns
        {'Новосибирск': {'Выручка': 15, 'Себестоимость': 783, 'Валовая прибыль': 77},
            'Саратов': {'Выручка': 53, 'Себестоимость': 42, 'Валовая прибыль': 9},
            'Всего': {'Выручка': 23.58, 'Себестоимость': 12.93, 'Валовая прибыль': 19.6}}
        """
        dep_sum_sales = dict()

        try:
            from MoiSkladPackage.MSReports.MSCustDeptAsync import MSCustDeptAsync
            requester1 = MSCustDeptAsync()
            res_cust_dep = await requester1.get_customers_dep_name_dict_async()
            from MoiSkladPackage.MSReports.MSCustSalesProfitAsync import MSCustSalesProfitAsync
            requester2 = MSCustSalesProfitAsync()
            res_cust_sales = await requester2.get_customers_sales_dict_async(from_date=from_date, to_date=to_date)
            summary_sales = 0
            summary_cost = 0
            summary_profit = 0
            for cust_href, cust_data in res_cust_sales.items():
                dep_name = res_cust_dep.get(cust_href, self._unknown_dep)
                sales = cust_data.get('cust_sales')
                cost = cust_data.get('cust_cost')
                profit = cust_data.get('cust_profit')
                summary_sales += sales
                summary_cost += cost
                summary_profit += profit
                if not dep_sum_sales.get(dep_name, None):
                    dep_sales_dict = dict()
                else:
                    dep_sales_dict = dep_sum_sales.get(dep_name)
                dep_sales_dict = {'Выручка': dep_sales_dict.get('Выручка', 0) + sales,
                                  'Себестоимость': dep_sales_dict.get('Себестоимость', 0) + cost,
                                  'Валовая прибыль': dep_sales_dict.get('Валовая прибыль', 0) + profit}
                dep_sum_sales[dep_name] = dep_sales_dict
            dep_sum_sales["Всего"] = dict({'Выручка': summary_sales,
                                           'Себестоимость': summary_cost,
                                           'Валовая прибыль': summary_profit})
        except Exception as e:
            msg = f"module {__class__.__name__} can't read customers department data, error: {e}"
            self.logger.error(msg)
        return dep_sum_sales

    async def get_handled_dep_sales(self, from_date: str, to_date: str):
        """ handler for agent payments result:
        {'Новосибирск': {'Выручка': 15, 'Себестоимость': 781, 'Валовая прибыль': 7, 'Выплаты Агенту': 97},
        'Саратов': {'Выручка': 5, 'Себестоимость': 21, 'Валовая прибыль': 311},
        'Основной': {'Выручка': 36840.0, 'Себестоимость': 7584.75, 'Валовая прибыль': 2},
        'Москва': {'Выручка': 6, 'Себестоимость': 45, 'Валовая прибыль': 2, 'Выплаты Агенту': 6},
        'Всего': {'Выручка': 23, 'Себестоимость': 12, 'Валовая прибыль': 10, 'Выплаты Агенту': 285}}
        """
        dep_sales = await self.get_dep_sales_dict_async(from_date=from_date, to_date=to_date)
        # get info {'Новосибирск': {'Валовая прибыль': 0.28}, 'Москва': {'Выручка': 0.11}}
        additional_dep_expences = self._module_config.get(self._main_key).get(self._agent_payments_key)

        for department, dep_dict in dep_sales.items():
            agent_payments_dict = additional_dep_expences.get(department, None)
            if agent_payments_dict:
                for key, mult in agent_payments_dict.items():
                    agent_sum = dep_dict.get(key, 0) * mult
                    dep_dict["Выплаты Агенту"] = dep_dict.get("Выплаты Агенту", 0) - agent_sum
                    dep_sales["Всего"]["Выплаты Агенту"] = dep_sales["Всего"].get("Выплаты Агенту", 0) - agent_sum
        # for dep, dep_dict in dep_sales.items():
        #     dep_dict["Отдел"] = dep
        return dep_sales


    async def get_outpayments_dict_async(self, from_date: str, to_date: str):
        """returns dict
        {'date_from': '2024-01-01', 'date_to': '2024-01-31', 'report_type': 'custom',
        'Зарплата': -65.0, 'Перемещение': -50.0}"""
        res_expences_dict = dict()
        try:
            from MoiSkladPackage.MSReports.MSPaymentsAsync import MSPaymentsAsync
            requester3 = MSPaymentsAsync()
            res_expences = await requester3.get_purpose_sum_dict_async(from_date=from_date, to_date=to_date)
            res_expences_dict.update(res_expences.get("date"))
            res_expences_dict.update(res_expences.get("data"))
        except Exception as e:
            msg = f"module {__class__.__name__} can't read expences data, error: {e}"
            self.logger.error(msg)
        return res_expences_dict


if __name__ == "__main__":
    start_time = time.time()
    print(f"report starts at {time.strftime('%H:%M:%S', time.localtime())}")
    connect = MSReportProfitAsync()
    # print(asyncio.run(connect.get_dep_sales_dict_async(from_date="2024-01-01", to_date="2024-01-31")))
    # print(asyncio.run(connect.get_outpayments_dict_async(from_date="2024-01-01", to_date="2024-01-31")))
    print(asyncio.run(connect.get_handled_dep_sales(from_date="2024-01-01", to_date="2024-01-31")))

    print(f"report done in {int(time.time() - start_time)}sec at {time.strftime('%H:%M:%S', time.localtime())}")

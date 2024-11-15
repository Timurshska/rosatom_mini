from typing import Tuple, Set, List, Dict
import ast
import argparse
import pandas as pd
import numpy as np

using_chars = False
COLUMNS = ["file_path", "product_name"]
if using_chars:
    COLUMNS.append("characteristics")


class MetricsMeter:
    def __init__(self):
        self.tp = 0
        self.fp = 0
        self.fn = 0

    def update(self, values: Tuple[float, float, float]):
        self.tp += values[0]
        self.fp += values[1]
        self.fn += values[2]


class ProductCharMetric:
    def __init__(self, predict_file_path: str, test_file_path: str):
        self.predict_df = self.read_file(predict_file_path)
        self.test_df = self.read_file(test_file_path)
        # if not using_chars:
        #     self.test_df.drop(columns=[self.test_df.columns[-1]], inplace=True)
        self.process_frames()
        self.count_metrics()

    @staticmethod
    def read_file(path: str) -> pd.DataFrame:
        df = pd.read_excel(path)
        return df

    def initialize_metrics_values(self):
        self.products_metrics = MetricsMeter()
        self.chars_metrics = MetricsMeter()

    def count_metrics(self) -> Tuple:
        self.initialize_metrics_values()
        for file_name in self.file_names:
            self.metrics_for_file(file_name)

    def process_frames(self):
        assert len(self.predict_df.columns) == len(
            self.test_df.columns
        ), f"The number of columns in predict {len(self.predict_df.columns)}  file differ from number of columns in test file  {len(self.test_df.columns)} :("
        self.predict_df.columns = COLUMNS
        self.test_df.columns = COLUMNS
        if using_chars:
            self.predict_df.characteristics = self.predict_df.characteristics.apply(
                lambda x: tuple(ast.literal_eval(x)) if not pd.isnull(x) else None
            )
            self.test_df.characteristics = self.test_df.characteristics.apply(
                lambda x: tuple(ast.literal_eval(x)) if not pd.isnull(x) else None
            )
        test_files = sorted(self.test_df.file_path.unique().tolist())
        predict_files = sorted(self.predict_df.file_path.unique().tolist())
        self.file_names = test_files

    def metrics_for_file(self, file_name: str):
        temp_predict = self.predict_df[self.predict_df.file_path == file_name]
        temp_test = self.test_df[self.test_df.file_path == file_name]

        file_predict_product_names = set(temp_predict.product_name)
        file_test_product_names = set(temp_test.product_name)
        products_metric_values = self.metrics_for_file_products(
            file_predict_product_names, file_test_product_names
        )
        self.products_metrics.update(products_metric_values)
        if using_chars:
            for product_name in file_test_product_names:
                product_predict_df = temp_predict[temp_predict.product_name == product_name]
                product_test_df = temp_test[temp_test.product_name == product_name]
                product_char_metric_values = self.metrics_for_product_char(
                    product_predict_df, product_test_df
                )
                self.chars_metrics.update(product_char_metric_values)

    @staticmethod
    def metrics_for_file_products(
        file_predict_product_names: Set[str], file_test_product_names: Set[str]
    ) -> Tuple[float, float, float]:
        file_products_tp = len(
            file_predict_product_names.intersection(file_test_product_names)
        )
        file_products_fp = len(file_predict_product_names - file_test_product_names)
        file_products_fn = len(file_test_product_names - file_predict_product_names)
        return file_products_tp, file_products_fp, file_products_fn

    @staticmethod
    def metrics_for_product_char(
        product_predict_df: pd.DataFrame, product_test_df: pd.DataFrame
    ) -> Tuple[float, float, float]:
        if product_predict_df.empty:
            return 0, 0, 0
        product_predict_dict = product_predict_df.iloc[0].to_dict()
        product_test_dict = product_test_df.iloc[0].to_dict()

        predict_chars = set(product_predict_dict["characteristics"])
        test_chars = set(product_test_dict["characteristics"])
        chars_tp = len(test_chars.intersection(predict_chars))
        chars_fp = len(predict_chars - test_chars)
        chars_fn = len(test_chars - predict_chars)
        return chars_tp, chars_fp, chars_fn

    @staticmethod
    def count_precision_recal_f1(
        metric_meter: MetricsMeter,
    ) -> Tuple[float, float, float]:
        if (not metric_meter.tp) and (not metric_meter.fp):
            precision = 0
        else:
            precision = round(metric_meter.tp / (metric_meter.tp + metric_meter.fp), 3)

        if (not metric_meter.tp) and (not metric_meter.fn):
            recall = 0
        else:
            recall = round(metric_meter.tp / (metric_meter.tp + metric_meter.fn), 3)

        if (not precision) and (not recall):
            f1_score = 0
        else:
            f1_score = round(2 * precision * recall / (precision + recall), 3)
        return precision, recall, f1_score

    def get_metrics(self, type: str = "product") -> Tuple[float, float, float]:
        metrics_meter = (
            self.products_metrics if type == "product" else self.chars_metrics
        )
        precision, recall, f1_score = self.count_precision_recal_f1(metrics_meter)
        return precision, recall, f1_score



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-tf", "--test_file", required=True)
    parser.add_argument("-pf", "--pred_file", required=True)
    args = parser.parse_args()

    metric_class = ProductCharMetric(args.pred_file, args.test_file)
    product_metric = metric_class.get_metrics(type="product")
    print(f"Precision, recall, f1 for products: {product_metric}")
    if using_chars:
        chars_metric = metric_class.get_metrics(type="chars")
        print(f"Precision, recall, f1 for chars: {chars_metric}")


if __name__ == "__main__":
    main()


# python metric.py -tf data/размеченный.xlsx -pf prompt_experiments/final_test_data_to_metrics.xlsx
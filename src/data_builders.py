from dataclasses import dataclass
from pathlib import Path
import csv
from datetime import datetime


@dataclass
class RawCSV:
    fields: list
    rows: list


class CsvBuilder:
    @staticmethod
    def Build(data: RawCSV, out_name: str = "data", out_dir: Path = Path("../out")):
        """
        Create csv file from raw data
        :param data:
        :param out_name: file name
        :param out_dir: file directory
        :return:
        """
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        path = Path(out_dir / f"{out_name}_{current_time}.csv")
        with open(path, 'w+', newline='') as file:
            writer = csv.writer(file)
            field = data.fields

            writer.writerow(field)
            for row in data.rows:
                writer.writerow(row)
        print(f"[+]Build new CSV {path.absolute()}")


if __name__ == "__main__":
    csv_data = RawCSV(fields=["name", "age", "country"], rows=[["Oladele Damilola", "40", "Nigeria"],
                                                          ["Alina Hricko", "23", "Ukraine"],
                                                          ["Isabel Walter", "50", "United Kingdom"]])
    CsvBuilder.Build(csv_data)

from src.parsers import PeopleCard
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
    def Build_CSV(data: RawCSV, out_name: str = "data", out_dir: Path = Path("./out"), time_stamp: bool = False):
        """
        Create csv file from raw data
        :param data:
        :param out_name: file name
        :param out_dir: file directory
        :param time_stamp: use time stamp on out file or no
        :return:
        """
        if time_stamp:
            current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            path = Path(out_dir / f"{out_name}_{current_time}.csv")
        else:
            path = Path(out_dir / f"{out_name}.csv")

        with open(path.absolute(), 'w+', newline='') as file:
            writer = csv.writer(file)
            field = data.fields

            writer.writerow(field)
            for row in data.rows:
                writer.writerow(row)
        print(f"[+]Build new CSV {path.absolute()}")


class PeopleCardsBuilder:
    __DefaultOutName = "dump"
    __DefaultOutDir = Path("./out")
    __UseTimeStamps = True

    def __init__(self, cards: [PeopleCard]):
        self.__cards = cards

    def __build_personal_datas(self, out_name: str = __DefaultOutName, out_dir: Path = __DefaultOutDir,
                               time_stamp: bool = __UseTimeStamps):
        out_name = "personal_data_" + out_name
        fields = ["ID", "Last_Name", "First_Name", "Middle_Name", "Gender", "Birth_Date", "Birth_Place", "Citizenship",
                  "Notes"]
        rows = []
        for card in self.__cards:
            pid = card.Id
            pd = card.PersonalData
            row = [pid, pd.last_name, pd.first_name, pd.middle_name, str(pd.gender), str(pd.birth_date),
                   pd.birth_place, str(pd.citizenship), pd.notes]
            rows.append(row)
        raw_csv = RawCSV(fields, rows)

        CsvBuilder.Build_CSV(raw_csv, out_name=out_name, out_dir=out_dir, time_stamp=time_stamp)

    def __build_document_datas(self, out_name: str = __DefaultOutName, out_dir: Path = __DefaultOutDir,
                               time_stamp: bool = __UseTimeStamps):
        out_name = "document_data_" + out_name
        fields = ["ID", "SNILS", "VISA", "B_Series", "B_Number", "B_IssuedBy", "B_IssuedDate", "B_IssuedPlace",
                  "B_ActNumber", "P_Series", "P_Number", "P_IssuedBy", "P_IssuedDate", "P_IssuedPlace"]
        rows = []
        for card in self.__cards:
            pid = card.Id
            doc = card.Document
            bcert = doc.birth_certificate
            pas = doc.passport
            row = [pid, doc.snils, doc.visa, bcert.series, bcert.number, bcert.issued_by, str(bcert.issued_date),
                   bcert.issued_place, bcert.act_number, pas.series, pas.number, pas.issued_by,
                   str(pas.issued_date), pas.issued_place]

            rows.append(row)
        raw_csv = RawCSV(fields, rows)

        CsvBuilder.Build_CSV(raw_csv, out_name=out_name, out_dir=out_dir, time_stamp=time_stamp)

    def __build_contact_datas(self, out_name: str = __DefaultOutName, out_dir: Path = __DefaultOutDir,
                              time_stamp: bool = __UseTimeStamps):
        out_name = "contact_data_" + out_name
        fields = ["ID", "Permanent_Address", "Temporary_Address", "Temporary_Address_End_Date", "Fact_Address",
                  "Email", "Work_Phone", "Mobile_Phone", "Home_Phone"]

        rows = []
        for card in self.__cards:
            pid = card.Id
            cd = card.ContactData
            row = [pid, cd.permanent_address, cd.temporary_address, str(cd.temporary_address_end_date),
                   cd.fact_address, cd.email, cd.work_phone, cd.mobile_phone, cd.home_phone]
            rows.append(row)

        raw_csv = RawCSV(fields, rows)

        CsvBuilder.Build_CSV(raw_csv, out_name=out_name, out_dir=out_dir, time_stamp=time_stamp)

    def __build_worker_datas(self, out_name: str = __DefaultOutName, out_dir: Path = __DefaultOutDir,
                             time_stamp: bool = __UseTimeStamps):
        out_name = "worker_data_" + out_name

        fields = ["ID", "Work_Start_Date", "Work_End_Date", "Teacher_Start_Date"]
        rows = []
        for card in self.__cards:
            pid = card.Id
            wd = card.WorkerData
            row = [pid, str(wd.work_start_date), str(wd.work_end_date), str(wd.teacher_start_date)]
            rows.append(row)

        raw_csv = RawCSV(fields, rows)

        CsvBuilder.Build_CSV(raw_csv, out_name=out_name, out_dir=out_dir, time_stamp=time_stamp)

    def Build(self, out_name: str = __DefaultOutName, out_dir: Path = __DefaultOutDir,
              time_stamp: bool = __UseTimeStamps):

        self.__build_personal_datas(out_name, out_dir, time_stamp)
        self.__build_document_datas(out_name, out_dir, time_stamp)
        self.__build_contact_datas(out_name, out_dir, time_stamp)
        self.__build_worker_datas(out_name, out_dir, time_stamp)


if __name__ == "__main__":
    csv_data = RawCSV(fields=["name", "age", "country"], rows=[["Oladele Damilola", "40", "Nigeria"],
                                                               ["Alina Hricko", "23", "Ukraine"],
                                                               ["Isabel Walter", "50", "United Kingdom"]])
    CsvBuilder.Build_CSV(csv_data)

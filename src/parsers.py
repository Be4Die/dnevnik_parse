from src.core_driver import PeopleCardWebElement
from src.data_providers import XPathsProvider, WebServices
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from dataclasses import dataclass
from enum import Enum
from datetime import date


class Gender(Enum):
    Male = 0
    Female = 1


class Citizenship(Enum):
    Undefined = "Укажите тип гражданства"
    CitizenOfRussianFederation = "Гражданин Российской Федерации"
    ForeignCitizen = "Иностранный гражданин"
    StatelessPerson = "Лицо без гражданства"
    CitizenOfRussianFederationAndForeign = "Гражданин Российской Федерации и иностранного государства"


@dataclass
class BirthCertificate:
    series: str
    number: str
    issued_by: str
    issued_date: date
    issued_place: str
    act_number: str


@dataclass
class Passport:
    series: str
    number: str
    issued_by: str
    issued_date: date
    issued_place: str


@dataclass
class PersonalData:
    last_name: str
    first_name: str
    middle_name: str
    gender: Gender
    birth_date: date
    birth_place: str
    citizenship: Citizenship
    notes: str


@dataclass
class ParentData(PersonalData):
    work_place: str
    work_position: str


@dataclass
class Document:
    snils: str
    visa: str
    birth_certificate: BirthCertificate
    passport: Passport


@dataclass
class ContactData:
    permanent_address: str
    temporary_address: str
    temporary_address_end_date: date
    fact_address: str
    email: str
    work_phone: str
    mobile_phone: str
    home_phone: str


@dataclass
class WorkerData:
    work_start_date: date
    work_end_date: date
    teacher_start_date: date


class PeopleCard:
    def __init__(self, person_id: int, personal_data: PersonalData, document: Document, contact_data: ContactData,
                 worker_data: WorkerData = None):
        self.Id = person_id
        self.PersonalData = personal_data
        self.Document = document
        self.ContactData = contact_data
        self.WorkerData = worker_data


def __dateConvert(raw_date: str) -> date:
    split_date = raw_date.split('.')
    if len(split_date) == 3:
        return date(int(split_date[2]), int(split_date[1]), int(split_date[0]))
    else:
        return date.min


def __build_personal_data(element: WebElement, xpaths: dict) -> PersonalData:
    _last_name = ''
    _first_name = ''
    _middle_name = ''
    _gender = Gender.Female
    _birth_date = date.min
    _birth_place = ''
    _citizenship = Citizenship.Undefined
    _notes = ''
    try:
        _last_name = element.find_element(By.XPATH, xpaths["last_name"]).get_attribute("value")
        _first_name = element.find_element(By.XPATH, xpaths["first_name"]).get_attribute("value")

        _middle_name = element.find_element(By.XPATH, xpaths["middle_name"]).get_attribute("value")
        sexM = element.find_element(By.XPATH, (xpaths["sexM"]))
        _gender = Gender.Male if sexM.get_attribute("checked") == "checked" else Gender.Female
        _birth_date = __dateConvert(element.find_element(By.XPATH, xpaths["birth_date"]).get_attribute("value"))

        _birth_place = element.find_element(By.XPATH, xpaths["birth_place"]).get_attribute("value")

        _citizenship = Citizenship.Undefined  # TODO: add parse citizenship
        _notes = element.find_element(By.XPATH, xpaths["notes"]).text

    except NoSuchElementException:
        pass

    return PersonalData(last_name=_last_name, first_name=_first_name, middle_name=_middle_name,
                        gender=_gender, birth_date=_birth_date, birth_place=_birth_place,
                        citizenship=_citizenship, notes=_notes)


def __build_birth_certificate(element: WebElement, xpaths: dict) -> BirthCertificate:
    _series = ''
    _number = ''
    _issued_by = ''
    _issued_date = date.min
    _issued_place = ''
    _act_number = ''
    try:
        _series = element.find_element(By.XPATH, xpaths["series"]).get_attribute("value")
        _number = element.find_element(By.XPATH, xpaths["number"]).get_attribute("value")
        _issued_by = element.find_element(By.XPATH, xpaths["issued_by"]).get_attribute("value")
        _issued_date = __dateConvert(element.find_element(By.XPATH, xpaths["issued_date"]).get_attribute("value"))
        _issued_place = element.find_element(By.XPATH, xpaths["issued_place"]).get_attribute("value")
        _act_number = element.find_element(By.XPATH, xpaths["act_number"]).get_attribute("value")
    except NoSuchElementException:
        pass
    return BirthCertificate(series=_series, number=_number, issued_by=_issued_by, issued_date=_issued_date,
                            issued_place=_issued_place, act_number=_act_number)


def __build_passport(element: WebElement, xpaths: dict) -> Passport:
    _series = ''
    _number = ''
    _issued_by = ''
    _issued_date = date.min
    _issued_place = ''
    try:
        _series = element.find_element(By.XPATH, xpaths["series"]).get_attribute("value")
        _number = element.find_element(By.XPATH, xpaths["number"]).get_attribute("value")
        _issued_by = element.find_element(By.XPATH, xpaths["issued_by"]).get_attribute("value")
        _issued_date = __dateConvert(element.find_element(By.XPATH, xpaths["issued_date"]).get_attribute("value"))
        _issued_place = element.find_element(By.XPATH, xpaths["issued_place"]).get_attribute("value")
    except NoSuchElementException:
        pass
    return Passport(series=_series, number=_number, issued_by=_issued_by,
                    issued_date=_issued_date, issued_place=_issued_place)


def __build_document(element: WebElement, xpaths: dict) -> Document:
    _snils = ''
    _visa = ''
    _birth_certificate = __build_birth_certificate(element, xpaths["birth_certificate_xpaths"])
    _passport = __build_passport(element, xpaths["passport_xpaths"])
    try:
        _snils = element.find_element(By.XPATH, xpaths["snils"]).get_attribute("value")
        _visa = element.find_element(By.XPATH, xpaths["visa"]).get_attribute("value")
    except NoSuchElementException:
        pass

    return Document(snils=_snils, visa=_visa, birth_certificate=_birth_certificate, passport=_passport)


def __build_contact_data(element: WebElement, xpaths: dict) -> ContactData:
    _permanent_address = ''
    _temporary_address = ''
    _temporary_address_end_date = date.min
    _fact_address = ''
    _email = ''
    _work_phone = ''
    _mobile_phone = ''
    _home_phone = ''

    try:
        _permanent_address = element.find_element(By.XPATH, xpaths["permanent_address"]).get_attribute("value")
        _temporary_address = element.find_element(By.XPATH, xpaths["temporary_address"]).get_attribute("value"),
        _temporary_address_end_date = __dateConvert(element.find_element(By.XPATH, xpaths["temporary_address_end_date"])
                                                    .get_attribute("value")),
        _fact_address = element.find_element(By.XPATH, xpaths["fact_address"]).get_attribute("value"),
        _email = element.find_element(By.XPATH, xpaths["email"]).get_attribute("value"),
        _work_phone = element.find_element(By.XPATH, xpaths["work_phone"]).get_attribute("value"),
        _mobile_phone = element.find_element(By.XPATH, xpaths["mobile_phone"]).get_attribute("value"),
        _home_phone = element.find_element(By.XPATH, xpaths["home_phone"]).get_attribute("value")
    except NoSuchElementException:
        pass

    return ContactData(permanent_address=_permanent_address, temporary_address=_temporary_address,
                       temporary_address_end_date=_temporary_address_end_date, fact_address=_fact_address,
                       email=_email, work_phone=_work_phone, mobile_phone=_mobile_phone, home_phone=_home_phone)


def __build_worker_data(element: WebElement, xpaths: dict) -> WorkerData:
    _work_start_date = date.min
    _work_end_date = date.min
    _teacher_start_date = date.min

    try:
        _work_start_date = __dateConvert(element.find_element(By.XPATH, xpaths["work_start_date"])
                                         .get_attribute("value"))
        _work_end_date = __dateConvert(element.find_element(By.XPATH, xpaths["work_end_date"]).get_attribute("value"))
        _teacher_start_date = __dateConvert(element.find_element(By.XPATH, xpaths["teacher_start_date"])
                                            .get_attribute("value"))
    except NoSuchElementException:
        pass

    return WorkerData(work_start_date=_work_start_date, work_end_date=_work_end_date,
                      teacher_start_date=_teacher_start_date)


def ParsePeopleCard(card: PeopleCardWebElement, xpaths_provider: XPathsProvider) -> PeopleCard:
    dnevnik_xpaths = xpaths_provider.get(WebServices.Dnevnik)

    pdata = __build_personal_data(card.personal_data, dnevnik_xpaths["personal_data_xpaths"])
    doc = __build_document(card.document, dnevnik_xpaths["document_xpaths"])
    cdata = __build_contact_data(card.contact_data, dnevnik_xpaths["contact_data_xpaths"])
    wdata = __build_worker_data(card.worker_data, dnevnik_xpaths["worker_data_xpaths"])

    people_card = PeopleCard(person_id=card.person_id, personal_data=pdata, document=doc, contact_data=cdata, worker_data=wdata)

    return people_card

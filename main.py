from src.core_driver import CoreDriver
from src.parsers import ParsePeopleCard
from src.data_builders import PeopleCardsBuilder

if __name__ == "__main__":
    driver = CoreDriver(click_delay=1, loading_delay=4)

    driver.Login()
    raw_data = driver.Parse_current_peoples(debug=True)
    cards = [ParsePeopleCard(card, driver.XPathsProvider) for card in raw_data]
    builder = PeopleCardsBuilder(cards)
    builder.Build()


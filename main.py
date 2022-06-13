from Interface import Interface
from Organizer import Organizer

def main():
    interface = Interface()
    interface.interface()
    while interface.region == '':
        pass
    org = Organizer()
    org.get_report(interface.region, interface.country, interface.year_current, interface.year_current - 1)


if __name__ == "__main__":
    main()
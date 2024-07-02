#include <iostream>
#include <fstream>

int main() {
    std::cout << "Hello World!";
    // Utworzenie obiektu ofstream o nazwie "plik" i otwarcie pliku o nazwie "plik.txt" w trybie zapisu
    std::ofstream plik("plik.txt");

    // Sprawdzenie, czy plik został otwarty pomyślnie
    if (plik.is_open()) {
        // Zapisanie tekstu "Hello World!" do pliku
        plik << "Hello World!";

        // Zamknięcie pliku
        plik.close();

        std::cout << "Tekst został zapisany w pliku plik.txt" << std::endl;
    } else {
        std::cout << "Nie udało się otworzyć pliku" << std::endl;
    }

    return 0;
}
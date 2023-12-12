#include <iostream>
#include <vector>
#include <map>
#include <algorithm>
#include <random>

class SlotMachine {
private:
    const int ROWS = 3;
    const int COLS = 3;

    std::map<char, int> symbolCount;
    std::map<char, int> symbolValue;

public:
    SlotMachine() {
        symbolCount['A'] = 2;
        symbolCount['B'] = 4;
        symbolCount['C'] = 6;
        symbolCount['D'] = 8;

        symbolValue['A'] = 5;
        symbolValue['B'] = 4;
        symbolValue['C'] = 3;
        symbolValue['D'] = 2;
    }

    double spin(double balance);
    void print() const;

private:
    std::vector<std::vector<char>> getSpinResult() const;
    std::pair<double, std::vector<int>> checkWinnings(const std::vector<std::vector<char>>& columns, double bet) const;
    void nudgeColumns(std::vector<std::vector<char>>& columns, double& balance, double bet);
};

double SlotMachine::spin(double balance) {
    double bet = 0.25; // default bet
    double totalBet = bet * 1;

    if (totalBet > balance) {
        std::cout << "You do not have enough to bet that amount, your current balance is: £" << balance << std::endl;
        return balance;
    } else {
        std::cout << "You are betting £" << bet << " on 1 line. Total bet is equal to: £" << totalBet << std::endl;
    }

    auto slots = getSpinResult();
    print();

    auto [winnings, winningLines] = checkWinnings(slots, bet);
    if (winnings > 0) {
        std::cout << "You won £" << winnings << "." << std::endl;
        balance += winnings;  // Add the winnings to the balance
    } else {
        std::cout << "Sorry, you didn't win this time." << std::endl;
    }

    // Deduct the total bet amount from the balance
    balance -= totalBet;

    nudgeColumns(slots, balance, bet);

    return balance;
}

void SlotMachine::print() const {
    std::cout << "Slot Machine Result:" << std::endl;
    for (int row = 0; row < ROWS; ++row) {
        for (int col = 0; col < COLS; ++col) {
            std::cout << columns[col][row];
            if (col < COLS - 1) {
                std::cout << " | ";
            }
        }
        std::cout << std::endl;
    }
}

std::vector<std::vector<char>> SlotMachine::getSpinResult() const {
    std::vector<std::vector<char>> columns;

    for (int i = 0; i < COLS; ++i) {
        std::vector<char> column;
        std::vector<char> currentSymbols;

        for (int j = 0; j < ROWS; ++j) {
            currentSymbols.push_back(symbolCount.begin()->first);
        }

        std::random_shuffle(currentSymbols.begin(), currentSymbols.end());

        for (int j = 0; j < ROWS; ++j) {
            column.push_back(currentSymbols[j]);
        }

        columns.push_back(column);
    }

    return columns;
}

std::pair<double, std::vector<int>> SlotMachine::checkWinnings(const std::vector<std::vector<char>>& columns, double bet) const {
    double winnings = 0.0;
    std::vector<int> winningLines;

    // Get the symbols in the middle row of each column
    std::vector<char> middleRowSymbols;
    for (const auto& column : columns) {
        middleRowSymbols.push_back(column[column.size() / 2]);
    }

    // Check if all symbols in the middle row are the same
    if (std::set<char>(middleRowSymbols.begin(), middleRowSymbols.end()).size() == 1) {
        char symbol = middleRowSymbols[0];
        winnings += symbolValue.at(symbol) * bet;
        winningLines.push_back(columns.size() / 2 + 1);
    }

    return std::make_pair(winnings, winningLines);
}

void SlotMachine::nudgeColumns(std::vector<std::vector<char>>& columns, double& balance, double bet) {
    int nudgeCount = 0;
    double winnings = 0.0;

    while (nudgeCount < 2) {
        std::cout << "Choose a column to nudge (1, 2, or 3) or press Enter to spin again, or 'e' to exit: ";
        std::string nudgeChoice;
        std::cin >> nudgeChoice;

        if (nudgeChoice == "") {
            // Allow for a new spin if Enter is pressed
            columns = getSpinResult();
            print();

            auto [winnings, winningLines] = checkWinnings(columns, bet);
            if (winnings > 0) {
                std::cout << "You won £" << winnings << "." << std::endl;
                balance += winnings;
            } else {
                std::cout << "Sorry, you didn't win this time." << std::endl;
            }
            break;
        } else if (nudgeChoice == "e") {
            // Exit the game
            break;
        } else if (nudgeChoice == "1" || nudgeChoice == "2" || nudgeChoice == "3") {
            int columnToNudge = std::stoi(nudgeChoice);
            columns[columnToNudge - 1] = getSpinResult()[0];
            print();

            auto [winnings, winningLines] = checkWinnings(columns, bet);
            if (winnings > 0) {
                std::cout << "You won £" << winnings << "." << std::endl;
                balance += winnings;
            } else {
                std::cout << "Sorry, you didn't win this time." << std::endl;
            }

            // Deduct the total bet amount from the balance
            balance -= bet;

            nudgeCount++;
        } else {
            std::cout << "Invalid choice. Press Enter to spin again, 'e' to exit, or choose a column to nudge (1, 2, or 3)." << std::endl;
        }
    }
}

int main() {
    double balance;
    std::cout << "What would you like to deposit? (Max Deposit: £50): £";
    std::cin >> balance;

    SlotMachine slotMachine;

    while (true) {
        std::cout << "Current balance is £" << balance << std::endl;
        std::cout << "Press 's' to Spin, 'e' to Exit: ";
        std::string choice;
        std::cin >> choice;

        if (choice == "e") {
            std::cout << "You left with £" << balance << std::endl;
            break;
        } else if (choice == "s") {
            balance = slotMachine.spin(balance);
        } else {
            std::cout << "Invalid choice. Press 's' to Spin or 'e' to Exit." << std::endl;
        }
    }

    return 0;
}

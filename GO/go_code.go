package main

import (
	"fmt"
	"math/rand"
	"time"
)

type Player struct {
	balance float64
}

// Define a function called "NewPlayer" that returns a pointer to a Player struct
func NewPlayer() *Player {
	return &Player{
		balance: 10.0,
	}
}

// Define a function called "deductBalance" that takes in a float64 and returns a float64
func (p *Player) getBalance() float64 {
	return p.balance
}

// Define a function called "deductBalance" that takes in a float64 and returns a float64
func (p *Player) setBalance(newBalance float64) {
	p.balance = newBalance
}

// Define an interface called "SlotMachine"
type SlotMachine interface {
	PrintSlotMachine(columns [][]rune)
	getSlotMachineSpin(rows, cols int, symbolCount map[rune]int) func(*Player) [][]rune
	checkWinnings(matrix [][]rune, bet int, values map[rune]int, player *Player) (int, string, error)
}

// Define a struct called "NormalMachine"
type NormalMachine struct{}

const rowSmall = 3
const colSmall = 3
const bet int = 1

var symbol_count = map[rune]int{
	'A': 2,
	'B': 4,
	'C': 6,
	'D': 8,
}

var symbol_value = map[rune]int{
	'A': 5,
	'B': 4,
	'C': 3,
	'D': 2,
}

// Define a struct called "JackPot"
type JackPot struct{}

const rowLarge = 5
const colLarge = 5

var symbol_count_large = map[rune]int{
	'&': 16,
	'$': 6,
	'*': 1,
}

var symbol_value_large = map[rune]int{
	'&': 50,
	'$': 25,
	'*': 10,
}

// Define a function called "PrintSlotMachine" that takes in a 2D slice of runes
func (m *NormalMachine) PrintSlotMachine(columns [][]rune) {
	for _, rowSmall := range columns {
		for _, symbol := range rowSmall {
			fmt.Printf("%c ", symbol)
		}
		fmt.Println()
	}
}

// Define a function called "PrintSlotMachine" that takes in a 2D slice of runes
func (m *JackPot) PrintSlotMachine(columns [][]rune) {
	for _, rowLarge := range columns {
		for _, symbol := range rowLarge {
			fmt.Printf("%c ", symbol)
		}
		fmt.Println()
	}
}

// Refactored code to improve readability and adhere to the specified rules.

// Define a function called "getSlotMachineSpin" that takes in the number of rows, columns, and a symbol count map, and returns a function that takes in a player and returns a 2D matrix of symbols.
func (m *NormalMachine) getSlotMachineSpin(rows, cols int, symbol_count map[rune]int) func(*Player) [][]rune {
	// Return a closure function that takes in a player and returns a 2D matrix of symbols.
	return func(player *Player) [][]rune {
		// Initialize an empty slice of columns with the specified number of columns.
		columns := make([][]rune, cols)
		// Iterate over each column and initialize an empty slice of runes with the specified number of rows.
		for i := range columns {
			columns[i] = make([]rune, rows)
		}

		// Generate a list of all symbols based on the given symbol count map.
		allSymbols := generateAllSymbols(symbol_count)

		// Shuffle the symbols randomly.
		shuffledSymbols := shuffleSymbols(allSymbols)

		// Fill the columns with symbols based on the shuffled symbols and the specified number of rows.
		fillColumns(columns, shuffledSymbols, rows)

		// Deduct the balance from the player's balance and store the new balance.
		newBalance := deductBalance(player.getBalance())
		player.setBalance(newBalance)

		// Return the generated columns.
		return columns
	}
}

// Define a function called "getSlotMachineSpin" that takes in the number of rows, columns, and a symbol count map, and returns a function that takes in a player and returns a 2D matrix of symbols.
func (m *JackPot) getSlotMachineSpin(rows, cols int, symbolCount map[rune]int) func(*Player) [][]rune {
	return func(player *Player) [][]rune {
		columns := make([][]rune, cols)
		for i := range columns {
			columns[i] = make([]rune, rows)
		}

		allSymbols := generateAllSymbolsLarge(symbolCount)
		shuffledSymbols := shuffleSymbols(allSymbols)
		fillColumns(columns, shuffledSymbols, rows)

		newBalance := deductBalance(player.getBalance())
		player.setBalance(newBalance)

		return columns
	}
}

// Helper functions
func generateAllSymbols(symbol_count map[rune]int) []rune {
	var allSymbols []rune

	for symbol, count := range symbol_count {
		for j := 0; j < count; j++ {
			allSymbols = append(allSymbols, symbol)
		}
	}

	return allSymbols
}

// Helper functions
func generateAllSymbolsLarge(symbol_count_large map[rune]int) []rune {
	var allSymbols []rune

	for symbol, count := range symbol_count_large {
		for j := 0; j < count; j++ {
			allSymbols = append(allSymbols, symbol)
		}
	}

	return allSymbols
}

// Helper functions
func shuffleSymbols(symbols []rune) []rune {
	rand.Seed(time.Now().UnixNano())
	rand.Shuffle(len(symbols), func(i, j int) {
		symbols[i], symbols[j] = symbols[j], symbols[i]
	})

	return symbols
}

// Helper functions
func fillColumns(columns [][]rune, symbols []rune, rows int) {
	for i := 0; i < len(columns); i++ {
		copy(columns[i], symbols[i*rows:(i+1)*rows])
	}
}

// Helper functions
func deductBalance(balance float64) float64 {
	return balance - 1.0
}

func (m *NormalMachine) checkWinnings(matrix [][]rune, bet int, values map[rune]int, player *Player) (int, string, error) {
	winnings := 0

	// Get the symbols in the middle row
	middleRowSymbols := matrix[len(matrix)/2]

	// Check if all symbols in the middle row are the same
	allSymbolsSame := isAllSymbolsSame(middleRowSymbols)

	if allSymbolsSame {
		symbol := middleRowSymbols[0]
		winnings = calculateWinnings(symbol, bet, values)

		// Update player's balance
		newBalance := updatePlayerBalance(player, winnings)

		message := generateMessage(newBalance)
		return winnings, message, nil
	} else {
		message := generateMessage(player.getBalance())
		return winnings, message, nil
	}
}

func (m *JackPot) checkWinnings(matrix [][]rune, bet int, values map[rune]int, player *Player) (int, string, error) {
	winnings := 0

	// Get the symbols in the middle row
	middleRowSymbols := matrix[len(matrix)/2]

	// Check if all symbols in the middle row are the same
	allSymbolsSame := isAllSymbolsSame(middleRowSymbols)

	if allSymbolsSame {
		symbol := middleRowSymbols[0]
		winnings = calculateWinnings(symbol, bet, values)

		// Update player's balance
		newBalance := updatePlayerBalance(player, winnings)

		message := generateMessage(newBalance)
		return winnings, message, nil
	} else {
		message := generateMessage(player.getBalance())
		return winnings, message, nil
	}
}

func isAllSymbolsSame(symbols []rune) bool {
	symbol := symbols[0]
	for _, middleSymbol := range symbols {
		if middleSymbol != symbol {
			return false
		}
	}
	return true
}

func calculateWinnings(symbol rune, bet int, values map[rune]int) int {
	return values[symbol] * bet
}

func updatePlayerBalance(player *Player, winnings int) float64 {
	newBalance := player.getBalance() + float64(winnings)
	player.setBalance(newBalance)
	return newBalance
}

func generateMessage(balance float64) string {
	return fmt.Sprintf("Your new balance is: £%.2f\n", balance)
}

// GameController struct represents the game controller
type GameController struct {
	Player
}

// pressSpin simulates a single spin in the game
func (gc *GameController) pressSpin(player *Player) {

	if player.getBalance() < 1.0 {
		fmt.Printf("Your balance is: £%.2f. You don't have enough money\n", player.getBalance())
		return
	}
	// Create an instance of NormalMachine
	var m SlotMachine

	// Set a seed value for the random number generator
	rand.Seed(time.Now().UnixNano())

	randomInt := rand.Intn(101)

	if randomInt > 70 {
		m = &JackPot{}

		spinResult := m.getSlotMachineSpin(rowLarge, colLarge, symbol_count_large)(player)

		m.PrintSlotMachine(spinResult)

		winnings, message, _ := m.checkWinnings(spinResult, bet, symbol_value_large, player)

		fmt.Println(message)
		fmt.Println("Your winnings: £", winnings)
	} else {
		m = &NormalMachine{}

		spinResult := m.getSlotMachineSpin(rowSmall, colSmall, symbol_count)(player)

		m.PrintSlotMachine(spinResult)

		winnings, message, _ := m.checkWinnings(spinResult, bet, symbol_value, player)
		fmt.Println(message)
		fmt.Println("Your winnings: £", winnings)

	}

}

// playGame simulates the game loop
func (gc *GameController) playGame() {
	for {
		gc.pressSpin(&gc.Player)
		fmt.Println("Would you like to play again? (y/n)")
		var choice string
		fmt.Scanln(&choice)

		switch choice {
		case "n":
			// Tell them balance at the end
			fmt.Printf("Your final balance is: £%.2f\n", gc.getBalance())
			fmt.Println("Thanks for playing!")
			return
		case "y":
			continue
		default:
			fmt.Println("Invalid input. Please enter 'y' or 'n'")
		}
	}
}

func main() {
	gameController := GameController{Player: *NewPlayer()}

	// Call the playGame method to start the game
	gameController.playGame()
}

package main

import (
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	math_rand "math/rand"
	"time"
)

// Convert ASCII string to hexadecimal
func asciiToHex(s string) string {
	return hex.EncodeToString([]byte(s))
}

// Convert hexadecimal string to ASCII
func hexToAscii(hexStr string) (string, error) {
	bytes, err := hex.DecodeString(hexStr)
	if err != nil {
		return "", err
	}
	return string(bytes), nil
}

// Convert hexadecimal string to bytes
func hexToBytes(hexStr string) ([]byte, error) {
	return hex.DecodeString(hexStr)
}

// Convert bytes to hexadecimal string
func bytesToHex(b []byte) string {
	return hex.EncodeToString(b)
}

// Convert ASCII string to bytes
func asciiToBytes(s string) []byte {
	return []byte(s)
}

// Convert bytes to ASCII string
func bytesToAscii(b []byte) string {
	return string(b)
}

// Convert ASCII string to base64
func asciiToBase64(s string) string {
	return base64.StdEncoding.EncodeToString([]byte(s))
}

// Convert base64 string to ASCII
func base64ToAscii(b64Str string) (string, error) {
	bytes, err := base64.StdEncoding.DecodeString(b64Str)
	if err != nil {
		return "", err
	}
	return string(bytes), nil
}

// Convert bytes to base64 string
func bytesToBase64(b []byte) string {
	return base64.StdEncoding.EncodeToString(b)
}

// Convert base64 string to bytes
func base64ToBytes(b64Str string) ([]byte, error) {
	return base64.StdEncoding.DecodeString(b64Str)
}

// Generate random hexadecimal string of given length
func generateRandomHex(numberOfHexBytes int) (string, error) {
	bytes := make([]byte, numberOfHexBytes)
	if _, err := rand.Read(bytes); err != nil {
		return "", err
	}
	return hex.EncodeToString(bytes), nil
}

// Generate random text
func generateRandomText(length int) string {
	const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+=[]{}|;:,.<>?/~` "
	seededRand := math_rand.New(math_rand.NewSource(time.Now().UnixNano()))
	b := make([]byte, length)
	for i := range b {
		b[i] = charset[seededRand.Intn(len(charset))]
	}
	return string(b)
}

func main() {
	// Example use cases
	asciiString := "Hello, World!"
	hexString := asciiToHex(asciiString)
	fmt.Printf("ASCII to Hex: %s\n", hexString)

	recoveredAscii, err := hexToAscii(hexString)
	if err != nil {
		log.Fatalf("Error converting hex to ASCII: %v", err)
	}
	fmt.Printf("Hex to ASCII: %s\n", recoveredAscii)

	// Convert ASCII string to bytes and back
	bytesData := asciiToBytes(asciiString)
	fmt.Printf("ASCII to Bytes: %v\n", bytesData)
	fmt.Printf("Bytes to ASCII: %s\n", bytesToAscii(bytesData))

	// Generate random hexadecimal string
	numberOfBytesToGenerate := 200
	randomHex, err := generateRandomHex(numberOfBytesToGenerate)
	if err != nil {
		log.Fatalf("Error generating random hex: %v", err)
	}
	fmt.Printf("Generated Hex: %s\n", randomHex)

	bytesFromHex, err := hexToBytes(randomHex)
	if err != nil {
		log.Fatalf("Error converting hex to bytes: %v", err)
	}
	fmt.Printf("Hex to Bytes: %v\n", bytesFromHex)
	fmt.Printf("Bytes to Hex: %s\n", bytesToHex(bytesFromHex))

	// Convert ASCII string to base64 and back
	base64String := asciiToBase64(asciiString)
	fmt.Printf("ASCII to Base64: %s\n", base64String)

	recoveredBase64, err := base64ToAscii(base64String)
	if err != nil {
		log.Fatalf("Error converting base64 to ASCII: %v", err)
	}
	fmt.Printf("Base64 to ASCII: %s\n", recoveredBase64)

	// Convert bytes to base64 and back
	base64FromBytes := bytesToBase64(bytesData)
	fmt.Printf("Bytes to Base64: %s\n", base64FromBytes)

	recoveredBytes, err := base64ToBytes(base64FromBytes)
	if err != nil {
		log.Fatalf("Error converting base64 to bytes: %v", err)
	}
	fmt.Printf("Base64 to Bytes: %v\n", recoveredBytes)

	// Define the file path
	filePath := "./sample_data/out.txt"
	dirPath := "./sample_data"

	// Check if the directory exists, and create it if it doesn't
	if _, err := os.Stat(dirPath); os.IsNotExist(err) {
		err := os.MkdirAll(dirPath, 0755) // Create the directory with appropriate permissions
		if err != nil {
			log.Fatalf("Error creating directory: %v", err)
		}
	}
	
	// Generate random text, write to file, and read back
	randomText := generateRandomText(200)
	err = ioutil.WriteFile(filePath, []byte(randomText), 0644)
	if err != nil {
		log.Fatalf("Error writing to file: %v", err)
	}

	fileContent, err := ioutil.ReadFile(filePath)
	if err != nil {
		log.Fatalf("Error reading from file: %v", err)
	}

	fileText := string(fileContent)
	fileBytes := asciiToBytes(fileText)
	fileHex := bytesToHex(fileBytes)
	recoveredFileText, err := hexToAscii(fileHex)
	if err != nil {
		log.Fatalf("Error converting file hex to ASCII: %v", err)
	}

	fmt.Printf("Original text: %s\n", fileText)
	fmt.Printf("Text bytes: %v\n", fileBytes)
	fmt.Printf("Hexadecimal string: %s\n", fileHex)
	fmt.Printf("Converted back to ASCII: %s\n", recoveredFileText)

	// Compute SHA-256 hash of the file contents
	fileHash := sha256.Sum256(fileBytes)
	recoveredHash := sha256.Sum256([]byte(recoveredFileText))

	fmt.Printf("SHA-256 hash of file contents: %x\n", fileHash)
	fmt.Printf("SHA-256 hash of recovered string: %x\n", recoveredHash)

	if fileHash == recoveredHash {
		fmt.Println("Hashes [match]")
	} else {
		fmt.Println("Hashes [do not match]")
	}
}

/*
ASCII to Hex: 48656c6c6f2c20576f726c6421
Hex to ASCII: Hello, World!
ASCII to Bytes: [72 101 108 108 111 44 32 87 111 114 108 100 33]
Bytes to ASCII: Hello, World!
Generated Hex: 58a03cf1eb1e0cf9badd41c22f857f334bbe49b3c9900f6daa047b60ef09cc802c8f32f84e1020ccc9430517987a078a8c6c97847c9b92b82eda5b9fe50996adf566d33cba1fa47348be24d378148b372d98a62a2018fdc5787ca79dc0844025a6ef25a723a1e2d38f24aa10eff14826d4a82c25268e51423b24531ad0f8b21417ec6d27fd8961ee397d0b8e82f89e39b16ce7735856d946063518d0c0ca104f0a9058793e3370a49083b13f0b72685be80bfd512eeb54a6a12deadd7f5afa89e4eeecafaa50086b
Hex to Bytes: [88 160 60 241 235 30 12 249 186 221 65 194 47 133 127 51 75 190 73 179 201 144 15 109 170 4 123 96 239 9 204 128 44 143 50 248 78 16 32 204 201 67 5 23 152 122 7 138 140 108 151 132 124 155 146 184 46 218 91 159 229 9 150 173 245 102 211 60 186 31 164 115 72 190 36 211 120 20 139 55 45 152 166 42 32 24 253 197 120 124 167 157 192 132 64 37 166 239 37 167 35 161 226 211 143 36 170 16 239 241 72 38 212 168 44 37 38 142 81 66 59 36 83 26 208 248 178 20 23 236 109 39 253 137 97 238 57 125 11 142 130 248 158 57 177 108 231 115 88 86 217 70 6 53 24 208 192 202 16 79 10 144 88 121 62 51 112 164 144 131 177 63 11 114 104 91 232 11 253 81 46 235 84 166 161 45 234 221 127 90 250 137 228 238 236 175 170 80 8 107]
Bytes to Hex: 58a03cf1eb1e0cf9badd41c22f857f334bbe49b3c9900f6daa047b60ef09cc802c8f32f84e1020ccc9430517987a078a8c6c97847c9b92b82eda5b9fe50996adf566d33cba1fa47348be24d378148b372d98a62a2018fdc5787ca79dc0844025a6ef25a723a1e2d38f24aa10eff14826d4a82c25268e51423b24531ad0f8b21417ec6d27fd8961ee397d0b8e82f89e39b16ce7735856d946063518d0c0ca104f0a9058793e3370a49083b13f0b72685be80bfd512eeb54a6a12deadd7f5afa89e4eeecafaa50086b
ASCII to Base64: SGVsbG8sIFdvcmxkIQ==
Base64 to ASCII: Hello, World!
Bytes to Base64: SGVsbG8sIFdvcmxkIQ==
Base64 to Bytes: [72 101 108 108 111 44 32 87 111 114 108 100 33]
Original text: |jxGc;pq$u9OAW6j~F/~gKF: x7<]Y!{*;H`Q19=R,>xWe_pYd<j5l*WuBv=[p6df-bUXV%$-+}Rx#9#-d<P<h:kA=nsOxDj)Py`tHL=SzS0m 7Y#C!}^AnL&GDi?X!SBVdf(7iugb7Fl/Zi4rRMY4l:}-V8)1phlR&#7g]D.`c.A[Q%$P/9(oj.sEA$,z6eJa|TJD#x
Text bytes: [124 106 120 71 99 59 112 113 36 117 57 79 65 87 54 106 126 70 47 126 103 75 70 58 32 120 55 60 93 89 33 123 42 59 72 96 81 49 57 61 82 44 62 120 87 101 95 112 89 100 60 106 53 108 42 87 117 66 118 61 91 112 54 100 102 45 98 85 88 86 37 36 45 43 125 82 120 35 57 35 45 100 60 80 60 104 58 107 65 61 110 115 79 120 68 106 41 80 121 96 116 72 76 61 83 122 83 48 109 32 55 89 35 67 33 125 94 65 110 76 38 71 68 105 63 88 33 83 66 86 100 102 40 55 105 117 103 98 55 70 108 47 90 105 52 114 82 77 89 52 108 58 125 45 86 56 41 49 112 104 108 82 38 35 55 103 93 68 46 96 99 46 65 91 81 37 36 80 47 57 40 111 106 46 115 69 65 36 44 122 54 101 74 97 124 84 74 68 35 120]
Hexadecimal string: 7c6a7847633b70712475394f4157366a7e462f7e674b463a2078373c5d59217b2a3b48605131393d522c3e7857655f7059643c6a356c2a577542763d5b703664662d6255585625242d2b7d52782339232d643c503c683a6b413d6e734f78446a2950796074484c3d537a53306d2037592343217d5e416e4c264744693f5821534256646628376975676237466c2f5a693472524d59346c3a7d2d5638293170686c52262337675d442e60632e415b512524502f39286f6a2e734541242c7a36654a617c544a442378
Converted back to ASCII: |jxGc;pq$u9OAW6j~F/~gKF: x7<]Y!{*;H`Q19=R,>xWe_pYd<j5l*WuBv=[p6df-bUXV%$-+}Rx#9#-d<P<h:kA=nsOxDj)Py`tHL=SzS0m 7Y#C!}^AnL&GDi?X!SBVdf(7iugb7Fl/Zi4rRMY4l:}-V8)1phlR&#7g]D.`c.A[Q%$P/9(oj.sEA$,z6eJa|TJD#x
SHA-256 hash of file contents: 92cbd7ff82de69f4e40c3ac2603e75f84a5423be7b6cf377191f25a522aef93e
SHA-256 hash of recovered string: 92cbd7ff82de69f4e40c3ac2603e75f84a5423be7b6cf377191f25a522aef93e
Hashes [match]

*/
